#### AsyncIO - Async/Await (Python >= 3.7)

Major change is [asyncio.run](https://docs.python.org/3.10/library/asyncio-task.html#asyncio.run).

```python
import asyncio

async def hello_world():
    print("Hello World!")

asyncio.run(hello_world())
```

```python
import asyncio

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))

asyncio.run(print_sum(1, 2))
```

```{admonition} Summary
* No need to know anything about a loop
* Just *run my async stuff!*
```
