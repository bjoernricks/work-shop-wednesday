from loop import Loop
from wait import wait


def load_data(host):
    connection = loop.create_connection(host)
    return (yield from connection)


def add(coroutine1, coroutine2):
    x, y = yield from wait([coroutine1, coroutine2])
    return x + y


def main():
    return (yield from add(load_data("1.2.3.4"), load_data("4.2.3.1")))


loop = Loop.get_current_loop()
result = loop.run(main())
print("Loop finished with result", result)
