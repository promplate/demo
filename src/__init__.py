from fastapi import FastAPI

app = FastAPI()


@app.get("/heartbeat")
def greet():
    """
    Returns a greeting message.
    """
    return "hi"
