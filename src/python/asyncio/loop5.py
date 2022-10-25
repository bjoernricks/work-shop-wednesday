from handle import Handle


class Loop:
    """Loop v5"""

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
        # execute all current known handles only.
        # not the ones added while running the handle callbacks
        scheduled = self._scheduled.copy()
        self._scheduled.clear()

        try:
            handle = scheduled.pop(0)  # fifo: extract first item
            while handle is not None:
                handle.run()
                handle = scheduled.pop(0)  # fifo: extract first item
        except IndexError:
            # list is empty
            pass

        # a shorter and even more smarter version
        #
        # for _ in range(len(self._scheduled)):
        #     handle = self._scheduled.pop(0)  # fifo: extract first item
        #     handle.run()

    def run_loop(self):
        """Run the loop"""
        self._running = True
        step = 1
        while self._running:
            print("Loop step", step, self._scheduled)
            self.run_step()
            step += 1

    def run(self, coroutine):
        """Run a coroutine until it is done/completed"""
        from task import Task  # avoid cyclic dependency

        task = Task(coroutine, "Initial Task")
        task.add_done_callback(self._done)
        self.run_loop()
        return task.result()

    def stop(self):
        """Stop running the loop"""
        self._running = False

    def schedule(self, name, callback, *args):
        """Schedule a callback for the next step/tick"""
        self._scheduled.append(Handle(name, callback, args))

    def _done(self, _future):
        self.stop()
