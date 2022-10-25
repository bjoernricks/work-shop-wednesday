from future import Future

from loop import Loop


class Task(Future):
    """Task v4"""

    def __init__(self, coroutine, name=None):
        super().__init__(name)
        self._coroutine = coroutine
        self._loop = Loop.get_current_loop()
        self.schedule()

    def step(self):
        try:
            yielded = next(self._coroutine)
        except StopIteration as e:
            self.set_result(e.value)
        else:
            # no result yet
            if isinstance(yielded, Future):
                # we are blocked by some external event for example waiting for
                # incoming data. let's wait until result is available
                yielded.add_done_callback(self._wakeup)
            else:
                # just schedule again
                self.schedule()

    def schedule(self):
        self._loop.schedule(self._name, self.step)

    def _wakeup(self, _future):
        self.schedule()
