from typing import cast
from asyncio import stream

import zhipuai
from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from promplate.llm.base import LLM
from promplate.prompt.chat import Message, ensure
from promplate_trace.auto import patch
from pydantic import Field, validate_call

from ..config import env
from .dispatch import link_llm

zhipuai.api_key = env.zhipu_api_key


def patch_prompt(prompt: str | list[Message]):
    messages = ensure(prompt)
    for i in messages:
        cast(dict, i).pop("name", None)
        if i["role"] == "system":
            i["role"] = "user"
    return messages


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
        messages = patch_prompt(prompt)
        return str((await run_in_threadpool(zhipuai.model_api.invoke, model="chatglm_pro", prompt=messages, **config))["data"]["choices"][0]["content"])  # type: ignore

    @staticmethod
    @patch.chat.agenerate
    async def generate(prompt: str | list[Message], /, **config):
        ChatGLM.validate(**config)
        messages = patch_prompt(prompt)
        config |= {"model": "chatglm_pro", "prompt": messages}
        res = zhipuai.model_api.sse_invoke(**config)

        first_token = True

        async for event in stream.iterate(iterate_in_threadpool(res.events())):
            if event.event in {"add", "finish"}:
                if first_token:
                    first_token = False
                    yield event.data.lstrip()
                else:
                    yield event.data
            elif event.event in {"error", "interrupted"}:
                print(event.data)


glm = ChatGLM()
