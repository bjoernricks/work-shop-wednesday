## Iterators
### From Generators to Iterators

Back to our initial very simple generator. What's the `YieldType`, `SendType`
and `ReturnType` of this generator?

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"
```

Actually it could be written as:

```python
from typing import Generator

def get_something_generator() -> Generator[str, None, None]:
    yield "foo"
    yield "bar"
    yield "baz"
```

This generator doesn't receive and return anything and just yields a value on
every call. That means when calling we **iterate** over some values? Yes indeed.
Therefore `Generator[YieldType, None, None]` could be rewritten as
`Iterator[YieldType]`.

```python
from typing import Iterator

def get_something_iterator() -> Iterator[str]:
    yield "foo"
    yield "bar"
    yield "baz"
```

### What's an Iterator

Citing the Python docs, an Iterator is

> An object representing a stream of data. Repeated calls to the iterator’s `__next__()` method [...] return successive items in the stream. When no more data are available a StopIteration exception is raised instead.

[Source](https://docs.python.org/3/glossary.html#term-iterator)

### Iterator base class

From the definition above we can derive a base class:

```python
class Iterator:
    def __next__(self):
        """Return the next item from the iterator.
        When exhausted, raise StopIteration
        """
```

Hey, but if an `Iterator` is a `Generator` where are the generator protocol
methods?

Let's take a look at the methods of a `generator` object again:

```python
print(dir(get_something_iterator()))
```

It contains the `__next__` *dunder* method of the `Iterator`. Does that mean ...
Yes maybe from looking at the `dir(get_something_iterator())` output you already
recognized the culprit. We lied initially about the Generator base class. I am
very sorry!

Actually the `Generator` base class looks like:

```python
class Generator(Iterator):
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

A `Generator` is derived from an `Iterator` which provides `__next__`. That's
why the Python glossary uses the term `generator iterator` instead of
`generator` but actually it might be a `iterator generator`. Because this is a
bit confusing and the class name is also just `generator` the term `generator`
fits best to me.

When providing the Iterator protocol for the Generator it could be implemented
with the following `__next__` method:

```python
    def __next__(self):
        """Return the next item from the generator.
        When exhausted, raise StopIteration.
        """
        return self.send(None)
```

To verify this behavior let us take look at our simple generator/iterator
function:

```python
def get_something_iterator():
    yield "foo"
    yield "bar"
    yield "baz"
```

Using it as a `Generator`:

```python
generator = get_something_iterator()
generator.send(None)
generator.send(None)
generator.send(None)
generator.send(None)
```

Output:
```
>>> generator = get_something_iterator()
>>> generator.send(None)
'foo'
>>> generator.send(None)
'bar'
>>> generator.send(None)
'baz'
>>> generator.send(None)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

Which is actually the same as using the `Iterator` behavior with the
[`next`](https://docs.python.org/3.10/library/functions.html#next) function:

```python
iterator = get_something_iterator()
next(iterator)
next(iterator)
next(iterator)
next(iterator)
```

Output:

```
>>> iterator = get_something_iterator()
>>> next(iterator)
'foo'
>>> next(iterator)
'bar'
>>> next(iterator)
'baz'
>>> next(iterator)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

### For Loop

Simplified version of a function mimicking a `for ... in` loop behavior to
print the values of an `Iterator`:

```python
def for_loop(iterator):
    while True:
        try:
            value = next(iterator)
            print(value)
        except StopIteration:
            return

for_loop(get_something_iterator())
```

The same behavior written with a real `for ... in` loop:

```python
for value in get_something_iterator():
    print(value)
```

### Call Flow

What's the interesting thing about `Generators`/`Iterators` and the `yield`
statement? Let us look at the following call flows:

```python
def get_something_generator():
    print("Within generator 1")
    yield "foo"
    print("Within generator 2")
    yield "bar"
    print("Within generator 3")
    yield "baz"
    print("Within generator 4")
```

```python
for i in get_something_generator():
    print("Within for 1")
    print(i)
    print("Within for 2")
```

Output:

```
Within generator 1
Within for 1
foo
Within for 2
Within generator 2
Within for 1
bar
Within for 2
Within generator 3
Within for 1
baz
Within for 2
Within generator 4
```

In contrast to iterating over a list:

```python
for i in list(get_something_generator()):
    print("Within for 1")
    print(i)
    print("Within for 2")
```

Output:

```
Within generator 1
Within generator 2
Within generator 3
Within generator 4
Within for 1
foo
Within for 2
Within for 1
bar
Within for 2
Within for 1
baz
Within for 2
```

A `yield` statements suspend the current execution sequence and returns to the
calling statement! As you can see therefore **Python Generators/Iterators are
coroutines!**

> Coroutines are computer program components that generalize subroutines for non-preemptive multitasking, by allowing execution to be suspended and resumed.

### Chaining Iterators

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"

def another_generator():
    for i in get_something_generator():
        yield i

for i in another_generator():
    print(i)
```

With Python 3.3 and [PEP 380](https://peps.python.org/pep-0380) it can be
simplified using the `yield from` statement:

```python
def get_something_generator():
    yield "foo"
    yield "bar"
    yield "baz"

def another_generator():
    yield from get_something_generator()

for i in another_generator():
    print(i)
```

### Links

* [Real Python - How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/)
* [PEP 255 – Simple Generators](https://peps.python.org/pep-0255/)
* [PEP 342 – Coroutines via Enhanced Generators](https://peps.python.org/pep-0342/)
* [PEP 380 – Syntax for Delegating to a Subgenerator](https://peps.python.org/pep-0380/)
* [Generator-iterator methods](https://docs.python.org/3.10/reference/expressions.html#generator-iterator-methods)
* [Iterator Types](https://docs.python.org/3.10/library/stdtypes.html?highlight=next#iterator-types)
* [Generator Types](https://docs.python.org/3.10/library/stdtypes.html?highlight=next#generator-types)
* [collections.abc.Iterator](https://github.com/python/cpython/blob/3.10/Lib/_collections_abc.py#L271)
* [collections.abc.Generator](https://github.com/python/cpython/blob/3.10/Lib/_collections_abc.py#L322)
