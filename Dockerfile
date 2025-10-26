FROM oven/bun:1-alpine AS js
WORKDIR /app
COPY frontend/package.json /
RUN bun install
COPY frontend .
RUN NODE_ENV=production bun run -b build

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS py
WORKDIR /app
COPY pyproject.toml .
RUN uv sync --compile-bytecode

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base
RUN apt-get update && apt-get install -y curl && curl -s https://api.github.com/repos/cli/cli/releases/latest | python -c "import json, sys; data = json.load(sys.stdin); tag = data['tag_name']; version = tag[1:]; print(f'https://github.com/cli/cli/releases/download/{tag}/gh_{version}_linux_amd64.tar.gz')" | xargs curl -L | tar -xz && cp gh_*/bin/gh /usr/local/bin/ && rm -rf gh_*
WORKDIR /app
COPY --from=js /app/dist frontend/dist
COPY --from=py /app .
COPY . .

ENV PORT=9040

EXPOSE $PORT

CMD .venv/bin/python -O -m uvicorn src.entry:app --host 0.0.0.0 --port $PORT
