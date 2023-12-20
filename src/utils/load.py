"""
This module defines functionality for loading and handling template components
for use with the promplate system, as well as utilities for file generation.
"""

from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Annotated, Literal

from promplate.prompt.utils import get_builtins

from .cache import cache
from .helpers import DotTemplate

root = Path("src/templates")

Component = str


def load_template(stem: Component) -> DotTemplate:
    """
    Load a template component based on the provided identifier.

    Args:
        stem (Component): The identifier for the template to be loaded.

    Returns:
        DotTemplate: The loaded template object.

    Raises:
        KeyError: If the specified component is not found.
    """
    try:
        return DotTemplate.read(glob()[stem])
    except KeyError:
        if (root / stem).is_dir():
            return getattr(components, stem)
        raise


def generate_pyi():
    """
    Generate a .pyi file containing type hints for the current module.
    This reflects the available components within the module for type checking.
    """
    if __debug__:
        source = Path(__file__)
        target = source.read_text()

        all_paths = f"Literal{list(glob())}"

        target = sub(r"\nComponent\s*=\s*.*?\n", f"\nComponent = {all_paths}\n", target)
        target = sub(r"\nTemplate\s*=\s*.*\n", f"\nTemplate = {all_paths}\n", target)

        source.with_suffix(".pyi").write_text(target)


def glob():
    """
    Glob the file paths for all components available within the templates directory.

    Returns:
        dict: A dictionary mapping component identifiers to their respective file paths.
    """
    return {
        path.as_posix().removeprefix(f"{root.as_posix()}/").removesuffix(path.suffix): path
        for path in root.glob("**/*")
        if path.is_file() and path.suffix not in {".py", ".pyc"}
    }

if not __debug__ and not TYPE_CHECKING:
    load_template = cache(load_template)
    glob = cache(glob)


class LazyLoader(dict):
    """
    A dictionary-like class that provides lazy loading functionality for template components.

    This handles the dynamic retrieval of templates upon access, allowing components to
    be loaded only when needed from the 'templates' directory.
    """

    path = root

    def __missing__(self, key):
        try:
            return load_template(key)
        except FileNotFoundError as e:
            raise KeyError(f"Prompt {key} not found") from e

    if TYPE_CHECKING:
        def __getitem__(self, _: Component) -> DotTemplate:
            ...

    def __getattr__(self, stem: str):
        if (root / stem).is_dir():
            loader = LazyLoader()
            loader.path = self.path / stem
            return loader
        return self[(self.path / stem).relative_to(root).as_posix()]

    if not __debug__:
        __getattr__ = cache(__getattr__)

    def __hash__(self):  # type: ignore
        return hash(self.path)

components = LazyLoader(get_builtins())  # avoid shadowing builtins

Template = Annotated[Literal.__getitem__(tuple(glob())), str]  # type: ignore
