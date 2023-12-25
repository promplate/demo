from pathlib import Path
from re import sub
from typing import TYPE_CHECKING, Literal

from promplate.prompt.utils import get_builtins
from pydantic import validate_call

from .cache import cache
from .helpers import DotTemplate

root = Path("src/templates")


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


def _load_template(stem: Template) -> DotTemplate:
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
    return _load_template(stem)


if TYPE_CHECKING:

    def load_template(stem: Template) -> DotTemplate:
        ...


class LazyLoader(dict):
    path = root

    def __missing__(self, key):
        try:
            return _load_template(key)
        except FileNotFoundError as e:
            raise KeyError(f"Prompt {key} not found") from e

    if TYPE_CHECKING:

        def __getitem__(self, _: Template) -> DotTemplate:
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
