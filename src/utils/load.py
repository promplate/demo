from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Literal

from promplate.prompt.utils import get_builtins
from typing_extensions import Self

from .helpers import DotTemplate

root = Path("src/templates")


def load_template(stem: str):
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
    def __load_template__(self, stem: str) -> DotTemplate:
        return self[(self.path / stem).relative_to(root).as_posix()]

    def __load_directory__(self, stem: str) -> Self | None:
        if (root / stem).is_dir():
            loader = LazyLoader()
            loader.path = self.path / stem
            return loader

        return None
    path = root

    def __missing__(self, key):
        try:
            return load_template(key)
        except FileNotFoundError:
            raise KeyError(f"Prompt {key} not found")

    def __getattr__(self, stem: str) -> Self | DotTemplate:
        directory_loader = self.__load_directory__(stem)
        if directory_loader is not None:
            return directory_loader
        return self.__load_template__(stem)

    if not __debug__:
        __getattr__ = cache(__getattr__)

    def __hash__(self):
        return hash(self.path)


components = LazyLoader(get_builtins())  # avoid shadowing builtins


Templates = Annotated[Literal.__getitem__(tuple(glob())), str]  # type: ignore
