from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    openai_api_key: str = "*"
    openai_base_url: str = ""

    model_config = SettingsConfigDict(env_file=".env")


env = Config()  # type: ignore
