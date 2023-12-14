from collections import ChainMap

from box import Box
from promplate import Context, Template


class SilentBox(Box):
    def __str__(self):
        if len(self):
            return super().__str__()
        return ""


def get_top_level_box(context: Context):
    return dict(SilentBox(context, default_box=True))


class DotTemplate(Template):
    def __init__(self, text, /, context=None):
        from .load import components

        super().__init__(text, context)
        self.context = ChainMap(get_top_level_box(self.context), components)

    def render(self, context=None):
        return super().render(context if context is None else get_top_level_box(context))

    async def arender(self, context=None):
        return await super().arender(context if context is None else get_top_level_box(context))
