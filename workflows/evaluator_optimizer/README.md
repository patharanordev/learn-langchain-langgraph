# Evaluator & Optimizer

Adding optimize node to evaluate it via `llm_call_evaluator`, outcome will be trigger to **end node** or **stay in feedback loop** via `route_joke`.

## Usage

```sh
curl --location 'http://localhost:8000/chat/1' \
--header 'Content-Type: application/json' \
--data '{
    "message": "Cats"
}'
```
