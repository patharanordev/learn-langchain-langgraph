# Orchestrator Workers

Someone call Map-reduce.

Workflow:

- Set topic to `orchestrator` to generate list of section.
- Then assign each section via `assign_workers` function to sub-llms or workers or `llm_call` to generate description/content of the section.
- Compose/Transform all of content via `synthesizer` before return to user.
