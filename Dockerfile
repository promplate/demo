FROM pypy:3.10-slim

WORKDIR /

COPY /pyproject.toml /

RUN pip install pdm && pdm install --prod && pdm venv activate > /activate.sh && \
    pip freeze | xargs pip uninstall -y && rm -rf ~/.cache

COPY . .

ENV PORT 9040

EXPOSE $PORT

CMD $(cat /activate.sh) && dotenv run python -O -m pdm prod