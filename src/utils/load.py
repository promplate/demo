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
        """
        Special method called by Python when a key is not found in the dictionary.

        This function attempts to load the template with the given key. If the template
        is not found, it raises a FileNotFoundError indicating the prompt cannot be
        located.
        """
        return load_template(key) if key in self else raise KeyError(f"Prompt {key} not found")


components = LazyLoader(get_builtins())  # avoid shadowing builtins


Templates = Annotated[Literal.__getitem__(tuple((i.stem for i in root.glob("*.j2")))), str]  # type: ignore
