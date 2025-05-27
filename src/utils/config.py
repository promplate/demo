from pydantic_settings import BaseSettings
from rich import print


class Config(BaseSettings):
    # llm providers
    openai_api_key: str = "*"
    openai_base_url: str = ""

    # other services
    serper_api_key: str = ""
    logfire_token: str = ""

    base_path: str = ""

    banned_substrings: list[str] = []
    banned_response: str = "Sorry, I can't help with that."

    openai_compatible_api: bool = True

    @property
    def base(self):
        return f"/{self.base_path}" if self.base_path else ""

    model_config = {"env_file": ".env", "extra": "allow"}


env = Config()

print(env)
