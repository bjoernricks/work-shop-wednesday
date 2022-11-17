### Async Generators

Additionally to the `AsyncIterator` a `AsyncGenerator` has been introduced in
[PEP 525](https://peps.python.org/pep-0525/) with Python 3.6.

Having `async/await` instead of `yield/yield from` for coroutines allows to use
`yield` for the initial purpose again: yielding via Generators.

#### AsyncGenerator

```python
class AsyncGenerator(AsyncIterator):
    async def asend(self, value: Any) -> Any:
        """
        Send a value into the asynchronous generator.
        Return next yielded value or raise StopAsyncIteration.
        """

    async def athrow(self, typ: Type[Exception], val=None, tb=None) -> Any:
        """
        Raise an exception in the asynchronous generator.
        Return next yielded value or raise StopAsyncIteration.
        """

    async def aclose(self) -> None:
        """
        Raise GeneratorExit inside coroutine.
        """
        try:
            await self.athrow(GeneratorExit)
        except (GeneratorExit, StopAsyncIteration):
            pass
        else:
            raise RuntimeError("asynchronous generator ignored GeneratorExit")

    async def __anext__(self) -> Any:
        """
        Return the next item from the asynchronous generator.
        When exhausted, raise StopAsyncIteration.
        """
        return await self.asend(None)
```

#### Async Generator Function

What's the purpose of an `AsyncGenerator`? Mostly to implement `async generator
functions`.

An `async generator function` is an `async def` function containing
a `yield` statement. `async generator functions` get converted to
`AsyncGenerator` objects when being called in the same manner as
`generator functions` get converted to `Generator` objects.

```python
async def foo():
    pass


async def bar():
    await foo()
    yield 42


gen = bar()
print(gen, type(gen))
```

Output:

```
<async_generator object bar at 0x7f5c90e9bbc0> <class 'async_generator'>
```

Without `async generator functions` iteration must be written by implementing an
`AsyncIterator` in a similar fashion like the following simplified example:

```python
from typing import AsyncIterator


class HttpPaginationAsyncIterator(AsyncIterator):
    def __init__(client: AsyncHttpClient, url: str):
        self.client = client
        self._next_url = url

    async def __anext__(self) -> dict:
        if not self._next_url:
            raise StopAsyncIteration()

        response = self.client.get(self._next_url)
        self._next_url = get_next_url(response)
        return response.json()


async def get_all_data(url: str) -> AsyncIterator[dict]:
    client = AsyncHttpClient()
    return HttpPaginationAsyncIterator(client, url)


async for data in get_all_data(SOME_URL):
    ...
```

With an `async generator function` this can be simplified

```python
async def get_all_data(url: str) -> dict:
    client = AsyncHttpClient()
    next_url = url
    while next_url:
        response = client.get(next_url)
        next_url = get_next_url(response)
        yield response.json()


async for data in get_all_data(SOME_URL):
    ...
```

Now it gets a bit complicated. We got four different function types:

```python
def func():            # a function
    return

def genfunc():         # a generator function
    yield

async def coro():      # a coroutine function
    await smth()

async def asyncgen():  # an asynchronous generator function
    await smth()
    yield 42
```

#### Issues

* `yield from` is not allowed in async generator functions.

```python
async def foo():
    for i in range(1, 10):
        yield i


async def bar():
    # yield from foo() is not allowed
    for i in foo():
        yield i
    yield 42
```

* You can't convert an `AsyncGenerator` or `AsyncIterator` into a sequence.

```python
async def bar():
    yield 42


sequence = list(bar())
```

Output:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'async_generator' object is not iterable
```

Converting isn't possible (at least at the moment) because `list` expects an
`Iterable` and can't handle an `AsyncIterable`.

Instead the following code must be used:

```python
async def bar():
    yield 42


sequence = [i async for i in bar()] # using PEP 530 – Asynchronous Comprehensions
```

```{admonition} Summary
* `AsyncGenerator` allows to write `async generator functions`.
* An `async generator function` is an async function containing the `yield`
  statement.
* `async generator functions` allow to write `AsyncIterators` more easily.
```
