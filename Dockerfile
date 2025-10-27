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
RUN apt-get update && apt-get install -y curl gpg wget && \
    mkdir -p -m 755 /etc/apt/keyrings && \
    wget -nv -O- https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg && \
    mkdir -p -m 755 /etc/apt/sources.list.d && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && apt-get install -y gh
WORKDIR /app
COPY --from=js /app/dist frontend/dist
COPY --from=py /app .
COPY . .

ENV PORT=9040

EXPOSE $PORT

CMD .venv/bin/python -O -m uvicorn src.entry:app --host 0.0.0.0 --port $PORT
