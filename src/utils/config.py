from pydantic_settings import BaseSettings


class Config(BaseSettings):
    openai_api_key: str = "*"
    openai_base_url: str = ""
    serper_api_key: str = ""

    model_config = {"env_file": ".env", "extra": "allow"}


env = Config()  # type: ignore
