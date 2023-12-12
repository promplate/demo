from fastapi import FastAPI

app = FastAPI()


@app.get("/heartbeat")
def greet():
    return "hi"
