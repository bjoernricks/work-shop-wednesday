from typing import Any, Generator


class Loop:
    """Loop v3"""

    _instance: "Loop" = None

    def __init__(self):
        self._running = False
        self._scheduled = []

    @classmethod
    def get_current_loop(cls) -> "Loop":
        if not cls._instance:
            cls._instance = Loop()
        return cls._instance

    def run_step(self) -> None:
        """Run a single step/tick of the loop"""
        try:
            task = self._scheduled.pop(0)  # fifo: extract first item
            while task is not None:
                task.step()
                task = self._scheduled.pop(0)  # fifo: extract first item
        except IndexError:
            # list is empty
            pass

    def run(self, coroutine: Generator[Any, None, Any]) -> Any:
        """Run a coroutine"""
        self._running = True
        step = 1
        while self._running:
            print("Loop step", step, self._scheduled)
            try:
                self.run_step()
                next(coroutine)
                step += 1
            except StopIteration as e:
                self._running = False
                return e.value

    def stop(self) -> None:
        """Stop running the loop"""
        self._running = False

    def schedule(self, task) -> None:
        """Schedule a Task for the next step/tick"""
        self._scheduled.append(task)
