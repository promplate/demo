FROM oven/bun:1-alpine AS js
WORKDIR /app
COPY frontend/package.json /
RUN bun install
COPY frontend .
RUN NODE_ENV=production bun run build

FROM python:3.12-slim AS py
WORKDIR /app
COPY pyproject.toml .
RUN pip install uv --disable-pip-version-check --root-user-action ignore && uv venv && uv sync --compile-bytecode

FROM python:3.12-slim AS base
WORKDIR /app
COPY --from=js /app/dist frontend/dist
COPY --from=py /app .
COPY . .

ENV PORT=9040
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE $PORT

CMD python3 -O -m uvicorn src.entry:app --host 0.0.0.0 --port $PORT
