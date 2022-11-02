### Awaitable Protocol

> An object that can be used in an await expression. Can be a coroutine or an
> object with an `__await__()` method

[Source](https://docs.python.org/3/glossary.html#term-awaitable)

```python
from typing import Any, Iterator


class Awaitable:

    def __await__(self) -> Iterator[Any]:
        """
        Returns an Iterator
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


