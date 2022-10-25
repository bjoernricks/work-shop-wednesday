from future import Future
from task import Task
from wait import wait

from loop import Loop


def some_result(result):
    future = Future("Some Result")
    future.set_result(result)
    return (yield from future)


def add(coroutine1, coroutine2):
    x, y = yield from wait(Task(coroutine1, "Add X"), Task(coroutine2, "Add Y"))
    return x + y


def main():
    return (yield from add(some_result(1), some_result(2)))


loop = Loop.get_current_loop()
result = loop.run(main())
print("Loop finished with result", result)
