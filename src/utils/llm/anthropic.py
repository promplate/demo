from typing import cast

from anthropic import AsyncAnthropic
from anthropic._types import NOT_GIVEN, NotGivenOr
from anthropic.types.beta import MessageParam
from promplate.llm.base import LLM
from promplate.prompt.chat import Message, ensure
from promplate_trace.auto import patch
from promplate_trace.utils import cache

from .common import client, ensure_safe
from .dispatch import link_llm


def split(prompt: str | list[Message]) -> tuple[list[MessageParam], NotGivenOr[str]]:
    messages = ensure(prompt)
    if messages[0]["role"] == "system":
        return cast(list[MessageParam], ensure_safe(messages[1:])), messages[0]["content"]
    return cast(list[MessageParam], ensure_safe(messages)), NOT_GIVEN


@cache
def get_anthropic():
    return AsyncAnthropic(http_client=client)


async def complete(prompt: str | list[Message], /, **config):
    """
    Create a message with the anthropic API and return the text of the response.

    Args:
        prompt (str | list[Message]): The input prompt to send to the API, may consist of strings or structured messages.
        config (dict): Configuration parameters for the API request.

    Returns:
        str: The text of the response from the API.
    """
    messages, system_message = split(prompt)
    res = await get_anthropic().beta.messages.create(messages=messages, system=system_message, max_tokens=4096, **config)
    return res.content[0].text


async def generate(prompt: str | list[Message], /, **config):
    """
    Create a message with the anthropic API and emit the content block delta from the stream of events.

    Args:
        prompt (str | list[Message]): The input prompt to send to the API, may consist of strings or structured messages.
        config (dict): Configuration parameters for the API request.

    Yields:
        str: The content block delta from the stream of events.
    """
    messages, system_message = split(prompt)
    async with await get_anthropic().beta.messages.create(
        messages=messages, system=system_message, max_tokens=4096, **config, stream=True
    ) as stream:
        async for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text


@link_llm("claude")
class Anthropic(LLM):
    complete = staticmethod(patch.chat.acomplete(complete))
    generate = staticmethod(patch.chat.agenerate(generate))


anthropic = Anthropic()


class RawAnthropic(LLM):
    complete = staticmethod(patch.text.acomplete(complete))
    generate = staticmethod(patch.text.agenerate(generate))


raw_anthropic = RawAnthropic()
