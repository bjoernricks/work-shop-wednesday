### History
#### Python 3.3
* A pluggable event loop, transport and protocol abstractions, and a higher-level scheduler based on yield from [PEP 3156](https://peps.python.org/pep-3156/)

#### Python 3.4
* `asyncio` library added to Python [https://docs.python.org/3.10/whatsnew/3.4.html#new-modules](https://docs.python.org/3.10/whatsnew/3.4.html#new-modules). Before it was developed under the `tulip` umbrella.

#### Python 3.5
* Change StopIteration handling inside generators [PEP 479](https://peps.python.org/pep-0479/)
* async/await syntax [PEP 492](https://peps.python.org/pep-0492/)

#### Python 3.6
*  Asynchronous Comprehensions [PEP 530](https://peps.python.org/pep-0530/)

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


