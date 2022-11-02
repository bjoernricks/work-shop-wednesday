from typing import Any, Generator


class Future:
    """Return a result in the future v2"""

    _result = None

    def __init__(self, name: str = None):
        self._name = name

    def set_result(self, result: Any) -> None:
        self._result = result

    def result(self) -> Any:
        return self._result

    def done(self) -> bool:
        return self.result() is not None

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name='{self._name}' "
            f"id='{hex(id(self))}'>"
        )

    def __iter__(self) -> Generator[None, None, Any]:
        yield
        return self.result()
