from typing import Literal

from .anthropic import anthropic
from .cerebras import cerebras
from .chatglm import glm
from .dispatch import find_llm
from .groq import groq
from .minimax import minimax
from .octoai import octoai
from .openai import openai
from .qwen import qwen
from .siliconflow import siliconflow

Model = Literal[
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "gpt-4-1106-preview",
    "gpt-4-0125-preview",
    "gpt-4-turbo",
    "gpt-4-turbo-2024-04-09",
    "chatglm_turbo",
    "claude-instant-1.2",
    "claude-2.1",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "gemma-7b-it",
    "gemma2-9b-it",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "llama-3.1-405b-reasoning",
    "llama3.1-8b",
    "llama3.1-70b",
    "mixtral-8x7b-32768",
    "nous-hermes-2-mixtral-8x7b-dpo",
    "qwen-turbo",
    "qwen-plus",
    "qwen-max",
    "abab5.5s-chat",
    "abab5.5-chat",
    "abab6-chat",
    "Qwen/Qwen2-7B-Instruct",
    "Qwen/Qwen2-1.5B-Instruct",
    "Qwen/Qwen1.5-7B-Chat",
    "Qwen/Qwen2-72B-Instruct",
    "Qwen/Qwen2-57B-A14B-Instruct",
    "Qwen/Qwen1.5-110B-Chat",
    "Qwen/Qwen1.5-32B-Chat",
    "Qwen/Qwen1.5-14B-Chat",
    "THUDM/glm-4-9b-chat",
    "THUDM/chatglm3-6b",
    "01-ai/Yi-1.5-9B-Chat-16K",
    "01-ai/Yi-1.5-6B-Chat",
    "01-ai/Yi-1.5-34B-Chat-16K",
    "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-ai/deepseek-llm-67b-chat",
]
