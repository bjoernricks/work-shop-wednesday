from future import Future


class Task(Future):
    """Task v1"""

    def __init__(self, coroutine, name=None):
        super().__init__(name)
        self._coroutine = coroutine
        self.run_loop()

    def step(self):
        try:
            next(self._coroutine)
        except StopIteration as e:
            self.set_result(e.value)

    def run_loop(self):
        while not self.done():
            self.step()
