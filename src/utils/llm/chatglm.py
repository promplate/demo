from typing import cast

import zhipuai
from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from promplate.llm.base import LLM
from promplate.prompt.chat import Message, ensure
from promplate_trace.auto import patch
from pydantic import Field, validate_call

from ..config import env

zhipuai.api_key = env.zhipu_api_key


def patch_prompt(prompt: str | list[Message]):
    messages = ensure(prompt)
    for i in messages:
        cast(dict, i).pop("name", None)
        if i["role"] == "system":
            i["role"] = "user"
    return messages


class ChatGLM(LLM):
    """A language model designed specifically for chat applications.

    This class provides methods to validate configuration parameters for language model generation,
    to complete a given prompt and to generate responses in a conversational manner. It leverages
    the OpenAI Codex model to produce human-like text based on the provided context.

    Methods:
        validate(temperature, top_p, **_): Validates the configuration parameters for the chat generation.
        complete(prompt, /, **config): Given a prompt, returns a complete chat response.
        generate(prompt, /, **config): Streams a generated response to a given prompt in real-time.
    """
    @staticmethod
    @validate_call
    def validate(temperature: float = Field(0.95, gt=0, le=1), top_p: float = Field(0.7, gt=0, lt=1), **_):
        pass

    @staticmethod
    @patch.chat.acomplete
    async def complete(prompt: str | list[Message], /, **config):
        ChatGLM.validate(**config)
        messages = patch_prompt(prompt)
        return (await run_in_threadpool(zhipuai.model_api.invoke, model="chatglm_pro", prompt=messages, **config))["data"]["choices"][0]["content"]  # type: ignore

    @staticmethod
    @patch.chat.agenerate
    async def generate(prompt: str | list[Message], /, **config):
        ChatGLM.validate(**config)
        messages = patch_prompt(prompt)
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
