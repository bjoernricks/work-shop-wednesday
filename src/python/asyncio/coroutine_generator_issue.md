### The Coroutine/Generator Issue

There are some issues in the concept:

* We have (mis-)used the generators
* Generators/Iterators are intended for yielding something that is consumed by
  the caller.
* Implementation wise we have the same thing, but semantically they are very
  different.
* Coroutines in contrast use `yield` and `yield from` to just suspend the
  current function and give control back to the loop.
* From looking at the code or the object users still could mix up coroutines and
  generators because it relies just on a technical detail.
* Using `yield`/`yield from` somewhere in a function declaration to make the
  function asynchronous is not very obvious.
* Users could still pass generators and generators could still run coroutines
  because nothing forbids to use coroutines as generators and the other way
  round.
* Users could refactor a generator function that it becomes a normal function
  (accidentally) just because `yield`/`yield from` is removed.
* As mentioned nothings forbids to pass a normal function as a coroutine. But it
  breaks the concept completely.


At least changing a coroutine to a normal function can be avoided by marking
all coroutine functions via a decorator. If the marked coroutine is changed to
a function an error is raised:

```python
import inspect

def mark_as_coroutine(func):
    if not inspect.isgeneratorfunction(func):
        raise TypeError(f"{func.__name__} is not a generator function")
    func._is_coroutine = True
    return func

def is_coroutine_function(func):
    return getattr(func, "_is_coroutine", False)
```

```python
@mark_as_coroutine
def coroutine():
    yield

@mark_as_coroutine
def just_a_function():
    pass
```

For the other issues:

**Async/Await to the rescue!**
