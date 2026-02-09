## Streaming

### .stream vs .astream

| Aspect          | `.stream()`          | `.astream()`           |
| --------------- | -------------------- | ---------------------- |
| Type            | Sync generator       | Async generator        |
| Usage Style     | `for ... in ...`     | `async for ... in ...` |
| Suitable for    | Simple/blocking code | Async/await systems    |
| Easy to stream? | Yes                  | Yes (with setup)       |

### stream_mode

| `stream_mode`       | Behavior                                                           |
| ------------------- | ------------------------------------------------------------------ |
| `"values"`          | Emits all final resolved values (most reliable for output)         |
| `"messages"`        | Emits only message updates                                         |
| `"updates"`         | Emits low-level execution updates (node-wise execution, etc.)      |
| `"all"`             | Emits everything possible (like a superset of the above modes)     |
| `["messages", ...]` | Not yet supported officially** in all streaming functions          |
| `"custom"`          | Meant for custom stream handlers — you must implement a handler    |