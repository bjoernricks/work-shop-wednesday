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

Current Implementation of Generators has been specified in
[PEP-342](https://peps.python.org/pep-0342/) shipped with Python 2.5 (!).
Therefore they are rather old. Maybe that's also the reason why they don't use
*dunder* methods for their protocol.

### Generator base class (without type hints)

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
A generator can be created easiest by defining a generator function. Therefore
let us take a look at a simple function first.

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

```python
# stage2 - closing a generator
generator = echo()
generator.send(None) # init
generator.send(1)
generator.close()
generator.send(2)
```

Output:

```
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

A generator can be annotated by the generic type
`Generator[YieldType, SendType, ReturnType]`.

Out echo function would have the following signature:

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
