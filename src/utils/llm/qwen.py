from typing import Generator, cast

from dashscope import Generation
from dashscope.api_entities.dashscope_response import GenerationResponse
from fastapi import HTTPException
from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from promplate.llm.base import LLM
from promplate.prompt.chat import Message, ensure
from promplate_trace.auto import patch

from src.utils.llm.dispatch import link_llm


@link_llm("qwen")
class Qwen(LLM):
    @staticmethod
    @patch.chat.acomplete
    async def complete(prompt: str | list[Message], /, **config):
        res = cast(
            GenerationResponse,
            await run_in_threadpool(Generation.call, messages=cast(list, ensure(prompt)), **config),
        )
        if res.status_code == 200:
            return res.output.text

        print(res)
        raise HTTPException(res.status_code, res.message)

    @staticmethod
    @patch.chat.agenerate
    async def generate(messages: str | list[Message], /, **config):
        config |= {"stream": True, "incremental_output": True}

        generator = Generation.call(messages=cast(list, ensure(messages)), **config)

        async for res in iterate_in_threadpool(cast(Generator[GenerationResponse, None, None], generator)):
            if res.status_code != 200:
                print(res)
                continue

            yield res.output.text


qwen = Qwen()
