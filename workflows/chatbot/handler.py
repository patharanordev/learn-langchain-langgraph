from workflows.chatbot.builder import graph
import uuid

def stream_graph_updates(user_input:str, id):
    config = {'configurable': {'thread_id': id}}
    
    # check state
    snapshot = graph.get_state(config)
    snapshot.next

    events = graph.stream(
        {'messages':[{"role": "user", "content": user_input}]},
        config,
        stream_mode='values'
    )
    
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()
            # print("Assistant:", event['messages'][-1])

def start_chatbot():
    try:
        uid = str(uuid.uuid4())
        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break

                stream_graph_updates(user_input, uid)
                # print('---------------------------------------')
            except:
                # fallback if input() is not available
                user_input = "What do you know about LangGraph?"
                print("User: " + user_input)
                stream_graph_updates(user_input, uid)
                break

    except Exception as e:
        print(f"An error occurred: {e}")