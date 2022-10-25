## AsyncIO - Implementation in CPython

### Generator Based (Python < 3.5)

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
    yield from asyncio.sleep(1.0)
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

#### Async/Await (Python >= 3.5 < 3.7)

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

#### Async/Await (Python >= 3.7)

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

### Awaitable Protocol

> An object that can be used in an await expression. Can be a coroutine or an
> object with an __await__() method

[Source](https://docs.python.org/3/glossary.html#term-awaitable)

> We say an object is an awaitable object if it can be used in an `await`
> expression. Many asyncio APIs are designed to accept awaitables.
>
> There are three main types of awaitable objects: coroutines, Tasks, and
> Futures.

> the term “coroutine” can be used for two closely related concepts:
>
> * a *coroutine function*: an `async def` function;
> * a *coroutine object*: an object returned by calling a *coroutine function*.

[Source](https://docs.python.org/3.10/library/asyncio-task.html#awaitables)

```python
class Awaitable:

    def __await__(self):
        """
        Returns an Iterator
        """
```

### Async/Await

Similar to the `yield` statement and generators, every function with an `async` prefix is a coroutine function. Calling the coroutine function doesn't execute
the code directly instead it returns a coroutine object.

```python
 async def foo():
    pass

print(type(foo))
coro = foo()
print(type(coro))
print(dir(coro))
```

Output:

```python
>>> print(type(foo))
<class 'function'>
>>> coro = foo()
>>> print(type(coro))
<class 'coroutine'>
>>> print(dir(coro))
['__await__', ...]
```

These coroutine objects implement the `awaitable` protocol.

Besides the [`async def` function definition](https://docs.python.org/3.10/reference/compound_stmts.html#coroutine-function-definition) there are
additional new expressions and statements. [`await`](https://docs.python.org/3.10/reference/expressions.html#await)
for awaiting a coroutine result, [async for](https://docs.python.org/3.10/reference/compound_stmts.html#the-async-for-statement)
for iterating over async iterables and [async with](https://docs.python.org/3.10/reference/compound_stmts.html#the-async-with-statement)
for async context managers.

> `await` expressions, `async for` and `async with` can only be used in the body
> of a coroutine function.
>
> Functions defined with async def syntax are always coroutine functions, even
> if they do not contain await or async keywords.

[Source](https://docs.python.org/3.10/reference/compound_stmts.html#coroutine-function-definition)


### AsyncIterable

```python
class AsyncIterable:
    def __aiter__(self) -> AsyncIterator:
        """
        Return an AsyncIterator
        """
```

### AsyncIterator

```python
class AsyncIterator(AsyncIterable):
    async def __anext__(self):
        """
        Return the next item or raise StopAsyncIteration when exhausted.
        """
```

### AsyncContextManager

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

### History
#### Python 3.3
* A pluggable event loop, transport and protocol abstractions, and a higher-level scheduler based on yield from https://peps.python.org/pep-3156/

#### Python 3.4
* `asyncio` library added to Python https://docs.python.org/3.10/whatsnew/3.4.html#new-modules. Before it was developed under the `tulip` umbrella.

#### Python 3.5
* async/await syntax https://peps.python.org/pep-0492/
* Change StopIteration handling inside generators https://peps.python.org/pep-0479/

#### Python 3.6
*  Asynchronous Comprehensions https://peps.python.org/pep-0530/

#### Python 3.7
* [asyncio.run](https://docs.python.org/3.10/library/asyncio-task.html#asyncio.run)
* [asyncio.create_task](https://docs.python.org/3.10/library/asyncio-task.html#asyncio.to_thread)

#### Python 3.8
* [asyncio repl](https://github.com/python/cpython/issues/81209) -> Running `python -m asyncio` launches a natively async REPL. This allows rapid experimentation with code that has a top-level await.
* [unittest.mock.AsyncMock and unittest.IsolatedAsyncioTestCase](https://docs.python.org/3/whatsnew/3.8.html#unittest)

#### Python 3.9
* [asyncio.to_thread](https://docs.python.org/3.10/library/asyncio-task.html#asyncio.to_thread) -> for running IO-bound functions in a separate thread to avoid blocking the event loop

#### Python 3.10
* [aiter and anext](https://github.com/python/cpython/issues/76042) -> async versions of iter and next

#### Python 3.11
* [TaskGroup](https://docs.python.org/3.11/library/asyncio-task.html#task-groups) -> structured concurrency in asyncio


### Links

* [Real Python - Speed Up Your Python Program With Concurrency](https://realpython.com/python-concurrency/)
* [Real Python - Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
* [testdrive.io - Speeding Up Python with Concurrency, Parallelism, and asyncio](https://testdriven.io/blog/concurrency-parallelism-asyncio/)
* [How the heck does async/await work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/)
* [Waiting in asyncio](https://hynek.me/articles/waiting-in-asyncio/)
