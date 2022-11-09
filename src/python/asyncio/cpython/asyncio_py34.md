### AsyncIO - Generator Based (Python < 3.5)

[Async generator-based coroutines](https://docs.python.org/3.10/library/asyncio-task.html#asyncio-generator-based-coro)
have been introduced with [PEP 3156](https://peps.python.org/pep-3156/) in
Python 3.3 and are usable with the introduction of the `asyncio` library in
[Python 3.4](https://docs.python.org/3.10/whatsnew/3.4.html#new-modules).
They already got replaced in Python 3.5. Support for generator-based coroutines
in asyncio is deprecated and is removed in Python 3.11.

```python
import asyncio

@asyncio.coroutine
def hello_world():
    print("Hello World!")

loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()
```

[Source](https://docs.python.org/3.4/library/asyncio-task.html#asyncio-hello-world-coroutine)

```python
import asyncio

@asyncio.coroutine
def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    yield from asyncio.sleep(1.0) # uses a Future
    return x + y

@asyncio.coroutine
def print_sum(x, y):
    result = yield from compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()
```

![Sequence Diagram](https://docs.python.org/3.4/_images/tulip_coro.png)

> The “Task” is created by the BaseEventLoop.run_until_complete() method when it gets a coroutine object instead of a task.

[Source](https://docs.python.org/3.4/library/asyncio-task.html#example-chain-coroutines)

Looks very familiar to our [implementation](implementing.md) isn't it?


```{admonition} Summary
* `Generator` based coroutines are used for pre-emptive multitasking.
* `asyncio` provides an *event* loop.
* The loop is returned by a factory function.
* A main coroutine is run in the loop until it is finished.
* A `Task` is created for running the main coroutine.
* `yield from` is used to suspend and resume coroutines.
* Coroutines are marked as coroutines with a `decorator`.
* The coroutine decorator converts *normal* functions into coroutines.
```
