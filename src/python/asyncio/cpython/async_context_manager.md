### Async Context Manager

`AsyncContextManager` got introduced in conjunction with the async/await syntax
in [PEP 492](https://peps.python.org/pep-0492/) with Python 3.5.

#### AsyncContextManager

```python
class AsyncContextManager:

    async def __aenter__(self):
        """Return context object upon entering the runtime context."""

    async def __aexit__(self, exc_type: Type[Exception], exc_value, traceback):
        """Raise any exception triggered within the runtime context."""
```

#### `async with`

Async Context Managers are used in conjunction with the `async with` statement.

The `async with` statement is defined as:

```python
async with EXPRESSION as TARGET:
    BLOCK
```

where the *as TARGET* part is optional.

This is semantically equivalent to:

```python
manager = (EXPRESSION)
try:
    TARGET = await manager.__aenter__()
    BLOCK
except:
    if not await manager.__aexit__(mgr, *sys.exc_info()):
        raise
else:
    await manager.__aexit__(mgr, None, None, None)
```

The best example for using an `AsyncContextManager` is creating a connection.
While creating a protocol connection over a network the application code has to
wait until the connection has been established. With an `AsyncContextManager`
the code waiting for the I/O can suspend and some other task can run until the
the connection is ready.

```{admonition} Summary
* `AsyncContextManager` can be used in conjunction with the `async with`
  statement.
* `AsyncContextManager` can suspend when entering the context, for example to
  establish a network connection.
* `AsyncContextManager`can suspend while exiting, for example to close a network
  connection.
```
