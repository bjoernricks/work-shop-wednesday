from future import Future

from loop import Loop


def some_result(value):
    future = Future()
    future.set_result(value)
    return (yield from future)


def add(coroutine1, coroutine2):
    x = yield from coroutine1
    y = yield from coroutine2
    return x + y


def main():
    return (yield from add(some_result(1), some_result(2)))


loop = Loop.get_current_loop()
result = loop.run(main())
print("Loop finished with result", result)
