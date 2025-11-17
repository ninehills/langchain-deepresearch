import os
from typing import List
import datetime

from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


# Search tool to use to do research
def WebSearch(
    query: str,
    max_results: int = 5,
):
    """Search the web for a query"""
    search_docs = tavily_client.search(
        query,
        search_depth="advanced",
        max_results=max_results,
        include_raw_content=False,
        topic="general",
    )
    return search_docs


# Fetch tool to do a deep fetch of a URL
def WebFetch(urls: List[str] | str):
    """Extract content from a list of URLs"""
    fetch_docs = tavily_client.extract(
        urls=urls,
        extract_depth="advanced",
        format="markdown",
    )
    return fetch_docs

# 获取当前日期
def GetCurrentDate():
    """Get the current date"""
    return datetime.datetime.now().strftime("%Y-%m-%d")


if __name__ == "__main__":
    print(">>> WebSearch")
    search_docs = WebSearch("What is the capital of France?")
    print(search_docs)

    print(">>> WebFetch")
    url = "https://en.wikipedia.org/wiki/Nvidia"
    fetch_docs = WebFetch(url)
    print(fetch_docs)
