from collections import ChainMap, defaultdict
from functools import partial
from typing import cast

from box import Box
from promplate import Context, Template


class SilentBox(Box):
    def __str__(self):
        if len(self):
            return super().__str__()
        return ""


SilentBox = partial(SilentBox, default_box=True)  # type: ignore


def get_top_level_box(context: Context):
    return dict(SilentBox(context))


class DotTemplate(Template):
    def __init__(self, text, /, context=None):
        from .load import components

        super().__init__(text, context)
        self.context = cast(Context, ChainMap(get_top_level_box(self.context), components, defaultdict(SilentBox)))

    def render(self, context=None):
        return super().render(context if context is None else get_top_level_box(context))

    async def arender(self, context=None):
        return await super().arender(context if context is None else get_top_level_box(context))
