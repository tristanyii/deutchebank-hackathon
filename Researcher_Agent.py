# Researcher_Agent.py
from typing import TypedDict, Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper, WikipediaAPIWrapper
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from langchain_community.tools import WikipediaQueryRun
from dotenv import load_dotenv
import os
import requests
from langchain_core.callbacks import StdOutCallbackHandler

load_dotenv() 

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
DPLA_API_KEY = os.getenv("DPLA_API_KEY")
if not all([GROQ_API_KEY, SERP_API_KEY, DPLA_API_KEY]):
    raise ValueError("One or more API keys are missing from .env file.")

llm = "meta-llama/llama-4-scout-17b-16e-instruct" 
chat_groq_llm = ChatGroq(model_name=llm, groq_api_key=GROQ_API_KEY)

def dpla_search(query: str) -> str:
    api_key = DPLA_API_KEY
    base_url = "https://api.dp.la/v2/items"
    params = {"q": query, "api_key": api_key, "page_size": 5}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get("docs"):
            return "No primary sources found in the DPLA for that query."
        results = []
        for item in data["docs"]:
            title = item.get("sourceResource", {}).get("title", "No Title")
            provider = item.get("provider", {}).get("name", "Unknown Provider")
            link = item.get("isShownAt", "No Link")
            results.append(f"Title: {title}\nProvider: {provider}\nLink: {link}\n---")
        return "\n".join(results)
    except requests.exceptions.RequestException as e:
        return f"Error accessing DPLA API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

class DPLASearchSchema(BaseModel):
    query: str
class GoogleSearchSchema(BaseModel):
    query: str
class WikipediaSearchSchema(BaseModel):
    query: str
    
researcher_agent_message = """
You are a highly skilled Archival Researcher Agent. Your mission is to write a COMPREHENSIVE and DETAILED report based on the provided research plan.

Workflow Protocol:
1.  You will be given a research plan or a direct question.
2.  You MUST analyze the request to determine the most appropriate tool.
3.  You MUST follow the Tool Selection Mandate below.
4.  After using the correct tool(s) to gather information, you MUST compile all findings into a single, cohesive, final report. This final output is the ONLY thing you will return.

Tool Selection Mandate (Strictly Enforced):
1. IF the request asks for a "general summary," "overview," or broad foundational knowledge of a topic, you MUST prioritize using the `wikipedia` tool first.
2. IF the request explicitly asks for "primary source documents," "transcripts," "photographs," "letters," "diaries," or "government records," you MUST use the `dpla_search` tool. This tool is your exclusive choice for archival material.
3. The `Google Search` tool is to be used for all other tasks, such as finding recent (post-2020) information, academic articles, or answering highly specific questions that are not general overviews.
"""

class Researcher_Agent:
    def __init__(self):
        self.model = chat_groq_llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", researcher_agent_message),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
        self.google_search_tool = Tool(
            name="google_search",
            description="A general web search tool. Use this for recent events, specific questions, finding academic articles, or when other specialized tools are not appropriate.",
            func=self.search.run,
            args_schema=GoogleSearchSchema 
        )
        
        self.dpla_tool = Tool(
            name="dpla_search",
            description="Use this tool EXCLUSIVELY to find primary source documents, such as letters, government records, photographs, diary entries, or historical transcripts.",
            func=dpla_search,
            args_schema=DPLASearchSchema
        )
        
        wiki_runner = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        self.wikipedia_tool = Tool(
            name="wikipedia",
            description="Use this tool to get a broad, general summary or overview of well-known topics, people, and historical events. It is best for foundational knowledge.",
            func=wiki_runner.run,
            args_schema=WikipediaSearchSchema
        )
        self.tools = [self.dpla_tool, self.google_search_tool, self.wikipedia_tool]

        self.researcher_agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=self.prompt,
        )

    def run_research(self, plan: str) -> str:
        """Run the researcher agent on a provided research plan string and return findings."""
        if not plan:
            raise ValueError("There is no researching plan")

        

        config = {}

        response = self.researcher_agent.invoke(
            {"messages": [("user", plan)]},
            config=config
        )
        
        output = response['messages'][-1].content
        return output