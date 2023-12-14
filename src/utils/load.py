from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Literal

from promplate.prompt.utils import get_builtins
from typing_extensions import Self

from .helpers import DotTemplate

root = Path("src/templates")


def load_template(stem: str):
    """Load a template given the stem of the template file.

    Args:
        stem (str): The stem (base name without suffix) of the template file.

    Returns:
        DotTemplate | LazyLoader: The loaded template as a DotTemplate object or LazyLoader if the stem corresponds to a directory.
    """
    try:
        return DotTemplate.read(glob()[stem])
    except KeyError:
        if (root / stem).is_dir():
            return getattr(components, stem)


def generate_pyi():
    if __debug__:
        source = Path(__file__)
        target = source.with_suffix(".pyi")
        target.write_text(source.read_text().replace("stem: str", f"stem: Literal{list(glob())}"))


def glob():
    return {
        path.as_posix().removeprefix(f"{root}/").removesuffix(path.suffix): path
        for path in root.glob("**/*")
        if path.is_file()
    }


if not __debug__ and not TYPE_CHECKING:
    load_template = cache(load_template)
    glob = cache(glob)


class LazyLoader(dict):
    path = root

    def __missing__(self, key):
        try:
            return load_template(key)
        except FileNotFoundError:
            raise KeyError(f"Prompt {key} not found")

    def __getattr__(self, stem: str) -> Self | DotTemplate:
        """Get an attribute representing a sub-directory or a template.

        Args:
            stem (str): The stem (base name without suffix) of the directory or template.

        Returns:
            Self | DotTemplate: A new LazyLoader instance if stem is a directory, or a DotTemplate object if stem is a template file.
        """
        if (root / stem).is_dir():
            loader = LazyLoader()
            loader.path = self.path / stem
            return loader

        return self[(self.path / stem).relative_to(root).as_posix()]

    if not __debug__:
        __getattr__ = cache(__getattr__)

    def __hash__(self):
        return hash(self.path)


components = LazyLoader(get_builtins())  # avoid shadowing builtins


Templates = Annotated[Literal.__getitem__(tuple(glob())), str]  # type: ignore
