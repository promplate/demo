"""
This file defines API routes and handlers for the server.

It includes endpoints for invoking models, streaming responses,
and processing individual steps in a run.
"""

from json import dumps
from sys import stderr
from traceback import print_exc
from typing import Annotated, Literal, cast

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, StreamingResponse
from promplate import Node
from pydantic import BaseModel, Field

from ..logic import get_node
from ..logic.tools import tool_map
from ..utils.config import env
from .sse import server_sent_events

run_router = APIRouter(tags=["call"])


class Message(BaseModel):
    """
    Represents a message in the context of a conversation.

    Attributes:
        content: The text content of the message.
        role: The role of the entity that produced the message (user, assistant, or system).
        name: An optional identifier for the tool associated with the message.
    """
    content: str
    role: Literal["user", "assistant", "system"]
    name: Annotated[Literal.__getitem__(tuple(tool_map)), str] | None = None  # type: ignore


class ContextIn(BaseModel):
    """
    Defines the input context for API calls that include a list of messages
    and settings for the conversation model.

    Attributes:
        messages: A list of messages that make up the conversation history.
        model: The model identifier for the language model to use.
        temperature: A float that controls the randomness of the model's responses.
    """
    messages: list[Message]
    model: Literal["gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106"] = "gpt-3.5-turbo-1106"
    temperature: float = Field(0.7, ge=0, le=1)

    model_config = {"json_schema_extra": {"example": {"messages": [{"content": "What's the date today?", "role": "user"}]}}}


@run_router.post(f"{env.base}/invoke/{{node:path}}")
async def invoke(context: ContextIn, node: Node = Depends(get_node)):
    """
    Process a synchronous API call to invoke an AI model.

    Args:
        context: The context containing messages and settings for the model.
        node: The Node object that will handle the API call.

    Returns:
        The model's response to the input context.
    """
    try:
        return await node.ainvoke(context.model_dump(exclude_unset=True), temperature=context.temperature, model=context.model)
    except Exception as e:
        print_exc(file=stderr)
        return PlainTextResponse(str(e), 500)


@run_router.post(f"{env.base}/stream/{{node:path}}")
async def stream(context: ContextIn, node: Node = Depends(get_node)):
    """
    Initiates a streaming response where the AI model's output
    is sent as server-sent events.

    Args:
        context: The context containing messages and settings for the model.
        node: The Node object that will handle the streaming.

    Returns:
        A streaming response with the model's output as events.
    """
    @server_sent_events
    async def make_stream():
        try:
            async for c in node.astream(context.model_dump(exclude_unset=True)):
                yield "partial" if c.get("partial") else "whole", dumps(c["parsed"], ensure_ascii=False)
            yield "finish", dumps(c.maps[0], ensure_ascii=False)  # type: ignore
        except Exception as e:
            print_exc(file=stderr)
            yield "error", str(e)

    return StreamingResponse(make_stream(), media_type="text/event-stream")


@run_router.put(f"{env.base}/single/{{node}}")
async def step_run(context: ContextIn, node: Node = Depends(get_node)):
    """
    Executes a single step of the AI model and returns the result.

    This is used when a step-by-step execution is required,
    rather than a continuous stream.

    Args:
        context: The context containing messages and configuration for the model.
        node: The Node object that executes the step.

    Returns:
        A plain text streaming response with the model's output for each step.
    """
    async def make_stream():
        last = ""
        async for c in node.astream(context.model_dump(exclude_unset=True)):
            if c.result != last:
                yield cast(str, c.result).removeprefix(last)
                last = c.result

    return StreamingResponse(make_stream(), media_type="text/plain")
