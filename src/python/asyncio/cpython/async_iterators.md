### Async Iterators

`AsyncIterable` and `AsyncIterator` got introduced in conjunction with the
async/await syntax in [PEP 492](https://peps.python.org/pep-0492/) with Python
3.5.

`AsyncIterators` in conjunction with the new `async for` statement allow
iterating over items that have been requested asynchronously. That means the
`async for` loop may suspend on every iteration until the next iteration result
is available.

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
    async def __anext__(self) -> Any:
        """
        Return the next item or raise StopAsyncIteration when exhausted.
        """
```

#### `async for`

A new `async for` statement is used in conjunction with `AsyncIterators`.

```python
async for TARGET in ITER:
    BLOCK
else:
    BLOCK2
```

```python
iterable = (ITER)
iter = iterable.__aiter__()
running = True
while running:
    try:
        TARGET = await iter.__anext__()
    except StopAsyncIteration:
        running = False
    else:
        BLOCK
else:
    BLOCK2
```

```{admonition} Summary
* `AsyncIterator` can be used in conjunction with the `async for` statement.
* `AsyncIterator` can suspend on each iteration, for example to request new data
  from the network.
```
