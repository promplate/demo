"""
This module contains utility functions for working with template files,
including generating stub types, listing available templates, and loading
specific templates into a lazy-loaded structure for efficient access.

Functions:
- generate_pyi: Generates '.pyi' stub files for template type hinting.
- glob: Lists available templates in a predefined root directory.
- load_template: Loads and validates a template given its stem path.

Classes:
- LazyLoader: A lazy-loaded dictionary-like class for accessing templates as attributes.
"""
from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Literal

from promplate.prompt.utils import get_builtins
from pydantic import validate_call

from .cache import cache
from .helpers import DotTemplate

root = Path("src/templates")

"""
Load and return a template given its stem (template name without file extension).
Validates that the template exists and raises an exception if not.

Args:
    stem (Template): The stem path of the template to be loaded.

Returns:
    DotTemplate: The DotTemplate object representing the loaded template.
"""


def generate_pyi():
    if __debug__:
        source = Path(__file__)
        target = source.read_text()

        all_paths = f"Literal{list(glob())}"

        target = sub(r"\nTemplate\s*=\s*.*\n", f"Template = {all_paths}", target)

        source.with_suffix(".pyi").write_text(target)


def glob():
    return {
        path.as_posix().removeprefix(f"{root.as_posix()}/").removesuffix(path.suffix): path
        for path in root.glob("**/*")
        if path.is_file() and path.suffix not in {".py", ".pyc"}
    }


Template = str if TYPE_CHECKING else Literal.__getitem__(tuple(glob()))


@validate_call
def load_template(stem: Template) -> DotTemplate:
    try:
        return DotTemplate.read(glob()[stem])
    except KeyError:
        if (root / stem).is_dir():
            return getattr(components, stem)
        raise


if not __debug__ and not TYPE_CHECKING:
    load_template = cache(load_template)
    glob = cache(glob)


class LazyLoader(dict):
    path = root

    def __missing__(self, key):
        """
        Attempt to load a prompt template with a given key. If the file is not found,
        raise a KeyError with a message indicating the prompt is not found.

        Args:
            key (str): The key representing the template to be loaded.

        Raises:
            KeyError: If the prompt with the given key does not exist.
        """
        try:
            return load_template(key)
        except FileNotFoundError as e:
            raise KeyError(f"Prompt {key} not found") from e

    if TYPE_CHECKING:

        def __getitem__(self, _: Template) -> DotTemplate:
            """
            Retrieve the DotTemplate object associated with the given type-checked key.

            Args:
                _ (Template): The key used to retrieve the template.

            Returns:
                DotTemplate: The requested DotTemplate object.
            """
            ...

    def __getattr__(self, stem: str):
        """
        Dynamically access templates as if they were attributes of a class. If the provided
        stem corresponds to a directory, a new LazyLoader instance for that directory is created.

        Args:
            stem (str): The stem that represents the template or directory.

        Returns:
            Union[DotTemplate, LazyLoader]: Either a DotTemplate object if the stem
            is a file, or a new LazyLoader instance if the stem is a directory.
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
        Generate a hash based on the current path attribute of the LazyLoader.
        This method allows LazyLoader instances to be used in hashed collections like sets.

        Returns:
            int: The hash value of the path attribute.
        """
        return hash(self.path)


components = LazyLoader(get_builtins())  # avoid shadowing builtins
