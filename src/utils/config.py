from pydantic_settings import BaseSettings
from rich import print


class Config(BaseSettings):
    # llm providers
    github_models_api_key: str = ""
    github_models_base_url: str = "https://models.inference.ai.azure.com"
    siliconflow_api_key: str = ""
    siliconflow_base_url: str = "https://api.siliconflow.cn/v1/"
    sambanova_api_key: str = ""
    sambanova_base_url: str = "https://api.sambanova.ai/v1"
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    anthropic_api_key: str = ""
    dashscope_api_key: str = ""
    cerebras_api_key: str = ""
    cerebras_base_url: str = "https://api.cerebras.ai/v1"
    minimax_api_key: str = ""
    openai_api_key: str = "*"
    openai_base_url: str = ""
    octoai_api_key: str = ""
    zhipu_api_key: str = ""
    gemini_api_key: str = ""
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    xai_api_key: str = ""
    xai_base_url: str = "https://api.x.ai/v1"
    yi_api_key: str = ""
    yi_base_url: str = "https://api.lingyiwanwu.com/v1"

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


env = Config()  # type: ignore

print(env)
