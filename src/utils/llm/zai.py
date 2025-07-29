from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from promplate.prompt.chat import Message
from promplate_trace.auto import patch
from pydantic import Field, validate_call
from zai import ZhipuAiClient

from ..config import env
from .common import SafeMessage, ensure_safe
from .dispatch import link_llm

sdk = ZhipuAiClient(base_url=env.zhipu_base_url or None, api_key=env.zhipu_api_key)


def ensure_even(prompt: str | list[Message]) -> list[SafeMessage]:
    messages = ensure_safe(prompt)
    return messages if len(messages) % 2 else [{"role": "user", "content": ""}, *messages]


@link_llm("glm-")
class ZhipuAI:
    @staticmethod
    @validate_call
    def validate(temperature: float = Field(0.95, gt=0, le=1), top_p: float = Field(0.7, gt=0, lt=1), **_): ...

    @staticmethod
    @patch.chat.acomplete
    async def complete(prompt: str | list[Message], /, **config):
        __class__.validate(**config)
        config |= {"messages": ensure_even(prompt), "thinking": {"type": "disabled"}}
        return str((await run_in_threadpool(sdk.chat.completions.create, **config)).choices[0].message.content).removeprefix(" ")  # type: ignore

    @staticmethod
    @patch.chat.agenerate
    async def generate(prompt: str | list[Message], /, **config):
        __class__.validate(**config)
        config |= {"messages": ensure_even(prompt), "thinking": {"type": "disabled"}}
        res = sdk.chat.completions.create(**config, stream=True)
        first_token = True
        async for event in iterate_in_threadpool(res):
            if first_token:
                first_token = False
                yield str(event.choices[0].delta.content).removeprefix(" ")  # type: ignore
            else:
                yield str(event.choices[0].delta.content)  # type: ignore


zai = ZhipuAI()
