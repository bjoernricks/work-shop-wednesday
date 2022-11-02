from typing import Any, Generator

from future import Future


class Task(Future):
    """Task v1"""

    def __init__(self, coroutine: Generator[Any, None, Any], name: str):
        super().__init__(name)
        self._coroutine = coroutine
        self.run_loop()

    def step(self) -> None:
        try:
            next(self._coroutine)
        except StopIteration as e:
            self.set_result(e.value)

    def run_loop(self) -> None:
        while not self.done():
            self.step()
