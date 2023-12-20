"""
This file contains the application configuration class that handles
environment-based settings using Pydantic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Configuration class leveraging Pydantic for environment management.
    It facilitates loading and accessing configuration variables.

    Attributes:
        openai_api_key (str): API key for the OpenAI service.
        openai_base_url (str): Base URL for the OpenAI API endpoints.
        model_config (SettingsConfigDict): Dictionary holding model-specific configuration,
                                         loaded from a designated .env file.
    """
    openai_api_key: str = "*"
    openai_base_url: str = ""

    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env")


env: Config = Config()
