FROM oven/bun:1-alpine AS js
WORKDIR /app
COPY frontend/package.json /
RUN bun install
COPY frontend .
RUN NODE_ENV=production bun run build

FROM python:3.12 AS py
WORKDIR /app
COPY pyproject.toml .
RUN pip install pdm && pdm install --prod && pdm venv activate > activate.sh

FROM python:3.12 AS base
WORKDIR /app
COPY --from=js /app/dist frontend/dist
COPY --from=py /app .
COPY . .

ENV PORT 9040

EXPOSE $PORT

CMD /bin/bash -c "$(cat activate.sh) && python3 -O -m uvicorn src:app --host 0.0.0.0 --port $PORT"
