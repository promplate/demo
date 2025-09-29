from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate.prompt.chat import ensure
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm

complete = patch.chat.acomplete(AsyncChatComplete(http_client=client, base_url=env.gemini_base_url, api_key=env.gemini_api_key))
generate = patch.chat.agenerate(AsyncChatGenerate(http_client=client, base_url=env.gemini_base_url, api_key=env.gemini_api_key))


def _patch_prompt(prompt):
    messages = ensure(prompt)
    for message in messages:
        if message["role"] == "system":
            message["role"] = "user"
    return messages


@link_llm("gemini")
@link_llm("gemma-3")
class Google(AsyncChatOpenAI):
    @staticmethod
    def complete(prompt: str, **kwargs):
        return complete(_patch_prompt(prompt), **kwargs)

    @staticmethod
    def generate(prompt: str, **kwargs):
        return generate(_patch_prompt(prompt), **kwargs)


google = Google()
