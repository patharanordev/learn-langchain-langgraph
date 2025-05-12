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

Active some workflow in `main.py`, then try:

```sh
# Linux or macOS
uv run main.py

# WindowsOS
python main.py
```
