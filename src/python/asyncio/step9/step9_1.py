from loop import Loop


class Future:
    """Return a result in the future"""

    _result = None

    def set_result(self, result):
        self._result = result

    def __iter__(self):
        print(self.__class__.__name__, 1)
        yield
        print(self.__class__.__name__, 2)
        return self._result


def some_result(value):
    future = Future()
    future.set_result(value)
    print(some_result.__name__, 1)
    return (yield from future)


def add(coroutine1, coroutine2):
    print(add.__name__, 1)
    x = yield from coroutine1
    print(add.__name__, 2)
    y = yield from coroutine2
    print(add.__name__, 3)
    return x + y


def main():
    print(main.__name__, 1)
    result = yield from add(some_result(1), some_result(2))
    print(main.__name__, 1)
    return result


loop = Loop.get_current_loop()
result = loop.run(main())
print("Loop finished with result", result)
