from typing import TYPE_CHECKING, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


if TYPE_CHECKING:

    def cache(func: Callable[P, T]) -> Callable[P, T]:
        ...

else:
    from functools import cache
