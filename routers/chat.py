from typing import Optional
from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse, JSONResponse
from models.chat_request import ChatRequest
from workflows.chatbot.builder import create_graph
import asyncio

STREAM_TOKEN_BUFFER_SIZE = 5

router = APIRouter(prefix="/chat", tags=["chat"])

def send_message(message: str):
    """
    Sending a message in the format required for Server-Sent Events (SSE).

    Note: The "data:" prefix is part of the Server-Sent Events (SSE) format
    """
    return f"data: {message}\n\n"

async def stream_graph_updates(thread_id: str, request: ChatRequest):
    config = {'configurable': {'thread_id': thread_id}}
    
    graph = create_graph(model=request.model, streaming=request.is_streaming)  # or use request.model
    snapshot = graph.get_state(config)
    snapshot.next
    print(snapshot)

    if request.is_streaming: # streaming

        # reduce workload when streaming
        buffer = []
        
        async for message_chunk, metadata in graph.astream(
            {'messages': [{"role": "user", "content": request.message}]},
            config,
            stream_mode='messages'
        ):
            if message_chunk.content:
                buffer.append(message_chunk.content)
                print(message_chunk.content, end="|", flush=True)

                if len(buffer) >= STREAM_TOKEN_BUFFER_SIZE:
                    message = "".join(buffer).strip()
                    buffer.clear()
                    yield send_message(message)
                    await asyncio.sleep(0.01)

        if len(buffer) > 0:
            message = "".join(buffer).strip()
            buffer.clear()
            yield send_message(message)
            await asyncio.sleep(0.01)

    else: # single-shot

        async for event in graph.astream(
            {'messages': [{"role": "user", "content": request.message}]},
            config,
            stream_mode='values'
        ):
            if "messages" in event:
                message = event["messages"][-1]
                content = message.content.strip()
                
                if content == "":
                    continue
                
                message.pretty_print()
                yield send_message(message.content)


@router.post("/{thread_id}")
async def chat(request: ChatRequest, thread_id:str):
    return StreamingResponse(
        stream_graph_updates(thread_id, request),
        media_type="text/event-stream"
    )