from box import Box
from promplate import Template
from promplate.prompt.utils import get_builtins


class SilentBox(Box):
    def __str__(self):
        if len(self):
            return super().__str__()
        return ""


class DotTemplate(Template):
    def render(self, context: dict):
        context = SilentBox(default_box=True) | get_builtins() | context
        return super().render(context)
