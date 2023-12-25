import zhipuai
from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from promplate.llm.base import LLM
from promplate.prompt.chat import Message
from promplate_trace.auto import patch
from pydantic import Field, validate_call

from ..config import env
from .common import SafeMessage, ensure_safe
from .dispatch import link_llm

zhipuai.api_key = env.zhipu_api_key


def ensure_even(prompt: str | list[Message]) -> list[SafeMessage]:
    messages = ensure_safe(prompt)
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
        messages = ensure_even(prompt)
        config |= {"model": "chatglm_pro", "prompt": messages}
        return (await run_in_threadpool(zhipuai.model_api.invoke, **config))["data"]["choices"][0]["content"]  # type: ignore

    @staticmethod
    @patch.chat.agenerate
    async def generate(prompt: str | list[Message], /, **config):
        ChatGLM.validate(**config)
        messages = ensure_even(prompt)
        config |= {"model": "chatglm_pro", "prompt": messages}
        res = zhipuai.model_api.sse_invoke(**config)

        first_token = True

        async for event in iterate_in_threadpool(res.events()):
            if event.event in {"add", "finish"}:
                if first_token:
                    first_token = False
                    yield event.data.lstrip()
                else:
                    yield event.data
            elif event.event in {"error", "interrupted"}:
                print(event.data)


glm = ChatGLM()
