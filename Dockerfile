FROM oven/bun:1-alpine AS js
WORKDIR /app
COPY frontend/package.json /
RUN bun install
COPY frontend .
RUN NODE_ENV=production bun run build

FROM bitnami/python:3.12 AS py
WORKDIR /
COPY /pyproject.toml /
RUN pip install fastapi uvicorn[standard] promplate[all] promplate-trace[langfuse,langsmith] python-box pydantic-settings httpx[http2] promptools[validation,stream] fake-useragent html2text beautifulsoup4 rich zhipuai anthropic dashscope
COPY . .
COPY --from=js /app/dist frontend/dist

ENV PORT 9040

EXPOSE $PORT

CMD python3 -O -m uvicorn src:app --host 0.0.0.0 --port $PORT
