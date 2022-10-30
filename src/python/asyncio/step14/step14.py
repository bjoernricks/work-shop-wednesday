from future import Future
from handle import Handle
from task import Task
from wait import wait

# this is just an non runable example how it could possibly work
#
# the real implementation is more complex and depends on the operating system,
# chosen loop implementation, socket type, selector implementation, ...


def create_socket(host):
    # just create a socket connection to a host
    sock = socket.socket()
    sock.setblocking(False)
    sock.connect(host)
    return sock  # a socket


class Loop:
    """Loop v5"""

    _instance = None

    def __init__(self):
        self._running = False
        self._scheduled = []
        self._selector = Selector()  # Some Selector class

    @classmethod
    def get_current_loop(cls):
        if not cls._instance:
            cls._instance = Loop()
        return cls._instance

    def run_step(self):
        if not self._scheduled:
            timeout = None  # wait forever
        else:
            timeout = 0  # just get the sockets with data

        # wait and block for data depending on the timeout
        # returns an iterable of handles which corresponding sockets have data
        handles = self._selector.select(timeout)
        if handles:
            self._scheduled.extend(handles)

        for _ in range(len(self._scheduled)):
            handle = self._scheduled.pop(0)  # fifo: extract first item
            handle.run()

    def create_connection(self, host):
        waiter = Future()
        socket = create_socket(host)
        self._selector.add(socket, Handle(self._receive_data, waiter, socket))
        return waiter

    def _receive_data(future, socket):
        data = socket.recv()
        future.set_result(data)

    def run_loop(self):
        self._running = True
        step = 1
        while self._running:
            print("Loop step", step, self._scheduled)
            self.run_step()
            step += 1

    def run(self, coroutine):
        # run until complete/done
        from task import Task  # avoid cyclic dependency

        task = Task(coroutine, "Initial Task")
        task.add_done_callback(self._done)
        self.run_loop()
        return task.result()

    def stop(self):
        self._running = False

    def schedule(self, name, callback, *args):
        self._scheduled.append(Handle(name, callback, args))

    def _done(self, _future):
        self.stop()


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
