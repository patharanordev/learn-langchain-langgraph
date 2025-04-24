from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from workflows.chatbot.nodes.chatbot_node import ChatbotNode
from workflows.chatbot.state import ChatbotState
from llms.ollama import OllamaChain
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

# set graph state
chatbot_graph_builder = StateGraph(ChatbotState)

# tools if need
tools = []
if os.environ.get('ENABLE_FEATURE_TAVILY', False)=='1':
    from langchain_community.tools.tavily_search import TavilySearchResults
    tavily = TavilySearchResults(max_results=2)
    tools.append(tavily)

if os.environ.get('ENABLE_FEATURE_HUMAN_ASSISTANCE', False)=='1':
    from workflows.chatbot.tools.human_assistance import human_assistance
    tools.append(human_assistance)

if os.environ.get('ENABLE_FEATURE_MATH', False)=='1':
    from workflows.chatbot.tools.math_tool import multiply
    tools.append(multiply)

# setup llm chain
llm_with_tools = OllamaChain(tools=tools)

# prepare nodes
chatbot_node = ChatbotNode(llm_with_tools.llm)
tool_node = ToolNode(tools=tools)

# add nodes
chatbot_graph_builder.add_node('chatbot', chatbot_node.get_node)
chatbot_graph_builder.add_node('tools', tool_node)

# add edges
chatbot_graph_builder.add_conditional_edges(
    'chatbot',
    tools_condition,
)
chatbot_graph_builder.add_edge(START, 'chatbot')
chatbot_graph_builder.add_edge("tools", 'chatbot')

# allow remember context of previous interactions
memory = MemorySaver()
# add chat memory
graph = chatbot_graph_builder.compile(checkpointer=memory)

# Save the image data to a file
img_data = graph.get_graph().draw_mermaid_png()
with open('./output/graph-chatbot.png', 'wb') as f:
    f.write(img_data)
    print("Graph image saved successfully!")
