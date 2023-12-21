"""
This module provides configuration settings for the application using environment variables.
"""
from pydantic_settings import BaseSettings
from rich import print


class Config(BaseSettings):
    openai_api_key: str = "*"
    openai_base_url: str = ""
    serper_api_key: str = ""

    base_path: str = ""

    @property
    def base(self):
        """
        Constructs the base API path.

        The value is prefixed with a slash if base_path is set,
        else returns an empty string.

        Returns:
            A string representing the base API path.
        """
        return f"/{self.base_path}" if self.base_path else ""

    model_config = {"env_file": ".env", "extra": "allow"}


env = Config()  # type: ignore

print(env)
