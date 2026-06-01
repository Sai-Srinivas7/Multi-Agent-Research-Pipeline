from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool

ddg = DuckDuckGoSearchRun()

@tool("Internet Search Tool")
def search_tool(query: str) -> str:
    """Search the internet for information, news, and AI frameworks."""
    return ddg.invoke(query)
