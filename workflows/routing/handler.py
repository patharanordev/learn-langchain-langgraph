from workflows.routing.builder import graph

def start_routing():
    # Invoke
    state = graph.invoke({"input": "Write me a joke about cats"})
    print(state["output"])