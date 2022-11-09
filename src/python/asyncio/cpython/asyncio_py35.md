#### AsyncIO - Async/Await (Python >= 3.5 < 3.7)

Major change is [PEP 492 – Coroutines with async and await syntax](https://peps.python.org/pep-0492/).

```python
import asyncio

async def hello_world():
    print("Hello World!")

loop = asyncio.get_event_loop()
loop.run_until_complete(hello_world())
loop.close()
```

[Source](https://docs.python.org/3.5/library/asyncio-task.html#example-hello-world-coroutine)

```python
import asyncio

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()
```

[Source](https://docs.python.org/3.5/library/asyncio-task.html#example-chain-coroutines)


```{admonition} Summary
* Explicit syntax for asyncio: async and await statements
* No coroutine decorator
* Native coroutines
```
