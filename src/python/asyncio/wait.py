from asyncio import iscoroutine
from typing import Any, Coroutine, Iterable, List, Union

from future import Future
from task import Task


def ensure_future(coro_or_future: Union[Coroutine, Future]) -> Future:
    """
    Ensure that passed object is a Future.

    If it is already a Future it is returned. If it is a coroutine a Task
    wrapping the coroutine is returned.
    """
    if isinstance(coro_or_future, Future):
        return coro_or_future
    elif iscoroutine(coro_or_future):
        return Task(coro_or_future, f"Task for {coro_or_future.__name__}")
    else:
        raise TypeError("A Future, a coroutine or an awaitable is required")


def wait(coros_or_futures: Iterable[Union[Coroutine, Future]]) -> List[Any]:
    """
    Wait for coroutines or futures to finish and gather their results as a list
    """
    counter = len(coros_or_futures)

    futures = [ensure_future(f) for f in coros_or_futures]
    waiter = Future(f"Waiter for {', '.join([str(f) for f in futures])}")

    def _on_completion(_future):
        nonlocal counter
        counter -= 1
        if counter <= 0:
            # all results are available let's wakeup
            waiter.set_result(None)

    for future in futures:
        future.add_done_callback(_on_completion)

    yield from waiter

    return [f.result() for f in futures]
