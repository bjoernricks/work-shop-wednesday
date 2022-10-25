class Loop:
    """Loop v2"""

    _instance = None

    def __init__(self):
        self._running = False

    @classmethod
    def get_current_loop(cls):
        if not cls._instance:
            cls._instance = Loop()
        return cls._instance

    def run(self, coroutine):
        """Run a coroutine"""
        self._running = True
        step = 1
        while self._running:
            print("Loop step", step)
            try:
                next(coroutine)
                step += 1
            except StopIteration as e:
                self._running = False
                return e.value

    def stop(self):
        """Stop running the loop"""
        self._running = False
