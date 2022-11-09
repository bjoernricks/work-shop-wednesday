### Async Generators

Additionally to the `AsyncIterator` a `AsyncGenerator` has been introduced in
[PEP 525](https://peps.python.org/pep-0525/) with Python 3.6.

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

Now it gets a bit complicated:

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

An asynchronous generator function is converted into an async generator object
when being called.

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


```{admonition} Summary
```
