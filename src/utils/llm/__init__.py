from openai.types.chat_model import ChatModel

from .dispatch import find_llm
from .openai import openai

openai_compatible_providers = {openai}


Model = ChatModel | str
