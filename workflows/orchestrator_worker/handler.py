from workflows.orchestrator_worker.builder import graph

def start_orchestrator():
    # Invoke
    state = graph.invoke({"topic": "Create a report on LLM scaling laws"})
    print(state["final_report"])