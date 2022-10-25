from loop import Loop


class Future:
    """Return a result in the future v3"""

    _result = None
    _done = False

    def __init__(self, name=None):
        self._name = name
        self._callbacks = []
        self._loop = Loop.get_current_loop()

    def set_result(self, result):
        self._result = result
        self._done = True
        self._schedule_callbacks()

    def result(self):
        return self._result

    def done(self):
        return self._done

    def add_done_callback(self, fn):
        if self.done():
            # we already have a result
            self._loop.schedule(self._name, fn, self)
        else:
            self._callbacks.append(fn)

    def _schedule_callbacks(self):
        if not self._callbacks:
            return

        callbacks = self._callbacks.copy()
        self._callbacks.clear()

        for callback in callbacks:
            self._loop.schedule(self._name, callback, self)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} name='{self._name}' "
            f"id='{hex(id(self))}'>"
        )

    def __iter__(self):
        yield self  # some new magic
        return self.result()
