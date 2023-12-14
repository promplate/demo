from functools import cache
from pathlib import Path
from typing import Annotated, Literal

from promplate.prompt.utils import get_builtins

from .helpers import DotTemplate

root = Path("src/templates")


def load_template(stem: str):
    """
    Load a template by stem name and return a DotTemplate object.

    This function reads the template file corresponding to the provided stem name,
    and creates a DotTemplate object which can be used to render the template with
    context.

    Args:
        stem (str): The stem name of the template to load.

    Returns:
        DotTemplate: A DotTemplate object created from the loaded template file.
    """
    return DotTemplate.read(glob()[stem])


def glob():
    """
    Retrieve a mapping of template stem names to their file paths.

    This function searches for all template files in the 'src/templates' directory
    and returns a dictionary where the key is the stem name of the template file
    and the value is the path to that file.

    Returns:
        dict: A dictionary mapping stem names to Path objects.
    """
    return {path.stem: path for path in root.glob("**/*")}


if not __debug__:
    load_template = cache(load_template)
    glob = cache(glob)


class LazyLoader(dict):
    def __missing__(self, key):
        try:
            return load_template(key)
        except FileNotFoundError:
            raise KeyError(f"Prompt {key} not found")


components = LazyLoader(get_builtins())  # avoid shadowing builtins


Templates = Annotated[Literal.__getitem__(tuple(glob())), str]  # type: ignore
