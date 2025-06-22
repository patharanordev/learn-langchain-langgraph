## Adaptive RAG

### Prerequisites

- Chroma
- Ollama
- Environment variables:

    ```txt
    USER_AGENT=learn_langchain_langgraph/0.1

    # For download embedding model from huggingface
    HF_TOKEN=hf_hD...TcDM

    # To support retriever selection in the future
    RETRIEVER_PROVIDER_NAME=chroma

    # Chroma settings
    CHROMA_HOST=chroma
    CHROMA_PORT=8000
    CHROMA_DEVICE=cpu
    ```

### Usage

Setting model/agent:

```sh
curl --location 'http://localhost:8000/chat/setting/1' \
--header 'Content-Type: application/json' \
--data '{
    "base_url": "http://local-ollama-service:11434",
    "model_name": "llama3.2:latest",
    "temperature": 0.7,
    "streaming": false,
    "use_agent": "adaptive_rag", 
    "save_graph_path": "./output/graph-adaptive-rag.png"
}'
```

Upload your documents (website's urls) that you want to vectordb (retriever), in this case it is ChromaDB:

```sh
curl --location 'http://localhost:8000/document/upload' \
--header 'Content-Type: application/json' \
--data '{
    "collection_name": "poc",
    "urls": [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/"
    ]
}'
```

Let's chat:

```sh
curl --location 'http://localhost:8000/chat/1' \
--header 'Content-Type: application/json' \
--data '{
    "message": "Who will the Bears draft first in the NFL draft?"
}'
```
