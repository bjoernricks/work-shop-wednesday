## Generators
### What's a Generator
Python defines three terms:
* [generator](https://docs.python.org/3/glossary.html#term-generator)
* [generator iterator](https://docs.python.org/3/glossary.html#term-generator-iterator)
* [generator expression](https://docs.python.org/3/glossary.html#term-generator-expression)


Personally I would use the following terms instead:

* generator function
* generator
* generator expression

The initial version of Generators is defined in [PEP-255](https://peps.python.org/pep-0255/)
for Python 2.2. It has been updated later on to the current implementation of
Generators which has been specified in [PEP-342](https://peps.python.org/pep-0342/)
shipped with Python 2.5 (!). Therefore they are rather old. Maybe that's also
the reason why they don't use *dunder* methods for their protocol.

### Generator base class (without type hints)

A Generator can be expressed as the following class:

```python
class Generator:
    def send(self, value):
        """Send a value into the generator.
        Return next yielded value or raise StopIteration.
        """

    def throw(self, typ, val=None, tb=None):
        """Raise an exception in the generator.
        Return next yielded value or raise StopIteration.
        """

    def close(self):
        """Raise GeneratorExit inside generator.
        """
```
While it is technically possible to write a generator by implementing this
class, a generator can be created easiest by defining a generator function.
Therefore let us take a look at a simple function first.

An example function returning a list of strings:

```python
def get_something_function():
    return ["foo", "bar", "baz"]

something = get_something_function()
print(type(something), something)
```

Output:
```
<class 'list'> ['foo', 'bar', 'baz']
```

Next let us take a look at a simple generator function.

An example generator function **yielding** strings:

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"

something = get_something_generator()
print(type(something), something)
```

Output
```
<class 'generator'> <generator object get_something_generator at 0x7f473fa50c10>
```

It's a generator! Every function containing a `yield` statement will create and
return a generator object when called. Even if the `yield` statement is
contained in an unused branch.

```python
def i_am_a_generator():
    if False:
        yield "foo"
    return "bar"

print(type(i_am_a_generator()))
```

Output
```
<class 'generator'>
```

> The yield statement may only be used inside functions. A function that
> contains a yield statement is called a generator function.

> When a generator function is called [...] no code in the body of the function
> is executed. Instead a generator-iterator object is returned;

[Source](https://peps.python.org/pep-0255/#specification-yield)

Let's take a look on the provided properties and methods of a generator (using
the `dir` function):

```python
print(dir(get_something_generator()))
```

The shown list contains the methods `close`, `send` and `throw` actually. Our
Generator class assumptions seem to be correct!

### Purpose of `close`, `send` and `throw`

A new generator function:

```python
def echo():
    sent = yield 0
    while sent >= 0:
        try:
            sent = yield sent
        except ValueError as e:
            print(e)
    return "Done"
```

#### Send

```python
# stage1 - sending a value
generator = echo()
generator.send(None) # init
generator.send(1)
generator.send(2)
generator.send(-1)
```

Output:

```
>>> generator = echo()
>>> generator.send(None) # init
0
>>> generator.send(1)
1
>>> generator.send(2)
2
>>> generator.send(-1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration: Done
```

When the generator function ends a `StopIteration` exception is raised
automatically.

#### Close

```python
# stage2 - closing a generator
generator = echo()
generator.send(None) # init
generator.send(1)
generator.close()
generator.send(2)
```

Output:

```python
>>> generator = echo()
>>> generator.send(None) # init
0
>>> generator.send(1)
1
>>> generator.close()
>>> generator.send(2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

When the `close` method is called on a generator a [GeneratorExit](https://peps.python.org/pep-0342/#new-standard-exception-generatorexit)
exception is raised within the generator. This exception can't be ignored.


```python
def simple_generator():
    sent = 0
    while True:
        try:
            sent = yield sent
        except GeneratorExit:
            pass


generator = simple_generator()
generator.send(None)
generator.send(123)
generator.close()
```

Output:

```python
>>> generator = simple_generator()
>>> generator.send(None)
0
>>> generator.send(123)
123
>>> generator.close()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: generator ignored GeneratorExit
```

> A generator should handle the GeneratorExit exception by re-raising it
> (or just not catching it) or by raising StopIteration.

Raising `StopIteration` means returning (a value or None) explicitly.

```python
def simple_generator():
    sent = 0
    while True:
        try:
            sent = yield sent
        except GeneratorExit:
            return


generator = simple_generator()
generator.send(None)
generator.send(123)
generator.close()
```

Output:

```python
>>> generator = simple_generator()
>>> generator.send(None)
0
>>> generator.send(123)
123
>>> generator.close()
```

[Source](https://peps.python.org/pep-0342/#new-standard-exception-generatorexit)

The `close` method is intended to be used for releasing resources within the
generator. For example to release a file descriptor or a network connection.

```python
def simple_generator():
    sent = 0
    while True:
        try:
            sent = yield sent
        except GeneratorExit:
            print("I am going to release something")
            return


generator = simple_generator()
generator.send(None)
generator.close()
```

Output:
```python
>>> generator = simple_generator()
>>> generator.send(None)
0
>>> generator.close()
I am going to release something
```

#### Throw

```python
# stage3 - throw into the generator
generator = echo()
generator.send(None) # init
generator.send(1)
generator.throw(ValueError("Foo"))
generator.send(2)
generator.throw(TypeError("Foo"))
generator.send(3)
```

Output:

```
>>> generator = echo()
>>> generator.send(None) # init
0
>>> generator.send(1)
1
>>> generator.throw(ValueError("Foo"))
Foo
1
>>> generator.send(2)
2
>>> generator.throw(TypeError("Foo"))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 5, in echo
TypeError: Foo
>>> generator.send(3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

The `throw` method can be used to raise an exception within the generator. The
exception can be catch via `try...except`.

> If the generator doesn’t catch the exception, the throw() appears to raise the
> same exception passed it (it falls through). If the generator raises another
> exception (this includes the StopIteration produced when it returns) that
> exception is raised by the throw() call.

[Source](https://peps.python.org/pep-0342/#new-generator-method-throw-type-value-none-traceback-none)

### Generator Type

A generator can be annotated by the generic type
`Generator[YieldType, SendType, ReturnType]`.

The `echo` function would have the following signature:

```python
def echo() -> Generator[int, int, str]:
```

We did see where the `YieldType` and `SendType` are used. But what about the
`ReturnType`?

Let's take a look at the following code using the `echo` function:

```python
generator = echo()

generator.send(None) # init

generator.send(1)
generator.send(2)

try:
    generator.send(-1)
except StopIteration as e:
    print(e.value)
```

The return type is converted into the `value` property of the raised
`StopIterator` exception.

If the generator function does not have a return statement, it is `None`
implicitly and then the `value` of the `StopIterator` exception is also `None`.
Therefore the type of a generator is `Generator[YieldType, SendType, None]` in
this case.

This also means that

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"
```

is equivalent to

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"

    return None
```

which is equivalent to

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"

    raise StopIteration(None)
```

### `__del__`

```python
def simple_generator():
    sent = 0
    while True:
        try:
            sent = yield sent
        except GeneratorExit:
            print("Closing generator")
            raise


generator = simple_generator()
generator.send(None)
generator.send(123)
generator = None
```

Output:

```python
>>> generator = simple_generator()
>>> generator.send(None)
0
>>> generator.send(123)
123
>>> generator = None
Closing generator
```

> `g.__del__()` is a wrapper for `g.close()`. This will be called when the
> generator object is garbage-collected (in CPython, this is when its reference
> count goes to zero).

[Source](https://peps.python.org/pep-0342/#new-generator-method-del)
