from os import getenv

from .utils.config import env


def get_sha(default: str):
    return getenv("RENDER_GIT_COMMIT") or getenv("RAILWAY_GIT_COMMIT_SHA") or default


if env.logfire_token:
    import logfire

    logfire.configure(code_source=logfire.CodeSource("https://github.com/promplate/demo", get_sha("deploy")))
    logfire.info("app started", **env.model_dump())
    logfire.instrument_openai()
    logfire.instrument_anthropic()
    logfire.instrument_system_metrics()

    from .entry import app

    logfire.instrument_fastapi(app)

from .utils.load import generate_pyi

generate_pyi()
