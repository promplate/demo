from box import Box
from promplate import Template
from promplate.prompt.utils import get_builtins


class SilentBox(Box):
    def __str__(self):
        if len(self):
            return super().__str__()
        return ""


class DotTemplate(Template):
    def render(self, context=None):
        """
        Render the template with the given context.

        This function merges the provided context with the built-in context and
        the default context, then renders the template using the combined context.
        """
        context = SilentBox(default_box=True) | get_builtins() | (context or {})
        return super().render(context)

    async def arender(self, context=None):
        """
        Asynchronously render the template with the given context.

        This function is an asynchronous version of `render` and performs the
        same merging of the provided context with the built-in context and
        the default context before rendering the template.
        """
        context = SilentBox(default_box=True) | get_builtins() | (context or {})
        return await super().arender(context)
