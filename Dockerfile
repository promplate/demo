FROM oven/bun:1-alpine AS js
WORKDIR /app
COPY frontend/package.json /
RUN bun install
COPY frontend .
RUN NODE_ENV=production bun run build

FROM python:3.12 AS py
WORKDIR /app
COPY pyproject.toml .
RUN pip install uv && uv venv && uv pip install -r pyproject.toml --compile-bytecode

FROM python:3.12 AS base
WORKDIR /app
COPY --from=js /app/dist frontend/dist
COPY --from=py /app .
COPY . .

ENV PORT 9040

EXPOSE $PORT

CMD /bin/bash -c "source .venv/bin/activate && python3 -O -m uvicorn src:app --host 0.0.0.0 --port $PORT"
