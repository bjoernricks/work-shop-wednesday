class Future:
    """Return a result in the future v1"""

    _result = None

    def set_result(self, result):
        self._result = result

    def __iter__(self):
        yield
        return self._result
