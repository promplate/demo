from pydantic_settings import BaseSettings
from rich import print


class Config(BaseSettings):
    # llm providers
    anthropic_api_key: str = ""
    dashscope_api_key: str = ""
    minimax_api_key: str = ""
    openai_api_key: str = "*"
    openai_base_url: str = ""
    octoai_api_key: str = ""
    zhipu_api_key: str = ""
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"

    # other services
    serper_api_key: str = ""
    logfire_token: str = ""

    base_path: str = ""

    banned_substrings: list[str] = []
    banned_response: str = "Sorry, I can't help with that."

    @property
    def base(self):
        return f"/{self.base_path}" if self.base_path else ""

    model_config = {"env_file": ".env", "extra": "allow"}


env = Config()  # type: ignore

print(env)
