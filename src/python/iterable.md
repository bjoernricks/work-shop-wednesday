## Iterable

### What's an Iterable

> An object capable of returning its members one at a time. Examples of
> iterables include all sequence types (such as list, str, and tuple) and some
> non-sequence types like dict, file objects, and objects of any classes you
> define with an __iter__() method [...]

> Iterables can be used in a for loop and in many other places where a sequence
> is needed [...]. When an iterable object is passed as an argument to the
> built-in function iter(), it returns an iterator for the object. This iterator
> is good for one pass over the set of values.

[Source](https://docs.python.org/3/glossary.html#term-iterable)


### Iterable base class (without type hints)

```python
class Iterable:

    def __iter__(self):
        """
        Returns an Iterator
        """
```

An Iterable is a class implementing the `__iter__` method.

### for ... in loop

When showing the [for loop semantics in the Iterator chapter](iterators.md#for-loop)
the Iterator was left out.


Actually a simplified version of a function mimicking a `for ... in` loop
behavior to print the values of an `Iterator` must be written as:

```python
def for_loop(iterable):
    iterator = iter(iterable)
    while True:
        try:
            value = next(iterator)
            print(value)
        except StopIteration:
            return

for_loop(get_something_iterator())
```

> When using iterables, it is usually not necessary to call iter() or deal with
> iterator objects yourself. The for statement does that automatically for you,
> creating a temporary unnamed variable to hold the iterator for the duration of
> the loop

[Source](https://docs.python.org/3/glossary.html#term-iterable)

Therefore an `Iterator` can be represented as:

```python
class Iterator(Iterable):
    def __next__(self):
        """Return the next item from the iterator.
        When exhausted, raise StopIteration
        """

    def __iter__(self):
        """
        Return the corresponding Iterator which is self
        """
        return self
```

And a `Generator` can be represented now as:

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
        try:
            self.throw(GeneratorExit)
        except (GeneratorExit, StopIteration):
            pass
        else:
            raise RuntimeError("generator ignored GeneratorExit")

    def __next__(self):
        return self.send(None)

    def __iter__(self):
        return self

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
```

### Links

* [Python Glossary - iterable](https://docs.python.org/3.10/glossary.html#term-iterable)
* [collections.abc.Iterable](https://github.com/python/cpython/blob/3.10/Lib/_collections_abc.py#L253)
* [iter function](https://docs.python.org/3.10/library/functions.html#iter)
