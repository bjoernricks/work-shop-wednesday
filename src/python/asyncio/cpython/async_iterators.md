### Async Generators/Iterators

#### AsyncGenerator

```python
class AsyncGenerator(AsyncIterator):
    async def asend(self, value):
        """
        Send a value into the asynchronous generator.
        Return next yielded value or raise StopAsyncIteration.
        """

    async def athrow(self, typ, val=None, tb=None):
        """
        Raise an exception in the asynchronous generator.
        Return next yielded value or raise StopAsyncIteration.
        """

    async def aclose(self):
        """
        Raise GeneratorExit inside coroutine.
        """
        try:
            await self.athrow(GeneratorExit)
        except (GeneratorExit, StopAsyncIteration):
            pass
        else:
            raise RuntimeError("asynchronous generator ignored GeneratorExit")

    async def __anext__(self):
        """
        Return the next item from the asynchronous generator.
        When exhausted, raise StopAsyncIteration.
        """
        return await self.asend(None)
```

#### AsyncIterable

```python
class AsyncIterable:
    def __aiter__(self) -> AsyncIterator:
        """
        Return an AsyncIterator
        """
```

#### AsyncIterator

```python
class AsyncIterator(AsyncIterable):
    async def __anext__(self):
        """
        Return the next item or raise StopAsyncIteration when exhausted.
        """
```

