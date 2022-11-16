from enum import Enum
from typing import Any, Callable, Generator

from loop import Loop


class CancelledError(Exception):
    """
    Raised if a Future is cancelled
    """


class FutureState(Enum):
    PENDING = "pending"
    DONE = "done"
    CANCELLED = "cancelled"


class Future:
    """Return a result in the future v5"""

    _result = None

    def __init__(self, name: str = None):
        self._name = name
        self._callbacks = []
        self._state = FutureState.PENDING
        self._loop = Loop.get_current_loop()

    def set_result(self, result: Any):
        if self._state != FutureState.PENDING:
            raise RuntimeError("Invalid Future state")

        self._result = result
        self._state = FutureState.DONE
        self._schedule_callbacks()

    def cancel(self) -> bool:
        if self._state != FutureState.PENDING:
            return False

        self._state = FutureState.CANCELLED
        self._schedule_callbacks()
        return True

    def result(self) -> Any:
        if self._state == FutureState.CANCELLED:
            raise CancelledError()
        if self._state != FutureState.DONE:
            raise RuntimeError("Invalid Future state")
        return self._result

    def done(self) -> bool:
        return self._state == FutureState.DONE

    def cancelled(self) -> bool:
        return self._state == FutureState.CANCELLED

    def add_done_callback(self, fn: Callable[["Future"], None]) -> None:
        if self._state != FutureState.PENDING:
            # we already have a result or are cancelled
            self._loop.schedule(self._name, fn, self)
        else:
            self._callbacks.append(fn)

    def _schedule_callbacks(self) -> None:
        if not self._callbacks:
            return

        callbacks = self._callbacks.copy()
        self._callbacks.clear()

        for callback in callbacks:
            self._loop.schedule(self._name, callback, self)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name='{self._name}' "
            f"state={self._state} id='{hex(id(self))}'>"
        )

    def __iter__(self) -> Generator["Future", None, Any]:
        yield self
        return self.result()

    __await__ = __iter__
