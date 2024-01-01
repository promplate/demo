"""Utility functions for loading templates and handling template paths."""

from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Literal, TypeAlias

from promplate.prompt.utils import get_builtins
from pydantic import validate_call

from .cache import cache
from .helpers import DotTemplate

root = Path("src/templates")


def generate_pyi():
    """
    Generates a .pyi file for type hinting purposes.
    """
    if __debug__:
        source = Path(__file__)
        target = source.read_text()

        all_paths = f"Literal{list(glob())}"

        target = sub(r"\nTemplate:\sTypeAlias\s*=\s*.*\n", f"Template = {all_paths}", target)

        source.with_suffix(".pyi").write_text(target)


def glob():
    """
    Returns a dictionary mapping template names to their file paths.
    """
    return {
        path.as_posix().removeprefix(f"{root.as_posix()}/").removesuffix(path.suffix): path
        for path in root.glob("**/*")
        if path.is_file() and path.suffix not in {".py", ".pyc"}
    }


Template: TypeAlias = str if TYPE_CHECKING else Literal.__getitem__(tuple(glob()))  # type: ignore


def _load_template(stem: Template) -> DotTemplate:
    """
    Loads a template given its name, and raises a KeyError exception if the template cannot be found.
    """
    try:
        return DotTemplate.read(glob()[stem])
    except KeyError:
        if (root / stem).is_dir():
            return getattr(components, stem)
        raise


if not __debug__ and not TYPE_CHECKING:
    _load_template = cache(_load_template)
    glob = cache(glob)


@validate_call
def load_template(stem: Template):
    """
    Wrapper function for _load_template() that validates the input
    before passing it to _load_template().
    """
    return _load_template(stem)


if TYPE_CHECKING:

    def load_template(stem: Template) -> DotTemplate:
        ...


class LazyLoader(dict):
    """
    Dictionary-like object that lazily loads templates when they are accessed.
    """
    path = root

    def __missing__(self, key):
        """
        Called by __getitem__ for missing key; tries to load the template,
        and raises KeyError if the template is not found.
        """
        try:
            return _load_template(key)
        except FileNotFoundError as e:
            raise KeyError(f"Prompt {key} not found") from e

    if TYPE_CHECKING:

        def __getitem__(self, _: Template) -> DotTemplate:
            """
            Returns the DotTemplate object corresponding to the template key.
            """
            ...

    def __getattr__(self, stem: str):
        """
        Returns the value for the attribute named stem if it exists,
        otherwise loads the template named stem.
        """
        if (root / stem).is_dir():
            loader = LazyLoader()
            loader.path = self.path / stem
            return loader

        return self[(self.path / stem).relative_to(root).as_posix()]

    if not __debug__:
        __getattr__ = cache(__getattr__)

    def __hash__(self):  # type: ignore
        """
        Returns the hash value of the LazyLoader based on the path attribute.
        """
        return hash(self.path)


components = LazyLoader(get_builtins())  # avoid shadowing builtins
