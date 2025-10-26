from promplate.llm.openai import AsyncChatComplete, AsyncChatGenerate, AsyncChatOpenAI
from promplate_trace.auto import patch

from ..config import env
from .common import client
from .dispatch import link_llm


@link_llm("abab")
@link_llm("MiniMax")
class MiniMax(AsyncChatOpenAI):
    complete = staticmethod(
        patch.chat.acomplete(AsyncChatComplete(http_client=client, base_url=env.minimax_base_url, api_key=env.minimax_api_key))
    )
    generate = staticmethod(
        patch.chat.agenerate(AsyncChatGenerate(http_client=client, base_url=env.minimax_base_url, api_key=env.minimax_api_key))
    )


minimax = MiniMax()
