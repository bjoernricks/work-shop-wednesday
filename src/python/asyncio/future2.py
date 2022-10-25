class Future:
    """Return a result in the future v2"""

    _result = None

    def __init__(self, name=None):
        self._name = name

    def set_result(self, result):
        self._result = result

    def result(self):
        return self._result

    def done(self):
        return self.result() is not None

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} name='{self._name}' "
            f"id='{hex(id(self))}'>"
        )

    def __iter__(self):
        yield
        return self.result()
