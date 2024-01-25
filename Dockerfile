FROM oven/bun:1 AS bun

WORKDIR /frontend

COPY frontend/package.json /

RUN bun install

COPY frontend .

RUN bun run build

FROM pypy:3.10 AS pypy

WORKDIR /

COPY /pyproject.toml /

RUN pip install pdm && pdm install --prod && pdm venv activate > /activate.sh && \
    pip freeze | xargs pip uninstall -y && rm -rf ~/.cache

COPY . .

COPY --from=bun /frontend/dist /frontend/dist

ENV PORT 9040

EXPOSE $PORT

CMD /bin/bash -c "$(cat /activate.sh) && python3 -O -m uvicorn src:app --host 0.0.0.0 --port $PORT"