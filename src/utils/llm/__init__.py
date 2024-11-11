from typing import Literal

from .anthropic import anthropic
from .azure import azure
from .cerebras import cerebras
from .chatglm import glm
from .dispatch import find_llm
from .groq import groq
from .minimax import minimax
from .octoai import octoai
from .openai import openai
from .qwen import qwen
from .siliconflow import siliconflow
from .xai import xai
from .yi import yi

openai_compatible_providers = {openai, xai, groq, azure, siliconflow, cerebras, yi}


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
    "azure:gpt-4o",
    "azure:gpt-4o-mini",
    "Mistral-Nemo",
    "Mistral-large",
    "Mistral-large-2407",
    "Mistral-small",
    "Meta-Llama-3.1-405B-Instruct",
    "Meta-Llama-3.1-70B-Instruct",
    "Meta-Llama-3.1-8B-Instruct",
    "Meta-Llama-3-70B-Instruct",
    "Meta-Llama-3-8B-Instruct",
    "Cohere-command-r-plus",
    "Cohere-command-r-plus-08-2024",
    "Cohere-command-r",
    "Cohere-command-r-08-2024",
    "AI21-Jamba-1.5-Large",
    "AI21-Jamba-1.5-Mini",
    "AI21-Jamba-Instruct",
    "Phi-3.5-MoE-instruct",
    "Phi-3.5-mini-instruct",
    "Phi-3-medium-128k-instruct",
    "Phi-3-medium-4k-instruct",
    "Phi-3-mini-128k-instruct",
    "Phi-3-mini-4k-instruct",
    "Phi-3-small-128k-instruct",
    "Phi-3-small-8k-instruct",
    "chatglm_turbo",
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "gemma-7b-it",
    "gemma2-9b-it",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "llama-3.1-405b-reasoning",
    "llama-3.2-1b-text-preview",
    "llama-3.2-3b-text-preview",
    "llama-3.2-11b-text-preview",
    "llama-3.2-90b-text-preview",
    "llama3.1-8b",
    "llama3.1-70b",
    "mixtral-8x7b-32768",
    "nous-hermes-2-mixtral-8x7b-dpo",
    "qwen-turbo",
    "qwen-plus",
    "abab5.5s-chat",
    "abab5.5-chat",
    "abab6-chat",
    "Qwen/Qwen2-7B-Instruct",
    "Qwen/Qwen2-1.5B-Instruct",
    "Qwen/Qwen2-72B-Instruct",
    "Qwen/Qwen2-57B-A14B-Instruct",
    "Vendor-A/Qwen/Qwen2-72B-Instruct",
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-32B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct",
    "THUDM/glm-4-9b-chat",
    "THUDM/chatglm3-6b",
    "01-ai/Yi-1.5-9B-Chat-16K",
    "01-ai/Yi-1.5-6B-Chat",
    "01-ai/Yi-1.5-34B-Chat-16K",
    "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-ai/DeepSeek-V2.5",
    "deepseek-ai/deepseek-llm-67b-chat",
    "internlm/internlm2_5-7b-chat",
    "internlm/internlm2_5-20b-chat",
    "yi-lightning",
    "grok-beta",
]
