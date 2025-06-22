from workflows.rag.adaptive.models.route_query import RouteQuery
from workflows.rag.adaptive.models.state import State
from llms.llm_provider import LLMProvider
from langchain_core.prompts import ChatPromptTemplate

class RouteQueryNode:

    system_prompt = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. Otherwise, use web-search."""

    def __init__(self, chain:LLMProvider):
        chain.set_prompt(ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "{question}"),
            ]
        ))
        self.llm = chain.settings.prompt | chain.llm

    def node(self, state:State):
        print('\n------------ RouteQueryNode ------------\n')
        print(state)

        result:RouteQuery = self.llm.invoke(
            {"question": state["messages"][-1]["content"]}
        )

        print('\nResult:\n')
        print(result)

        state["messages"].append({
            "content": result.datasource
        })
        
        return {
            "messages": state["messages"],
            "question": state["messages"][-1]["content"],
            "datasource": result.datasource
        }