from typing import Annotated
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool

from langgraph.types import Command, interrupt

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""

    # TODO: need to learn more about interrupt
    human_response = interrupt({"query": query})
    return human_response["data"]

# @tool
# # Note that because we are generating a ToolMessage for a state update, we
# # generally require the ID of the corresponding tool call. We can use
# # LangChain's InjectedToolCallId to signal that this argument should not
# # be revealed to the model in the tool's schema.
# def human_assistance(
#     name:str, tool_call_id: Annotated[str, InjectedToolCallId]
# ) -> str:
#     human_response = interrupt({
#         'question': 'Is this correct?',
#         'name': name,
#     })

#     if human_response.get('correct', '').lower().startwith('y'):
#         verified_name = name
#         response = 'Correct'
#     else:
#         verified_name = human_response.get('name', name)
#         response = f'Made a correction: {human_response}'

#     state_update = {
#         'name': verified_name,
#         'messages': [ToolMessage(response, tool_call_id=tool_call_id)],
#     }

#     return Command(update=state_update)