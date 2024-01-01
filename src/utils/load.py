"""
This file contains utility functions for loading templates and managing lazy loading of components.

It handles template file path resolution, template content loading, and provides mechanisms to
optimize I/O operations through caching and lazy loading patterns.

Functions:
- generate_pyi: Generates .pyi files for better type inference.
- glob: Returns a dictionary of template paths.
- _load_template: Helper function to load a template by stem.
- load_template: Public function to load a template.

Classes:
- LazyLoader: Implements a lazy loading pattern for template components.Extends functionality to a dictionary with loading mechanisms.
"""

from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Literal, TypeAlias

from promplate.prompt.utils import get_builtins
from pydantic import validate_call

from .cache import cache
from .helpers import DotTemplate

root = Path("src/templates")


def generate_pyi():
    """Generates a .pyi file for better type inference by including the paths of all template files.

    This function will create a .pyi file with updated type hints that match the current template files
    available when running in debug mode. When not in debug mode, this function will have no effect.
    """
    if __debug__:
        source = Path(__file__)
        target = source.read_text()

        all_paths = f"Literal{list(glob())}"

        target = sub(r"\nTemplate:\sTypeAlias\s*=\s*.*\n", f"Template = {all_paths}", target)

        source.with_suffix(".pyi").write_text(target)


def glob():
    """Returns a dictionary mapping template stems to their respective paths.

    This function traverses the defined root directory and compiles a dictionary that
    maps the relative paths of templates (excluding the '.py' and '.pyc' suffix) to their corresponding Path objects.
    """
    return {
        path.as_posix().removeprefix(f"{root.as_posix()}/").removesuffix(path.suffix): path
        for path in root.glob("**/*")
        if path.is_file() and path.suffix not in {".py", ".pyc"}
    }


Template: TypeAlias = str if TYPE_CHECKING else Literal.__getitem__(tuple(glob()))  # type: ignore


def _load_template(stem: Template) -> DotTemplate:
    """Loads a template file by its stem name and returns a DotTemplate object.

    Args:
        stem: The stem of the template file to load.

    Returns:
        A DotTemplate object instantiated with the content from the template file.

    Raises:
        KeyError: If the template does not exist or the stem corresponds to a directory.
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
    """Public function that loads a template by its stem and returns the content.

    Args:
        stem: The stem of the template file to load.

    Returns:
        The content of the template, typically used for dynamic text generation.
    """
    return _load_template(stem)


if TYPE_CHECKING:

    def load_template(stem: Template) -> DotTemplate:
        ...


class LazyLoader(dict):
    """A dict subclass that lazily loads template components on demand.

    This class is a lazy loader for template components, which allows for components to be
    loaded only when they are accessed. It extends the dictionary class and overrides methods
    to provide lazy loading functionality.

    Attributes:
        path (Path): The root path from which components will be loaded.
    """
    path = root

    def __missing__(self, key):
        """Override dict's __missing__ to provide a handler for missing keys.

        This method attempts to load a template with the given key as the stem. If the file is not found,
        a KeyError is raised instead of the default behavior.

        Args:
            key: The key that is not found in the dictionary.

        Returns:
            The loaded template corresponding to the key.

        Raises:
            KeyError: If the prompt represented by key is not found.
        """
        try:
            return _load_template(key)
        except FileNotFoundError as e:
            raise KeyError(f"Prompt {key} not found") from e

    if TYPE_CHECKING:

        def __getitem__(self, _: Template) -> DotTemplate:
        """Specialized __getitem__ for type checking and inference.

        This method is only relevant during type checking to provide better type inference for template components.
        In runtime, it behaves the same as a regular dictionary __getitem__.

        Args:
            _: Ignored. Present only to satisfy the method signature.

        Returns:
            An instance of DotTemplate, representing a template component.
        """
            ...

    def __getattr__(self, stem: str):
        """Loads a template component if accessed as an attribute.

        If the attribute corresponds to a directory, a new LazyLoader instance is created for that subpath.
        Otherwise, it tries to fetch the component directly.

        Args:
            stem: The stem to resolve as a path within the templates directory.

        Returns:
            A LazyLoader instance for subdirectories or the loaded template component.

        Raises:
            KeyError: If the template component cannot be resolved or does not exist.
        """
        if (root / stem).is_dir():
            loader = LazyLoader()
            loader.path = self.path / stem
            return loader

        return self[(self.path / stem).relative_to(root).as_posix()]

    if not __debug__:
        __getattr__ = cache(__getattr__)

    def __hash__(self):  # type: ignore
        """Provides a hash based on the path attribute.

        This custom __hash__ is implemented to allow instances of LazyLoader to be used as keys in dictionaries
        or to be included in sets. It uses the path attribute for hash computation.

        Returns:
            An integer hash of the path.
        """
        return hash(self.path)


components = LazyLoader(get_builtins())  # avoid shadowing builtins
