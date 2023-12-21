"""
This file is responsible for defining the application's configuration settings.
It includes various configuration parameters that are loaded at runtime.
"""
from pydantic_settings import BaseSettings
from rich import print


class Config(BaseSettings):
    """
    Configuration class that holds application settings derived from environment variables.
    
    Attributes:
        openai_api_key: The API key for accessing OpenAI services.
        openai_base_url: The base URL for OpenAI API calls.
        serper_api_key: The API key for accessing Serper services.
        base_path: The base path for the application's endpoints.
    """
    openai_api_key: str = "*"
    openai_base_url: str = ""
    serper_api_key: str = ""

    base_path: str = ""

    @property
    def base(self):
        """
        Property to construct and return the base API path.
        
        Returns:
            str: The absolute base path prefix for API endpoints or an empty string if not set.
        """
        return f"/{self.base_path}" if self.base_path else ""

    model_config = {"env_file": ".env", "extra": "allow"}


env = Config()  # type: ignore

print(env)
