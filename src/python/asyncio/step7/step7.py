from future import Future

from loop import loop


def some_result(value):
    # just a coroutine to return some value
    future = Future()
    # do something, we just fake it here
    future.set_result(value)
    return (yield from future)


def add(coroutine1, coroutine2):
    x = yield from coroutine1
    y = yield from coroutine2
    return x + y


def main():
    return (yield from add(some_result(1), some_result(2)))


result = loop(main())
print("Loop finished with result", result)
