"""
File: openai.py

This module is used to create an instance of the `AsyncChatOpenAI` class from the `promplate.llm.openai` module, which is used to interact with the OpenAI API.
"""
from os import environ

from httpx import AsyncClient
from promplate.llm.openai import AsyncChatOpenAI
# TODO: Add a docstring to the `AsyncChatOpenAI` class in the `promplate.llm.openai` module to describe its purpose and usage.

from ..config import env

openai = AsyncChatOpenAI(http_client=AsyncClient(http2=True), api_key=env.openai_api_key, base_url=env.openai_base_url).bind(
    # The `openai` object is an instance of the `AsyncChatOpenAI` class, which is used to interact
    # with the OpenAI API. It is initialized with the following parameters:
    # - `http_client`: An HTTP client for making requests.
    # - `api_key`: The API key for authenticating with the OpenAI API.
    # - `base_url`: The base URL for the API endpoints.
    # - `model`: OpenAI model to be used for generating responses.
    # - `temperature`: Controls the randomness of the response generation.
    model="gpt-3.5-turbo-1106",
    temperature=0.2,
    # response_format={"type": "json_object"},
)


environ.clear()
