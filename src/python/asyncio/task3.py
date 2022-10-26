from future import Future

from loop import Loop


class Task(Future):
    """Task v3"""

    def __init__(self, coroutine, name):
        super().__init__(name)
        self._coroutine = coroutine
        self._loop = Loop.get_current_loop()
        self.schedule()

    def step(self):
        try:
            next(self._coroutine)
        except StopIteration as e:
            self.set_result(e.value)
        else:
            # no result yet
            self.schedule()

    def schedule(self):
        self._loop.schedule(self._name, self.step)
