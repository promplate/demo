from typing import Awaitable, Callable, overload

from promplate.chain.node import ChainContext, Context
from promplate.chain.node import Node as N
from promplate.llm.base import LLM
from promplate.prompt.template import Template

type _MaybeContext = Context | None

type _Return = _MaybeContext | Awaitable[_Return]

type _Process[C: ChainContext, T: _Return] = Callable[[C], T]

class Node[C: ChainContext = ChainContext](N):
    @overload
    def __new__(cls, template: Template | str, partial_context: C, llm: LLM | None = ..., **config) -> Node[C]: ...
    @overload
    def __new__(cls, template: Template | str, partial_context: _MaybeContext = ..., llm: LLM | None = ..., **config) -> Node: ...
    def pre_process[T: _Return](self, process: Callable[[C], T]) -> Callable[[C], T]: ...  # type: ignore
    def mid_process[T: _Return](self, process: Callable[[C], T]) -> Callable[[C], T]: ...  # type: ignore
    def end_process[T: _Return](self, process: Callable[[C], T]) -> Callable[[C], T]: ...  # type: ignore
