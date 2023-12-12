FROM pypy:3.10

WORKDIR /

COPY /pyproject.toml /

RUN pip install pdm && pdm install --prod && pdm venv activate > /activate.sh && \
    pip freeze | xargs pip uninstall -y && rm -rf ~/.cache

COPY . .

ENV PORT 9040

EXPOSE $PORT

CMD /bin/bash -c "$(cat /activate.sh) && python3 -m uvicorn src:app --host 0.0.0.0 --port $PORT"