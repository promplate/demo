from collections import ChainMap

from box import Box
from promplate import Context, Template


class SilentBox(Box):
    def __str__(self):
        if len(self):
            return super().__str__()
        return ""


def get_top_level_box(context: Context):
    """
    Takes a Context object as input and returns a dictionary with a top-level box representation.

    This function extracts the top-level context information and wraps it inside a dictionary,
    using a SilentBox which suppresses empty strings when coerced to a string representation.

    Args:
        context (Context): The input context from which to generate the top-level box.

    Returns:
        dict: A dictionary representation of the top-level box.
    """
    return dict(SilentBox(context, default_box=True))


class DotTemplate(Template):
    """
    Subclass of the Template class for parsing text templates with context represented as dot notation.

    This class enhances the template rendering capabilities of the base Template class by
    supporting dot notation to access context values, providing more intuitive navigation
    within the context object.

    Methods:
        __init__(text, /, context=None): Initialize the DotTemplate instance with the
            given text and optional context.
        render(context=None): Render the template using the given context (if provided) or
            the stored context.
        arender(context=None): Asynchronously render the template similar to the render method.
    """
    
    def __init__(self, text, /, context=None):
        from .load import components

        super().__init__(text, context)
        self.context = ChainMap(get_top_level_box(self.context), components)

    def render(self, context=None):
        return super().render(context if context is None else get_top_level_box(context))

    async def arender(self, context=None):
        return await super().arender(context if context is None else get_top_level_box(context))
