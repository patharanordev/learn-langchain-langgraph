from workflows.prompt_chain.builder import graph

def start_promp_chain():
    # Invoke
    state = graph.invoke({"topic": "cats"})
    print("Initial joke:")
    print(state["joke"])
    print("\n--- --- ---\n")
    if "improved_joke" in state:
        print("Improved joke:")
        print(state["improved_joke"])
        print("\n--- --- ---\n")

        print("Final joke:")
        print(state["final_joke"])
    else:
        print("Joke failed quality gate - no punchline detected!")

# from langgraph.func import entrypoint, task
# from llms.ollama import OllamaChain

# # setup llm chain
# llm = OllamaChain().llm

# # Tasks
# @task
# def generate_joke(topic: str):
#     """First LLM call to generate initial joke"""
#     msg = llm.invoke(f"Write a short joke about {topic}")
#     return msg.content


# def check_punchline(joke: str):
#     """Gate function to check if the joke has a punchline"""
#     # Simple check - does the joke contain "?" or "!"
#     if "?" in joke or "!" in joke:
#         return "Fail"

#     return "Pass"


# @task
# def improve_joke(joke: str):
#     """Second LLM call to improve the joke"""
#     msg = llm.invoke(f"Make this joke funnier by adding wordplay: {joke}")
#     return msg.content


# @task
# def polish_joke(joke: str):
#     """Third LLM call for final polish"""
#     msg = llm.invoke(f"Add a surprising twist to this joke: {joke}")
#     return msg.content


# @entrypoint()
# def parallel_workflow(topic: str):
#     original_joke = generate_joke(topic).result()
#     if check_punchline(original_joke) == "Pass":
#         return original_joke

#     improved_joke = improve_joke(original_joke).result()
#     return polish_joke(improved_joke).result()

# def start_promp_chain():
#     # Invoke
#     for step in parallel_workflow.stream("cats", stream_mode="updates"):
#         print(step)
#         print("\n")