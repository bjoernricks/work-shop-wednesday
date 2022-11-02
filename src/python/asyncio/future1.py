from typing import Any, Generator


class Future:
    """Return a result in the future v1"""

    _result = None

    def set_result(self, result: Any):
        self._result = result

    def __iter__(self) -> Generator[None, None, Any]:
        yield
        return self._result
