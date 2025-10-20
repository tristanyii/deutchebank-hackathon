import os
from typing import TypedDict, Optional, List
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from Research_Planning_Agent import Research_Planning_Agent
from Researcher_Agent import Researcher_Agent
from Checker_Agent import CheckerAgent
from report_agent import report_workflow

#1. Define the State for the Graph 
class AgentState(TypedDict):
    """
    Represents the state of our multi-agent graph.
    This dictionary will be passed and updated between nodes.
    """
    original_query: str
    plan: Optional[str]
    research_findings: Optional[str]
    checked_output: Optional[str]
    pdf_path: Optional[str]
    next: str

# 2. Instantiate Agents and the Supervisor LLM 
load_dotenv()
if not all([os.getenv("GROQ_API_KEY"), os.getenv("SERP_API_KEY"), os.getenv("DPLA_API_KEY")]):
    raise ValueError("One or more API keys are missing from .env file.")

# Instantiate the "worker" agents
planning_agent = Research_Planning_Agent()
researcher_agent = Researcher_Agent()
checker_agent = CheckerAgent()
report_generator_graph = report_workflow()

# Instantiate the "supervisor" LLM
supervisor_llm = ChatGroq(model_name="meta-llama/llama-4-scout-17b-16e-instruct", groq_api_key=os.getenv("GROQ_API_KEY"))

# 3. Define the Supervisor Node 
supervisor_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """You are a supervisor of a team of expert agents. Your job is to manage a workflow to generate a historical research report.
         Based on the current state of the project, you must decide which agent to call next.
         
         Here is the required sequence:
         1. If a 'plan' does not exist, call the 'Planner'.
         2. If a 'plan' exists but 'research_findings' do not, call the 'Researcher'.
         3. If 'research_findings' exist but 'checked_output' does not, call the 'Checker'.
         4. If 'checked_output' exists, call the 'Reporter'.
         5. Once a 'pdf_path' exists, the task is complete.
         
         **CRITICAL INSTRUCTION:** Your response MUST be ONLY a single word from the following list:
         - Planner
         - Researcher
         - Checker
         - Reporter
         - FINISH
         
         Do NOT provide any explanation, preamble, or any other text.
         
         Given the following state, what is the next step?
         State:
         {state}
         """),
        ("user", "Respond with a single word indicating the next agent to call."),
    ]
)

supervisor_chain = supervisor_prompt | supervisor_llm

def supervisor_node(state: AgentState):
    print("\n--- [SUPERVISOR] Evaluating next step... ---")
    # The supervisor makes a decision
    response = supervisor_chain.invoke({"state": state})
    next_agent = response.content.strip()
    print(f"--- [SUPERVISOR] Decision: Call '{next_agent}' ---")
    return {"next": next_agent}

# 4. Define Worker Node Functions 

def run_planner_node(state: AgentState):
    print("--- [NODE] EXECUTING PLANNING AGENT ---")
    plan = planning_agent.run(state['original_query'])
    print("Plan Generated.")
    return {"plan": plan}

def run_researcher_node(state: AgentState):
    print("--- [NODE] EXECUTING RESEARCHER AGENT ---")
    findings = researcher_agent.run_research(state['plan'])
    print("Research Findings Compiled.")
    return {"research_findings": findings}

def run_checker_node(state: AgentState):
    print("--- [NODE] EXECUTING CHECKER AGENT ---")
    check_result = checker_agent.evaluate(
        agent_input=state['original_query'],
        agent_output=state['research_findings']
    )
    print("Findings Checked and Verified.")
    return {"checked_output": check_result.rewritten_output}

def run_reporter_node(state: AgentState):
    print("--- [NODE] EXECUTING REPORT GENERATOR ---")
    report_input = {"rewritten_output": state['checked_output']}
    final_report_state = report_generator_graph.invoke(report_input)
    print("PDF Report Generated.")
    return {"pdf_path": final_report_state.get("pdf_path")}


# 5. Build the Graph 
def build_workflow():
    """Build and return the compiled workflow graph"""
    workflow = StateGraph(AgentState)

    # Add the nodes
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Planner", run_planner_node)
    workflow.add_node("Researcher", run_researcher_node)
    workflow.add_node("Checker", run_checker_node)
    workflow.add_node("Reporter", run_reporter_node)

    # Define the edges
    workflow.set_entry_point("Supervisor")
    
    workflow.add_edge("Planner", "Supervisor")
    workflow.add_edge("Researcher", "Supervisor")
    workflow.add_edge("Checker", "Supervisor")
    workflow.add_edge("Reporter", "Supervisor")

    workflow.add_conditional_edges(
        "Supervisor",
        lambda x: x["next"],
        {
            "Planner": "Planner",
            "Researcher": "Researcher",
            "Checker": "Checker",
            "Reporter": "Reporter",
            "FINISH": END,
        },
    )

    # Compile the graph
    return workflow.compile()


def visualize_graph(app, output_file="workflow_graph.png"):
    """Generate and save a visualization of the workflow graph"""
    try:
        from IPython.display import Image, display
        
        # Generate the graph visualization
        graph_image = app.get_graph().draw_mermaid_png()
        
        # Save to file
        with open(output_file, "wb") as f:
            f.write(graph_image)
        
        print(f"Graph visualization saved to: {output_file}")
        
        # Try to display if in Jupyter
        try:
            display(Image(graph_image))
        except:
            print("(Display only works in Jupyter notebooks)")
            
        return output_file
    except Exception as e:
        print(f"⚠️ Could not generate graph visualization: {e}")
        return None


def run_workflow(user_query: str, app=None):
    """Run the workflow with a given query"""
    if app is None:
        app = build_workflow()
    
    print(f"\nStarting research process for query: '{user_query}'")
    print("\n--- [GRAPH] INVOKING THE SUPERVISOR WORKFLOW ---")
    
    initial_state = {"original_query": user_query}
    
    try:
        final_state = app.invoke(initial_state)
        pdf_path = final_state.get("pdf_path")
        
        print("\n--- [GRAPH] PROCESS COMPLETE ---")
        print(f"\n Success! Your report has been generated.")
        print(f" You can find it here: {os.path.abspath(pdf_path)}")
        
        return final_state, pdf_path
        
    except Exception as e:
        print(f"\n An error occurred during the graph execution: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def main():
    print("🔑 Environment variables loaded.")
    
    # Build the workflow
    app = build_workflow()
    
    # Visualize the graph
    print("\n Generating workflow visualization...")
    visualize_graph(app)
    
    # Example query
    user_query = "Create a comprehensive report on the Apollo 11 mission. Start with a general summary of the mission's objectives and key astronauts involved. Then, find specific primary source documents, like official NASA mission transcripts or original photographs from the landing. Finally, include a summary of recent (post-2020) academic discussions or articles about the scientific and engineering challenges of returning to the moon."
    
    # Run the workflow
    run_workflow(user_query, app)


if __name__ == "__main__":
    main()