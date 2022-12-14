from typing import Any, Callable, Generator

from future import Future
from handle import Handle

# this is just an non runable example how it could possibly work
#
# the real implementation is more complex and depends on the operating system,
# chosen loop implementation, socket type, selector implementation, ...


def create_socket(host) -> Socket:
    # just create a socket connection to a host
    sock = socket.socket()
    sock.setblocking(False)
    sock.connect(host)
    return sock  # a socket


class Loop:
    """Loop v6"""

    _instance: "Loop" = None

    def __init__(self):
        self._running = False
        self._scheduled = []
        self._selector = Selector()  # Some Selector class

    @classmethod
    def get_current_loop(cls) -> "Loop":
        if not cls._instance:
            cls._instance = Loop()
        return cls._instance

    def create_connection(self, host: str):
        waiter = Future()
        socket = create_socket(host)
        self._selector.add(socket, Handle(self._receive_data, waiter, socket))
        return waiter

    def _receive_data(future: Future, socket: Socket):
        data = socket.recv()
        future.set_result(data)

    def run_step(self) -> None:
        """Run a single step/tick of the loop"""
        if not self._scheduled:
            timeout = None  # wait forever until data is available
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

    def run_loop(self) -> None:
        """Run the loop"""
        self._running = True
        step = 1
        while self._running:
            print("Loop step", step, self._scheduled)
            self.run_step()
            step += 1

    def run(self, coroutine: Generator[Any, None, Any]) -> Any:
        """Run a coroutine until it is done/completed"""
        from task import Task  # avoid cyclic dependency

        # create a root task for our coroutine
        # the tasks gets scheduled immediately in its constructor
        task = Task(coroutine, "Initial Task")
        task.add_done_callback(self._done)
        self.run_loop()
        return task.result()

    def stop(self) -> None:
        """Stop running the loop"""
        self._running = False

    def schedule(self, name: str, callback: Callable, *args: Any) -> None:
        """Schedule a callback for the next step/tick"""
        self._scheduled.append(Handle(name, callback, args))

    def _done(self, _future) -> None:
        self.stop()
