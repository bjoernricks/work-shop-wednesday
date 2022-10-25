class Handle:
    """A callback handle"""

    def __init__(self, name, callback, args):
        self._name = name
        self._callback = callback
        self._args = args

    def run(self):
        self._callback(*self._args)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} name='{self._name}' "
            f"callback='{self._callback.__name__}'>"
        )
