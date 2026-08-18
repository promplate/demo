from typing import cast

from anthropic import AsyncAnthropic, Omit, omit
from anthropic.types import MessageParam
from promplate.prompt.chat import Message, ensure
from promplate_trace.auto import patch
from promplate_trace.utils import cache

from src.utils import prefill

from ..config import env
from .common import client, ensure_safe
from .dispatch import link_llm


def split(prompt: str | list[Message]) -> tuple[list[MessageParam], Omit | str]:
    messages = ensure(prompt)
    if messages[0]["role"] == "system":
        return cast(list[MessageParam], ensure_safe(messages[1:])), messages[0]["content"]
    return cast(list[MessageParam], ensure_safe(messages)), omit


@cache
def get_anthropic():
    return AsyncAnthropic(http_client=client, base_url=env.anthropic_base_url or None, api_key=env.anthropic_api_key)


@prefill.patch_async_complete
async def complete(prompt: str | list[Message], /, **config):
    messages, system_message = split(prompt)
    res = await get_anthropic().messages.create(messages=messages, system=system_message, max_tokens=4096, **config)
    return res.content[0].text


@prefill.patch_async_generate
async def generate(prompt: str | list[Message], /, **config):
    messages, system_message = split(prompt)
    async with await get_anthropic().messages.create(
        messages=messages, system=system_message, max_tokens=4096, **config, stream=True
    ) as stream:
        async for event in stream:
            if event.type == "content_block_delta":
                yield getattr(event.delta, "text", "")


@link_llm("claude")
class Anthropic:
    complete = staticmethod(patch.chat.acomplete(complete))
    generate = staticmethod(patch.chat.agenerate(generate))


anthropic = Anthropic()


class RawAnthropic:
    complete = staticmethod(patch.text.acomplete(complete))
    generate = staticmethod(patch.text.agenerate(generate))


raw_anthropic = RawAnthropic()
