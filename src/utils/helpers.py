"""This file contains utility classes and functions for Promplate template rendering.

It defines a SilentBox class for silent string representation of Box instances, and a DotTemplate class which extends
Promplate's Template class with additional context processing using ChainMap.
"""

from collections import ChainMap
from typing import cast

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
        """Constructor that initializes the DotTemplate class with given text and optional context.

        This method imports components from the 'load' module and creates a ChainMap combining the top-level
        box of the context and the components for advanced template rendering.

        Args:
            text (str): Template text to be used for rendering.
            context (Optional[Context]): Context dictionary or mapping to provide additional data for rendering.

        Returns:
            None
        """
        from .load import components

        super().__init__(text, context)
        self.context = cast(Context, ChainMap(get_top_level_box(self.context), components))

    def render(self, context=None):
        """Render the template with the specified context.

        If no context is provided, uses the top-level box of the saved context. This function overrides the standard
        render method to utilize ChainMap for context management.

        Args:
            context (Optional[Context]): The context to render the template with. If None, default is used.

        Returns:
            str: The rendered template text.
        """
        return super().render(context if context is None else get_top_level_box(context))

    async def arender(self, context=None):
        return await super().arender(context if context is None else get_top_level_box(context))
