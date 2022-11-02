from typing import Any, Callable, Iterable


class Handle:
    """A callback handle"""

    def __init__(self, name: str, callback: Callable, args: Iterable[Any]):
        self._name = name
        self._callback = callback
        self._args = args

    def run(self) -> None:
        self._callback(*self._args)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name='{self._name}' "
            f"callback='{self._callback.__name__}'>"
        )
