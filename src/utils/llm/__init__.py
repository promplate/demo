from typing import Literal

from .anthropic import anthropic
from .azure import azure
from .cerebras import cerebras
from .chatglm import glm
from .deepseek import deepseek
from .dispatch import find_llm
from .google import google
from .groq import groq
from .minimax import minimax
from .openai import openai
from .qwen import qwen
from .sambanova import sambanova
from .siliconflow import siliconflow
from .xai import xai
from .yi import yi

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
    "gpt-4o-2024-11-20",
    "gpt-4-1106-preview",
    "gpt-4-0125-preview",
    "gpt-4-turbo",
    "gpt-4-turbo-2024-04-09",
    "azure:gpt-4o",
    "azure:gpt-4o-mini",
    "azure:o1",
    "azure:o1-mini",
    "azure:o3-mini",
    "azure:o1-preview",
    "Mistral-Nemo",
    "Mistral-large",
    "Mistral-large-2407",
    "Mistral-large-2411",
    "Mistral-small",
    "Mistral-small-2503",
    "Codestral-2501",
    "Ministral-3B",
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
    "Phi-4",
    "Phi-3.5-MoE-instruct",
    "Phi-3.5-mini-instruct",
    "Phi-3-medium-128k-instruct",
    "Phi-3-medium-4k-instruct",
    "Phi-3-mini-128k-instruct",
    "Phi-3-mini-4k-instruct",
    "Phi-3-small-128k-instruct",
    "Phi-3-small-8k-instruct",
    "DeepSeek-R1",
    "DeepSeek-V3",
    "chatglm_turbo",
    "claude-instant-1.2",
    "claude-2.1",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "qwen-2.5-32b",
    "qwen-2.5-coder-32b",
    "qwen-qwq-32b",
    "deepseek-r1-distill-qwen-32b",
    "deepseek-r1-distill-llama-70b",
    "deepseek-r1-distill-llama-70b-specdec",
    "gemma-7b-it",
    "gemma2-9b-it",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "llama-3.1-70b-specdec",
    "llama-3.1-405b-reasoning",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "llama-3.2-11b-vision-preview",
    "llama-3.2-90b-vision-preview",
    "llama-3.3-70b-versatile",
    "llama-3.3-70b-specdec",
    "llama3.1-8b",
    "llama3.1-70b",
    "llama-3.3-70b",
    "mixtral-8x7b-32768",
    "qwen-turbo",
    "qwen-plus",
    "qwen-max",
    "abab5.5s-chat",
    "abab5.5-chat",
    "abab6-chat",
    "Qwen/QwQ-32B-Preview",
    "Qwen/QwQ-32B",
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-32B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct-128K",
    "THUDM/glm-4-9b-chat",
    "THUDM/chatglm3-6b",
    "01-ai/Yi-1.5-9B-Chat-16K",
    "01-ai/Yi-1.5-6B-Chat",
    "01-ai/Yi-1.5-34B-Chat-16K",
    "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-ai/DeepSeek-V2.5",
    "deepseek-ai/deepseek-llm-67b-chat",
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-R1",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "internlm/internlm2_5-7b-chat",
    "internlm/internlm2_5-20b-chat",
    "yi-lightning",
    "grok-beta",
    "grok-2-1212",
    "Qwen2.5-Coder-32B-Instruct",
    "Qwen2.5-72B-Instruct",
    "QwQ-32B-Preview",
    "QwQ-32B",
    "Llama-3.1-Tulu-3-405B",
    "Llama-3.2-11B-Vision-Instruct",
    "Llama-3.2-90B-Vision-Instruct",
    "Meta-Llama-3.2-1B-Instruct",
    "Meta-Llama-3.2-3B-Instruct",
    "Meta-Llama-3.3-70B-Instruct",
    "DeepSeek-V3-0324",
    "DeepSeek-R1-Distill-Llama-70B",
    "deepseek-chat",
    "deepseek-reasoner",
    "gemma-3-27b-it",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-thinking-exp",
]
