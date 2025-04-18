from functools import cached_property

from promplate import Callback
from promplate import Node as N
from promplate.chain.node import ChainContext
from promplate.prompt.utils import AutoNaming
from promplate_trace.auto import patch


@patch.node
class Node(N, AutoNaming):
    def __init__(self, template, partial_context=None, *args, **config):
        super().__init__(template, partial_context, *args, **config)

        context_type = partial_context.__class__
        if issubclass(context_type, ChainContext) and context_type is not ChainContext:
            self.add_callbacks(Callback(on_enter=lambda _, context, config: (context_type(context), config)))


class KeyAsAttr(AutoNaming):
    def __init__(self, initial=None):
        self.initial = initial

    @cached_property
    def fallback_name(self):
        return str(id(self))  # this should not happen, just in case

    def __get__(self, obj: dict | None, cls):
        if obj is None:
            return self
        return obj.get(self.name, self.initial)

    def __set__(self, obj: dict, value):
        obj[self.name] = value

    def __delete__(self, obj: dict):
        del obj[self.name]
