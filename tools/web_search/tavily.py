from langchain_community.tools.tavily_search import TavilySearchResults
from config.settings import settings

web_search_tool = TavilySearchResults(
    tavily_api_key=settings.tavily_api_key,
    k=3,
)