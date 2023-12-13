from box import Box
from promplate import Template
from promplate.prompt.utils import get_builtins


class SilentBox(Box):
    """This class extends the Box class and overrides the __str__ method to return a string representation only when the box is not empty."""
    def __str__(self):
        if len(self):
            return super().__str__()
        return ""


class DotTemplate(Template):
    def render(self, context: dict):
        context = SilentBox(default_box=True) | get_builtins() | context
        return super().render(context)
