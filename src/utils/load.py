from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Literal

from promplate.prompt.utils import get_builtins
from typing_extensions import Self

from .helpers import DotTemplate

root = Path("src/templates")


def load_template(stem: str):
    """Load a template based on its stem name.

    Parameters:
    stem (str): The stem name of the template to load.

    Returns:
    DotTemplate: The loaded template object.
    """
    try:
        return DotTemplate.read(glob()[stem])
    except KeyError:
        if (root / stem).is_dir():
            return getattr(components, stem)


def generate_pyi():
    """Generate a .pyi file from the current module for static typing."""
    if __debug__:
        source = Path(__file__)
        target = source.with_suffix(".pyi")
        target.write_text(source.read_text().replace("stem: str", f"stem: Literal{list(glob())}"))


def glob():
    """Return a mapping of file stems to file paths for all files in the root directory.

    Returns:
    dict: A dictionary where keys are stems and values are file paths.
    """
    return {
        path.as_posix().removeprefix(f"{root}/").removesuffix(path.suffix): path
        for path in root.glob("**/*")
        if path.is_file()
    }


if not __debug__ and not TYPE_CHECKING:
    load_template = cache(load_template)
    glob = cache(glob)


class LazyLoader(dict):
    """A dictionary-like object that lazily loads templates on access."""
    path = root

    def __missing__(self, key):
        """Handle requests for missing items by trying to load the template.

        Parameters:
        key (str): The key for the missing item.

        Returns:
        DotTemplate: The loaded template if found; otherwise, raises KeyError.

        Raises:
        KeyError: If the prompt for the given key is not found.
        """
        try:
            return load_template(key)
        except FileNotFoundError:
            raise KeyError(f"Prompt {key} not found")

    def __getattr__(self, stem: str) -> Self | DotTemplate:
        """Get an attribute or lazily load a sub-template based on a directory stem.

        Parameters:
        stem (str): The directory stem to lazily load sub-templates from.

        Returns:
        LazyLoader | DotTemplate: A new LazyLoader if directory, else the template object.
        """
        if (root / stem).is_dir():
            loader = LazyLoader()
            loader.path = self.path / stem
            return loader

        return self[(self.path / stem).relative_to(root).as_posix()]

    if not __debug__:
        __getattr__ = cache(__getattr__)

    def __hash__(self):
        """Compute the hash based on the path of the LazyLoader.

        Returns:
        int: The hash value of the path.
        """
        return hash(self.path)


components = LazyLoader(get_builtins())  # avoid shadowing builtins


Templates = Annotated[Literal.__getitem__(tuple(glob())), str]  # type: ignore
