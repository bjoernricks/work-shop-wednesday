from typing import Any, Generator

from future import Future

from loop import Loop


class Task(Future):
    """Task v2"""

    def __init__(self, coroutine: Generator[Any, None, Any], name: str):
        super().__init__(name)
        self._coroutine = coroutine
        self._loop = Loop.get_current_loop()
        self.schedule()

    def step(self) -> None:
        try:
            next(self._coroutine)
        except StopIteration as e:
            self.set_result(e.value)
        else:
            # no result yet
            self.schedule()

    def schedule(self) -> None:
        self._loop.schedule(self)
