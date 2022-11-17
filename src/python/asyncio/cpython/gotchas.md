### Gotchas with asyncio

#### RuntimeWarning: coroutine 'xyz' was never awaited

A very common mistake is to forget the `await` statement when calling
coroutines. You will run into it several times. I Promise!

```python
import asyncio

async def coro():
  return 42


async def other_coro():
  coro()

asyncio.run(other_coro())
```

Output:

```
<stdin>:2: RuntimeWarning: coroutine 'coro' was never awaited
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```

