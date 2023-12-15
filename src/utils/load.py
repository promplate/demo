from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Annotated, Literal

from promplate.prompt.utils import get_builtins

from .cache import cache
from .helpers import DotTemplate

root = Path("src/templates")


Component = str


def load_template(stem: Component) -> DotTemplate:
    try:
        return DotTemplate.read(glob()[stem])
    except KeyError:
        if (root / stem).is_dir():
            return getattr(components, stem)
        raise


def generate_pyi():
    if __debug__:
        source = Path(__file__)
        target = source.read_text()

        all_paths = f"Literal{list(glob())}"

        target = sub(r"\nComponent\s*=\s*.*?\n", f"Component = {all_paths}", target)
        target = sub(r"\nTemplate\s*=\s*.*\n", f"Template = {all_paths}", target)

        source.with_suffix(".pyi").write_text(target)


def glob():
    return {
        path.as_posix().removeprefix(f"{root.as_posix()}/").removesuffix(path.suffix): path
        for path in root.glob("**/*")
        if path.is_file() and path.suffix not in {".py", ".pyc"}
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
