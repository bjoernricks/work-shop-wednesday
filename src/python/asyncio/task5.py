from typing import Any, Generator

from future import CancelledError, Future
from loop import Loop


class Task(Future):
    """Task v5"""

    def __init__(self, coroutine: Generator[Any, None, Any], name: str):
        super().__init__(name)
        self._coroutine = coroutine
        self._loop = Loop.get_current_loop()
        self._fut_waiter = None
        self._must_cancel = False
        self.schedule()

    def step(self, exc: Exception = None) -> None:
        self._fut_waiter = None

        if self._must_cancel:
            if not isinstance(exc, CancelledError):
                exc = CancelledError()
            self._must_cancel = False

        try:
            if exc is None:
                yielded = self._coroutine.send(None)
            else:
                # This may also be a cancellation.
                yielded = self._coroutine.throw(exc)
        except StopIteration as e:
            self.set_result(e.value)
        except CancelledError:
            # coroutine is cancelled
            # update task status via future
            super().cancel()
        else:
            # no result yet
            if isinstance(yielded, Future):
                # we are blocked by some external event for example waiting for
                # incoming data. let's wait until result is available
                yielded.add_done_callback(self._wakeup)
                self._fut_waiter = yielded
                if self._must_cancel:  # may have been set since last suspend
                    if yielded.cancel():
                        self._must_cancel = False
            else:
                # just schedule again
                self.schedule()

    def schedule(self, exc: Exception = None) -> None:
        self._loop.schedule(self._name, self.step, exc)

    def cancel(self) -> bool:
        if self.done():
            return False

        if self._fut_waiter is not None:
            # we are waiting for a "blocked" result
            if self._fut_waiter.cancel():
                return True

        # task is just scheduled now
        self._must_cancel = True
        return True

    def _wakeup(self, future: Future) -> None:
        try:
            future.result()
        except Exception as exc:
            # This may also be a cancellation.
            self.schedule(exc)
        else:
            self.schedule()
