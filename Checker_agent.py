# Checker Agent 
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from dataclasses import dataclass
import os, json

# Make sure GROQ_API_KEY is set
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment.")

# Initialize ChatGroq LLM
llm_model = "meta-llama/llama-4-scout-17b-16e-instruct"
chat_groq_llm = ChatGroq(model_name=llm_model, groq_api_key=GROQ_API_KEY)

@tool
def check_agent_output(agent_input: str, agent_output: str) -> str:
    """
    Evaluates whether the agent_output is realistic, reliable, and well-supported
    based on the original agent_input.
    Returns a JSON string containing:
      - overall_score
      - verdict (reliable/questionable/unreliable)
      - reasons
      - suggested_fixes
      - evidence_snippets
    """
    prompt = f"""
    You are a historical fact-checker. Your task is to evaluate the provided "AGENT OUTPUT" for factual accuracy. Do not add any new information, quotes, or citations. Your role is only to verify.

    AGENT INPUT (for context):
    '''{agent_input}'''

    AGENT OUTPUT (to be checked):
    '''{agent_output}'''

    Return ONLY JSON with this schema. Be highly critical.
    {{
        "overall_score": float,
        "verdict": "reliable"|"questionable"|"unreliable",
        "reasons": [{{"type": "accuracy_check" | "source_verification", "message": str, "severity": "low|medium|high"}}],
        "suggested_fixes": [str],
        "evidence_snippets": [],
        "checks_performed": ["factual_accuracy_verification"]
    }}
    """
    response = chat_groq_llm.invoke(prompt)
    # Ensure JSON output
    text = response.content
    try:
        # Extract JSON if there is extra text
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            json_text = text[start:end+1]
            json.loads(json_text)  
            return json_text
    except:
        pass
    # fallback
    return json.dumps({"overall_score": 0.5, "verdict": "questionable", "reasons": [{"type":"llm_failure","message":"Could not parse JSON","severity":"medium"}], "suggested_fixes": [], "evidence_snippets": [], "checks_performed":["basic_check"]})

@tool
def rewrite_agent_output(agent_output: str, suggested_fixes: List[str]) -> str:
    """
    Rewrites the agent_output based on suggested fixes. Uses conservative wording and marks uncertain facts.
    Returns the corrected paragraph.
    """
    fixes_text = "\n".join(f"- {f}" for f in suggested_fixes)
    prompt = f"""
    You are an editor. Given the following paragraph and a list of suggested fixes,
    rewrite the paragraph applying all fixes. Use conservative wording for uncertain facts.

    ORIGINAL PARAGRAPH:
    '''{agent_output}'''

    SUGGESTED FIXES:
    {fixes_text}

    Return ONLY the rewritten paragraph text.
    """
    response = chat_groq_llm.invoke(prompt)
    return response.content.strip()

checker_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an Editor and Proofreader. Your task is to review the following research text for clarity, factual accuracy, and grammatical correctness.

    Your Mandate is Strict:
    1.  Read the entire text to understand its content and flow.
    2.  Correct any spelling mistakes, grammatical errors, or awkward phrasing.
    3.  Ensure the facts presented are coherent and logical.

    CRITICAL INSTRUCTION: You MUST PRESERVE the original level of detail and length.
    1. DO NOT SUMMARIZE the content.
    2. DO NOT REMOVE sections or paragraphs.
    3. DO NOT INVENT new information, quotes, or citations.

    Your output should be a refined, proofread, full-length version of the original input text.
    """),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

checker_tools = [check_agent_output, rewrite_agent_output]

checker_agent_runnable = create_tool_calling_agent(
    llm=chat_groq_llm,
    tools=checker_tools,
    prompt=checker_prompt
)

checker_executor = AgentExecutor(agent=checker_agent_runnable, tools=checker_tools, verbose=True, return_intermediate_steps=True)

class CheckerState(TypedDict):
    agent_input: str
    agent_output: str
    check_result: str
    rewritten_output: str

@dataclass
class CheckResult():
    check_result: str
    rewritten_output: str

class CheckerAgent:
    def __init__(self):
        self.chat_groq_llm = chat_groq_llm
        self.tools = [check_agent_output, rewrite_agent_output]
        self.workflow = StateGraph(CheckerState)
        self.workflow.add_node("checker", CheckerAgent.checker_node)
        self.workflow.set_entry_point("checker")
        self.workflow.add_edge("checker", END)
        self.compiled_graph = self.workflow.compile()

    @staticmethod
    def checker_node(state: CheckerState) -> dict:
        print("--- EXECUTING CHECKER NODE ---")
        check_json = check_agent_output(state["agent_input"], state["agent_output"])
        state["check_result"] = check_json

        # Parse suggested fixes
        try:
            parsed = json.loads(check_json)
            fixes = parsed.get("suggested_fixes", [])
        except:
            fixes = []

        # Rewrite only if fixes exist
        if fixes:
            rewritten = rewrite_agent_output(state["agent_output"], fixes)
            state["rewritten_output"] = rewritten
        else:
            state["rewritten_output"] = state["agent_output"]

        return {"check_result": state["check_result"], "rewritten_output": state["rewritten_output"]}
    
    def evaluate(self, agent_input: str, agent_output: str) -> CheckResult:
        state = {
            "agent_input": agent_input,
            "agent_output": agent_output,
            "check_result": "",
            "rewritten_output": ""
        }
        final_state = self.compiled_graph.invoke(state)
        return CheckResult(
            check_result=final_state["check_result"],
            rewritten_output=final_state["rewritten_output"]
        )
