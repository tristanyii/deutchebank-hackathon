# Untapped_Resource_Agent.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests 

load_dotenv() 

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
if not all([GROQ_API_KEY, SERP_API_KEY]):
    raise ValueError("GROQ_API_KEY and SERP_API_KEY are required in .env file.")

llm = "meta-llama/llama-4-scout-17b-16e-instruct"
chat_groq_llm = ChatGroq(model_name=llm, groq_api_key=GROQ_API_KEY)

def government_resource_search(query: str) -> str:
    """ Find government programs based on query.    """
    # Define common government resource categories and agencies
    resource_categories = {
        "financial assistance": [
            "SNAP (Supplemental Nutrition Assistance Program)",
            "TANF (Temporary Assistance for Needy Families)", 
            "SSI (Supplemental Security Income)",
            "Medicaid",
            "Housing Choice Voucher Program (Section 8)",
            "Low Income Home Energy Assistance Program (LIHEAP)"
        ],
        "healthcare": [
            "Medicare",
            "Medicaid", 
            "Community Health Centers",
            "Veterans Health Administration",
            "Indian Health Service",
            "Children's Health Insurance Program (CHIP)"
        ],
        "housing": [
            "HUD Public Housing",
            "Housing Choice Voucher Program",
            "Rural Housing Programs (USDA)",
            "Veterans Housing Programs",
            "Native American Housing Programs",
            "Homeless Assistance Programs"
        ],
        "employment": [
            "Workforce Innovation and Opportunity Act (WIOA)",
            "Unemployment Insurance",
            "Job Corps",
            "Trade Adjustment Assistance",
            "Veterans Employment Programs",
            "Disability Employment Programs"
        ],
        "education": [
            "Pell Grant Program",
            "Federal Student Loans",
            "Head Start Program",
            "Special Education Services",
            "Adult Education Programs",
            "Veterans Education Benefits (GI Bill)"
        ]
    }
    
    query_lower = query.lower()
    matched_resources = []
    for category, resources in resource_categories.items():
        if any(keyword in query_lower for keyword in category.split()):
            matched_resources.extend([f"{category.title()} - {r}" for r in resources])

    if not matched_resources:
        matched_resources = [
            "211 (Dial 2-1-1 for local resources)",
            "Benefits.gov - Find government benefits",
            "Social Services Administration (local office)",
            "Community Action Agencies",
            "Salvation Army",
            "United Way"
        ]
    
    result = "Government and Community Resources:\n\n"
    result += "\n".join(f"{i+1}. {r}" for i, r in enumerate(matched_resources[:10]))
    return result

class QuerySchema(BaseModel):
    query: str


def nonprofit_search(query: str) -> str:
    """
    Searches for nonprofit and community resources based on the user's query.
    """
    nonprofit_categories = {
        "food assistance": [
            "Local Food Banks",
            "Feeding America Network", 
            "Meals on Wheels",
            "Soup Kitchens",
            "Community Gardens",
            "Church Food Pantries"
        ],
        "housing assistance": [
            "Habitat for Humanity",
            "Salvation Army Housing Programs",
            "Local Homeless Shelters",
            "Catholic Charities Housing",
            "United Way Housing Programs",
            "Community Action Agencies"
        ],
        "healthcare": [
            "Federally Qualified Health Centers (FQHC)",
            "Free Clinics Association",
            "Planned Parenthood",
            "Community Mental Health Centers",
            "Lions Club Vision Programs",
            "American Red Cross Health Services"
        ],
        "financial assistance": [
            "United Way Emergency Financial Assistance",
            "Salvation Army Financial Aid",
            "Catholic Charities Emergency Services",
            "Local Community Foundation Grants",
            "Churches and Faith-Based Aid",
            "Goodwill Financial Counseling"
        ],
        "employment": [
            "Goodwill Job Training",
            "YMCA Employment Programs", 
            "Local Workforce Development Boards",
            "Dress for Success",
            "Career Centers",
            "Volunteer Organizations"
        ]
    }
    
    query_lower = query.lower()
    matched_resources = []
    
    for category, resources in nonprofit_categories.items():
        if any(keyword in query_lower for keyword in category.split()):
            matched_resources.extend([f"{category.title()} - {r}" for r in resources])
    
    if not matched_resources:
        matched_resources = [
            "United Way (Call 211)",
            "Salvation Army",
            "Catholic Charities",
            "Local Community Action Agency",
            "American Red Cross",
            "Goodwill Industries",
            "Local Faith-Based Organizations",
            "Community Foundation"
        ]
    
    result = "Available Nonprofit and Community Resources:\n\n"
    result += "\n".join(f"{i+1}. {r}" for i, r in enumerate(matched_resources[:10]))
    return result

single_agent_prompt="""
You are a Untapped Resource Assistant Agent for housing resources.
You help users find both government and nonprofit resources based on their needs.

Follow this process:
1. Analyze the user's request to determine the required resource type. 
2. **Prioritize** the internal tools (`government_resource_search` or `nonprofit_search`) first.
3. **ONLY use the `Google Search` tool if the user asks for specific, current, or external information** (e.g., "what is the *latest* eligibility for LIHEAP", "contact details for NYC food banks", or information *not covered* by the internal tools).
4. Always output a short structured summary:
   - Government Resources
   - Nonprofit Resources
   - Next Steps
"""

class ResourceAgent:
    def __init__(self):
        self.model = chat_groq_llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", single_agent_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
        self.search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
        self.tools = [
            Tool(
                name="government_resource_search",
                description="Finds federal/state programs and benefits.",
                func=government_resource_search,
                args_schema=QuerySchema
            ),
            Tool(
                name="nonprofit_search",
                description="Finds nonprofit organizations and community support services.",
                func=nonprofit_search,
                args_schema=QuerySchema
            ),
            Tool(
                name="google_search",
                description="Finds the latest program info, eligibility updates, or contact info.",
                func=self.search.run,
                args_schema=QuerySchema
            )
        ]
           
        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=self.prompt
        )

    def find_resources(self, query: str) -> str:
        if not query:
            raise ValueError("Please provide a description of your situation or needs.")
        
        response = self.agent.invoke({"messages": [("user", query)]})
        final_message = response["messages"][-1]
        
        # Check if the final message has content and is not just a final ToolCall
        if final_message.content:
             return final_message.content
        else:
             for msg in reversed(response["messages"]):
                 if msg.content:
                     return msg.content
             return "Agent concluded the task but did not provide a final answer."