from typing import TypeVar

from promplate.llm.base import LLM

prefix2llm: dict[str, LLM] = {}


T = TypeVar("T", bound=LLM)


def link_llm(*prefixes: str):
    def decorator(llm_class: type[T]) -> type[T]:
        class Wrapper(llm_class):  # type: ignore
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for prefix in prefixes:
                    prefix2llm[prefix] = self

        Wrapper.__doc__ = llm_class.__doc__
        Wrapper.__name__ = llm_class.__name__
        Wrapper.__module__ = llm_class.__module__
        Wrapper.__qualname__ = llm_class.__qualname__

        return Wrapper  # type: ignore

    return decorator


def find_llm(name: str):
    for prefix in sorted(prefix2llm, key=len, reverse=True):  # longest prefix first
        if name.startswith(prefix):
            return prefix2llm[prefix]
    raise NotImplementedError(name)
