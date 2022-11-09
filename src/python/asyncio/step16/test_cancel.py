from future import Future
from loop import Loop
from task import Task
from wait import wait


def some_result(result):
    future = Future("Some Result")
    future.set_result(result)
    return (yield from future)


def add(coroutine1, coroutine2):
    x, y = yield from wait([coroutine1, coroutine2])
    return x + y


def main():
    future = Future("Test")
    future.cancel()
    return (yield from future)


loop = Loop.get_current_loop()
result = loop.run(main())
print("Loop finished with result", result)
