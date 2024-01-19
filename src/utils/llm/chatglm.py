from functools import cache

from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from promplate.llm.base import LLM
from promplate.prompt.chat import Message
from promplate_trace.auto import patch
from pydantic import Field, validate_call
from zhipuai import ZhipuAI
from zhipuai.api_resource.chat.chat import Chat

from ..config import env
from .common import SafeMessage, ensure_safe, ensure_safe_messages
from .dispatch import link_llm


@cache
def get_client():
    return Chat(ZhipuAI(api_key=env.zhipu_api_key))


def ensure_even(prompt: str | list[Message]) -> list[SafeMessage]:
    messages = ensure_safe, ensure_safe_messages(prompt)
    return messages if len(messages) % 2 else [{"role": "user", "content": ""}, *messages]


@link_llm("chatglm")
class ChatGLM(LLM):
    @staticmethod
    @validate_call
    def validate(temperature: float = Field(0.95, gt=0, le=1), top_p: float = Field(0.7, gt=0, lt=1), **_):
        pass

    @staticmethod
    @patch.chat.acomplete
    async def complete(prompt: str | list[Message], /, **config):
        ChatGLM.validate(**config)
        config |= {"model": "chatglm_pro", "messages": ensure_even(prompt)}
        return str((await run_in_threadpool(get_client().completions.create, **config)).choices[0].message.content).removeprefix(" ")  # type: ignore

    @staticmethod
    @patch.chat.agenerate
    async def generate(prompt: str | list[Message], /, **config):
        ChatGLM.validate(**config)
        config |= {"model": "chatglm_pro", "messages": ensure_even(prompt)}
        res = get_client().completions.create(**config, stream=True)
        first_token = True
        async for event in iterate_in_threadpool(res):
            if first_token:
                first_token = False
                yield str(event.choices[0].delta.content).removeprefix(" ")  # type: ignore
            else:
                yield str(event.choices[0].delta.content)  # type: ignore


glm = ChatGLM()
