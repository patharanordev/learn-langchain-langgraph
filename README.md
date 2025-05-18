# Learn LangChain & LangGraph

Ref. https://langchain-ai.github.io/langgraph/tutorials/

## Prerequisites

### Environment Variables

Prepare `.env` file:

```env
# 3rd-party frameworks
OPENAI_API_KEY=
TAVILY_API_KEY=tvly-dev-xdfFV...IYgM2
LOGFIRE_API_KEY=pylf_v1_us_z79J9...VN7Rz
LANGCHAIN_API_KEY=

# bedrock
AWS_BEDROCK_REGION=
AWS_BEDROCK_ACCESS_KEY=
AWS_BEDROCK_SECRET_KEY=

# feature flags
ENABLE_FEATURE_TAVILY=0
ENABLE_FEATURE_HUMAN_ASSISTANCE=0
ENABLE_FEATURE_MATH=0
```

### Package Management

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Ollama

Let's provide [Ollama](https://ollama.com/) via `http://localhost:11434/`.

### MCP Server

Serve some MCP's tool, ex. [weather](https://modelcontextprotocol.io/quickstart/server).

You need to serve some MCP server before testing langgraph:

```sh
uv run weather.py
```

Currently I'm listening MCP server via port number `7300` in langgraph. So don't forget set it in MCP server too.

## Usage

### Linux or macOS

```sh
uv venv

# WinOS: active venv
.\.venv\Scripts\activate.ps1

# Linux: active venv
source .venv/bin/activate

# Install dependency
uv sync
```

### WindowsOS

To prevent `onnxruntime` incompatible with `windows` platform:

```sh
error: Distribution `onnxruntime==1.22.0 @ registry+https://pypi.org/simple` can't be installed because it doesn't have a source distribution or wheel for the current platform

hint: You're on Windows (`win_amd64`), but `onnxruntime` (v1.22.0) only has wheels for the following platforms: `manylinux_2_27_aarch64`, `manylinux_2_27_x86_64`, `manylinux_2_28_aarch64`, `manylinux_2_28_x86_64`, `macosx_13_0_universal2`
```

please install dependency via `python3` this CLI:

```sh
uv pip freeze > requirements.txt
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run

> ---
> Don't forget start `ollama` if you no have any LLM providers:
>
> ```
> ollama serve
> ```
>
> ---

Active some workflow in `main.py`, then try:

```sh
# Linux or macOS
uv run main.py

# WindowsOS
python main.py
```

Started:

```sh
INFO:     Started server process [22576]
INFO:     Waiting for application startup.
Starting up...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:58164 - "POST /chat/1 HTTP/1.1" 200 OK
```

### Streaming

```sh
curl --location 'http://localhost:8000/chat/1' \
--header 'Content-Type: application/json' \
--data '{
    "message": "hi, who are you?",
    "model": "llama3.2:latest",
    "is_streaming": true
}'
```

Ex. output:

```sh
StateSnapshot(values={}, next=(), config={'configurable': {'thread_id': '1'}}, metadata=None, created_at=None, parent_config=None, tasks=(), interrupts=())
I|'m| an| AI| chat|bot|,| also| known| as| a| convers|ational| AI| or| natural| language| processing| (|N|LP|)| model|.| I| don|'t| have| personal| experiences|,| emotions|,| or| consciousness| like| humans| do|,| but| I|'m| designed| to| simulate| conversation| and| answer| questions| to| the| best| of| my| ability|.

|My| name| isn|'t| really| a| "|name|"| in| the| classical| sense|,| but| I|'m| often| referred| to| as| "|Assistant|"| or| "|Bot|"| by| users| like| you|.| I| exist| solely| to| provide| information|,| answer| questions|,| and| engage| in| discussions| on| a| wide| range| of| topics|.

|I|'ve| been| trained| on| vast| amounts| of| text| data|,| which| allows| me| to| generate| human|-like| responses| to| a| broad| range| of| queries|.| However|,| my| knowledge| cutoff| is| December| |202|3|,| so| if| you| ask| me| about| very| recent| events| or| developments|,| I| might| not| have| the| most| up|-to|-date| information|.

|Feel| free| to| ask| me| anything|,| and| I|'ll| do| my| best| to| provide| a| helpful| response|!|
```

## References

- [Streaming in LangGraph](./docs/streaming.md)