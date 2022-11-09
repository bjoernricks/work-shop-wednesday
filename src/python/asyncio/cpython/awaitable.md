### Awaitable Protocol

What has changed since [Generator based coroutines](../cpython.md) in detail?

First of all a new awaitable protocol has been introduced. An object
implementing this protocol can be *awaited* with the `await` statement.

> An object that can be used in an await expression. Can be a coroutine or an
> object with an `__await__()` method

[Source](https://docs.python.org/3/glossary.html#term-awaitable)

```python
from typing import Any, Generator


class Awaitable:

    def __await__(self) -> Generator[Any, None, Any]
        """
        Returns an Generator
        """
```

> We say an object is an awaitable object if it can be used in an `await`
> expression. Many asyncio APIs are designed to accept awaitables.
>
> There are three main types of awaitable objects: coroutines, Tasks, and
> Futures.

> the term “coroutine” can be used for two closely related concepts:
>
> * a *coroutine function*: an `async def` function;
> * a *coroutine object*: an object returned by calling a *coroutine function*.

[Source](https://docs.python.org/3.10/library/asyncio-task.html#awaitables)

Old coroutines are now often called *generator based coroutines* and new ones
are called *native coroutines* to differentiate them.

The previous generator based coroutine code

```python
# some_value = yield from generator_based_coroutine() is the same as
gen = generator_based_coroutine_function().__iter__() # generators are iterators
try:
    while True:
        x = gen.send(None) # same as next(gen)
        yield x
except StopIteration as e:
    some_value = e.value
```

is replaced with

```python
# some_value = await native_coroutine() is the same as
coro = native_coroutine_function().__await__()
try:
    while True:
        x = coro.send(None) # a native coroutine is not an Iterator (no __next__ method)
        yield x
except StopIteration as e:
    some_value = e.value
```

```{admonition} Summary
* `Awaitable`s replace `Iterable`s. That means `__await__` is used instead of
    `__iter__`.
* The `await` statement replaces the `yield from` statement.
