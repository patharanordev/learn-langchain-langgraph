from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from models.chat_request import ChatRequest
from models.settings_request import SettingsRequest
from workflows.mcp_integration.builder import build_graph as build_graph_mcp
from workflows.routing.builder import build_graph as build_graph_routing
import asyncio

graph_cache = {
    # thread_id: compiled_graph
}
STREAM_TOKEN_BUFFER_SIZE = 5
router = APIRouter(prefix="/chat", tags=["chat"])

def send_message(message: str):
    """
    Sending a message in the format required for Server-Sent Events (SSE).

    Note: The "data:" prefix is part of the Server-Sent Events (SSE) format
    """
    return f"data: {message}\n\n"

def transform_message(message: any):
    if isinstance(message, str):
        return message
    elif isinstance(message, list) \
        and len(message) > 0 \
        and message[-1] is not None:
        return dict(message[-1]).get("text", '')
    else:
        return ''

async def invoke_graph(thread_id: str, request: ChatRequest):
    config = {'configurable': {'thread_id': thread_id}}
    
    graph = graph_cache[thread_id].get("graph")
    snapshot = graph.get_state(config)
    snapshot.next
    print(snapshot)

    # single-shot

    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config=config
    )

    # Extract the message content
    messages = result.get("messages", [])
    if not messages:
        return ""

    message = messages[-1]
    if isinstance(message, dict):
        content = message.get("content", "").strip()
    else:
        content = message.content.strip()
        if hasattr(message, "pretty_print"):
            message.pretty_print()

    return content

async def stream_graph_updates(thread_id: str, request: ChatRequest):
    config = {'configurable': {'thread_id': thread_id}}
    
    graph = graph_cache[thread_id].get("graph")
    snapshot = graph.get_state(config)
    snapshot.next
    print(snapshot)

    # reduce workload when streaming
    buffer = []
    
    async for message_chunk, metadata in graph.astream(
        {'messages': [{"role": "user", "content": request.message}]},
        config,
        stream_mode='messages'
    ):
        if message_chunk.content:
            print(message_chunk.content, end="|", flush=True)
            buffer.append(transform_message(message_chunk.content))
            
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

@router.post("/setting/{thread_id}")
async def update_setting(request: SettingsRequest, thread_id:str):
    try:
        if request.use_agent == "routing":
            graph = await build_graph_routing(request)
        else:
            graph = await build_graph_mcp(request)

        graph_cache[thread_id] = {
            "settings": request,
            "graph": graph,
        }

        return JSONResponse(
            content={ "data": "updated", "error": None },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={ "data": None, "error": str(e) },
            status_code=400
        )

@router.post("/{thread_id}")
async def chat(request: ChatRequest, thread_id:str):
    
    if thread_id not in graph_cache.keys():
        # TODO: Set to default setting
        return JSONResponse(
            content={ "data": None, "error": "Please set your model first." },
            status_code=400
        )

    # check setting of user's graph
    setting: SettingsRequest = graph_cache[thread_id].get("settings")
    if setting.is_streaming:
        return StreamingResponse(
            stream_graph_updates(thread_id, request),
            media_type="text/event-stream"
        )
    else:
        content = await invoke_graph(thread_id, request)
        return JSONResponse(
            content={ "data": content },
        )