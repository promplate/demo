from contextlib import suppress

with suppress(ModuleNotFoundError):
    from dotenv import load_dotenv

    load_dotenv(override=True)

from .utils.config import env

if env.logfire_token:
    import logfire

    logfire.configure()
    logfire.info("app started", **env.model_dump())
    logfire.instrument_httpx()
    logfire.instrument_openai()
    logfire.instrument_anthropic()

    from .entry import app

    logfire.instrument_fastapi(app)

from .utils.load import generate_pyi

generate_pyi()
