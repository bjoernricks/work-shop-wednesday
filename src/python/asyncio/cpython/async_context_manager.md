### AsyncContextManager

```python
class AsyncContextManager:

    async def __aenter__(self):
        """Return context object upon entering the runtime context."""

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Raise any exception triggered within the runtime context."""
```
