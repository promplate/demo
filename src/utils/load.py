from functools import cache
from pathlib import Path
from typing import Annotated, Literal

from promplate.prompt.utils import get_builtins

from .helpers import DotTemplate

root = Path("src/templates")


def load_template(path: str):
    return DotTemplate.read(root / f"{path}.j2")


if not __debug__:
    load_template = cache(load_template)


class LazyLoader(dict):
    def __missing__(self, key):
        try:
            return load_template(key)
        except FileNotFoundError:
            raise KeyError(f"Prompt {key} not found")


components = LazyLoader(get_builtins())  # avoid shadowing builtins


Templates = Annotated[Literal.__getitem__(tuple((i.stem for i in root.glob("*.j2")))), str]  # type: ignore
