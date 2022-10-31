from handle import Handle


class Loop:
    """Loop v4"""

    _instance = None

    def __init__(self):
        self._running = False
        self._scheduled = []

    @classmethod
    def get_current_loop(cls):
        if not cls._instance:
            cls._instance = Loop()
        return cls._instance

    def run_step(self):
        """Run a single step/tick of the loop"""
        try:
            handle = self._scheduled.pop(0)  # fifo: extract first item
            while handle is not None:
                handle.run()
                handle = self._scheduled.pop(0)  # fifo: extract first item
        except IndexError:
            # list is empty
            pass

    def run(self, coroutine):
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

    def stop(self):
        """Stop running the loop"""
        self._running = False

    def schedule(self, name, callback, *args):
        """Schedule a callback for the next step/tick"""
        self._scheduled.append(Handle(name, callback, args))