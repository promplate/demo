"""
This file contains utilities for loading templates and generating type hinting files.
It provides functionality for template management within the codebase.
"""
from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Literal

from promplate.prompt.utils import get_builtins
from pydantic import validate_call

from .cache import cache
from .helpers import DotTemplate

root = Path("src/templates")


def generate_pyi():
    """
    Generate a .pyi file for type hinting.

    This function only runs in debug mode.
    """
    if __debug__:
        source = Path(__file__)
        target = source.read_text()

        all_paths = f"Literal{list(glob())}"

        target = sub(r"\nTemplate\s*=\s*.*\n", f"Template = {all_paths}", target)

        source.with_suffix(".pyi").write_text(target)


def glob():
    """
    Return a dictionary mapping template names to their file paths.

    Returns:
        dict: A mapping from template names to file paths.
    """
    return {
        path.as_posix().removeprefix(f"{root.as_posix()}/").removesuffix(path.suffix): path
        for path in root.glob("**/*")
        if path.is_file() and path.suffix not in {".py", ".pyc"}
    }


Template = str if TYPE_CHECKING else Literal.__getitem__(tuple(glob()))


def _load_template(stem: Template) -> DotTemplate:
    """
    Load a template based on the given stem.

    Args:
        stem (Template): The stem of the template to load.

    Returns:
        DotTemplate: The loaded template.

    Raises:
        KeyError: If the template with the given stem is not found.
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
    Load a template based on the given stem.

    Args:
        stem (Template): The stem of the template to load.

    Returns:
        DotTemplate: The loaded template.
    """
    return _load_template(stem)


class LazyLoader(dict):
    """
    Lazily load templates as they are requested.

    This class is a custom dictionary that facilitates lazy loading of templates. It allows
    templates to be loaded on-demand, which can provide performance benefits by not
    loading all templates at startup.
    """

    path = root

    def __missing__(self, key):
        """
        LazyLoader method that gets called when a key is not present.

        It attempts to load the template associated with the key, raising a KeyError if the template does not exist.

        Args:
            key (str): The key for which the template should be loaded.

        Raises:
            KeyError: If the template cannot be found with the given key.
        """
        try:
            return _load_template(key)
        except FileNotFoundError as e:
            raise KeyError(f"Prompt {key} not found") from e

    if TYPE_CHECKING:

        def __getitem__(self, _: Template) -> DotTemplate:
            ...

    def __getattr__(self, stem: str):
        """
        Get an attribute using dot notation or create a new LazyLoader for it if it represents a subdirectory of templates.

        Args:
            stem (str): The attribute name corresponding to the template stem or subdirectory.

        Returns:
            DotTemplate or LazyLoader: A DotTemplate if the stem represents a template, or
            a new LazyLoader if the stem represents a subdirectory.
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
        Generate a hash based on the path of this LazyLoader.

        Returns:
            int: The hash code for this LazyLoader instance.
        """
        return hash(self.path)


components = LazyLoader(get_builtins())  # avoid shadowing builtins
