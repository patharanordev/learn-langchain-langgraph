from langchain import hub
from workflows.rag.agentic_ai.builder import graph
import pprint, os

class AgenticAI:
    def __init__(self):
        os.environ['USER_AGENT'] = 'my-agentic-ai'
        
    def validate_prompt(self):
        print('*' * 20 + 'Prompt[rlm/rag-prompt]' + '*' * 20)
        hub.pull('rlm/rag-prompt').pretty_print()

    def start(self):
        inputs = {
            'messages': [
                ('user', 'What does Lilian Weng say about the types of agent memory?')
            ]
        }

        for output in graph.stream(inputs):
            for key, value in output.items():
                pprint.pprint(f"Output from node '{key}':")
                pprint.pprint("---")
                pprint.pprint(value, indent=2, width=80, depth=None)
            pprint.pprint("\n---\n")