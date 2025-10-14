from .utils.config import env

if env.logfire_token:
    import logfire

    logfire.configure()
    logfire.info("app started", **env.model_dump())
    logfire.instrument_openai()
    logfire.instrument_anthropic()
    logfire.instrument_system_metrics()

    from .entry import app

    logfire.instrument_fastapi(app)

from .utils.load import generate_pyi

generate_pyi()
