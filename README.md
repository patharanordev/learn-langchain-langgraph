# Learn LangChain & LangGraph

Ref. https://langchain-ai.github.io/langgraph/tutorials/



## Prerequisites

### Environment Variables

Prepare `.env` file:

```text
OPENAI_API_KEY=
TAVILY_API_KEY=tvly-dev-xdfFV...IYgM2
LOGFIRE_API_KEY=pylf_v1_us_z79J9...VN7Rz
LANGCHAIN_API_KEY=
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

```sh
uv venv

# WinOS: active venv
.\.venv\Scripts\activate.ps1

# Linux: active venv
source .venv/bin/activate

# Install dependency
uv sync
```

active some workflow in `main.py`, then try:

```sh
uv run main.py
```
