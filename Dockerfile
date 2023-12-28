FROM bitnami/python

WORKDIR /

COPY /pyproject.toml /

RUN pip install fastapi uvicorn[standard] promplate[all] promplate-trace[langfuse,langsmith] python-box pydantic-settings httpx[http2] promptools[validation] fake-useragent html2text beautifulsoup4 rich zhipuai anthropic

COPY . .

ENV PORT 9040

EXPOSE $PORT

CMD python3 -O -m uvicorn src:app --host 0.0.0.0 --port $PORT
