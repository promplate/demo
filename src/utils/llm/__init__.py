from typing import Literal

from .anthropic import anthropic
from .chatglm import glm
from .dispatch import find_llm
from .groq import groq
from .minimax import minimax
from .octoai import octoai
from .openai import openai
from .qwen import qwen

Model = Literal[
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-4o-2024-05-13",
    "gpt-4-1106-preview",
    "gpt-4-0125-preview",
    "gpt-4-turbo-2024-04-09",
    "chatglm_turbo",
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "gemma-7b-it",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "llama2-70b-4096",
    "mixtral-8x7b-32768",
    "nous-hermes-2-mixtral-8x7b-dpo",
    "qwen-turbo",
    "qwen-plus",
    "abab5.5s-chat",
    "abab5.5-chat",
    "abab6-chat",
]
