import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
import base64
from typing import Dict

from Research_Planning_Agent import Research_Planning_Agent
from Researcher_Agent import Researcher_Agent
from Checker_Agent import CheckerAgent
from report_agent import report_workflow

# Configuration and Initialization 

st.set_page_config(page_title="Historical Research Generator", page_icon="📚", layout="wide")

st.markdown("""
<style>
    .main-title {font-size: 2.5rem; color: #667eea; text-align: center; font-weight: bold;}
    .subtitle {text-align: center; color: #666; margin-bottom: 2rem;}
    .status-box {padding: 1.2rem; border-radius: 12px; margin: 0.8rem 0; border-left: 5px solid; transition: all 0.3s;}
    .active {background: #e3f2fd; border-color: #2196f3; box-shadow: 0 4px 12px rgba(33,150,243,0.3);}
    .complete {background: #e8f5e9; border-color: #4caf50; box-shadow: 0 2px 8px rgba(76,175,80,0.2);}
    .waiting {background: #fafafa; border-color: #e0e0e0; opacity: 0.7;}
    
    /* Make the chat area scrollable and reserve space for the input */
    .stApp > header {visibility: hidden;}
    /* Ensure chat history has some breathing room at the bottom */
    .main > div {padding-bottom: 5rem;} 
</style>
""", unsafe_allow_html=True)

# Initialize session state for all critical components
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {
        'Supervisor': 'waiting',
        'Planner': 'waiting',
        'Researcher': 'waiting',
        'Checker': 'waiting',
        'Reporter': 'waiting'
    }
if 'processing' not in st.session_state:
    st.session_state.processing = False 
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Enter your historical research query below to generate a report."}
    ]

PROCESSING_MESSAGE = "Assistant is processing your query... Please wait while the agents run. ⏳"

def check_api_keys():
    """Checks for required API keys in environment variables."""
    load_dotenv()
    keys = ["GROQ_API_KEY", "SERP_API_KEY", "DPLA_API_KEY"]
    missing = [k for k in keys if not os.getenv(k)]
    return len(missing) == 0, missing

def set_example_query(example: str):
    """Sets the example query to the st.chat_input value via its session state key."""
    st.session_state["chat_input"] = example

def render_agent_status(name: str, icon: str, desc: str, status: str, status_placeholder: st.delta_generator.DeltaGenerator):
    """Render agent status card with appropriate styling."""
    css_class = "waiting"
    status_text = "⏳ Waiting"
    
    if status == "complete":
        css_class = "complete"
        status_text = "✅ Complete"
    elif status == "active":
        css_class = "active"
        status_text = "⚡ Active - Running Now!"
    
    status_placeholder.markdown(f'''
    <div class="status-box {css_class}">
        <div style="font-size: 1.1rem;"><strong>{icon} {name}</strong></div>
        <div style="color: #666; margin: 0.3rem 0;">{desc}</div>
        <div style="font-weight: 600; color: {"#2196f3" if css_class == "active" else "#4caf50" if css_class == "complete" else "#999"};">{status_text}</div>
    </div>
    ''', unsafe_allow_html=True)

# Agent Workflow Function

def run_agent_workflow(query: str, status_placeholders: Dict[str, st.delta_generator.DeltaGenerator], progress_placeholder: st.delta_generator.DeltaGenerator):
    """Runs the multi-agent workflow and updates Streamlit status dynamically."""
    
    st.session_state.pdf_path = None 
    
    # Initialize agents
    planning_agent = Research_Planning_Agent()
    researcher_agent = Researcher_Agent()
    checker_agent = CheckerAgent()
    report_gen = report_workflow()
    
    supervisor_placeholder = status_placeholders['Supervisor']
    planner_placeholder = status_placeholders['Planner']
    researcher_placeholder = status_placeholders['Researcher']
    checker_placeholder = status_placeholders['Checker']
    reporter_placeholder = status_placeholders['Reporter']

    try:
        # Supervisor starts
        st.session_state.agent_status['Supervisor'] = 'active'
        render_agent_status("Supervisor", "🎯", "Orchestrating workflow", "active", supervisor_placeholder)
        progress_placeholder.info("🔄 Supervisor initiating workflow...")
        
        # Planner Agent
        st.session_state.agent_status['Planner'] = 'active'
        render_agent_status("Planner", "📋", "Creating research plan", "active", planner_placeholder)
        progress_placeholder.progress(5)
        progress_placeholder.info("🔄 Planning research strategy...")
        
        plan = planning_agent.run(query)
        
        st.session_state.agent_status['Planner'] = 'complete'
        render_agent_status("Planner", "📋", "Creating research plan", "complete", planner_placeholder)
        progress_placeholder.progress(25)
        
        # Researcher Agent
        st.session_state.agent_status['Researcher'] = 'active'
        render_agent_status("Researcher", "🔍", "Gathering information", "active", researcher_placeholder)
        progress_placeholder.info("🔄 Gathering historical information...")
        
        findings = researcher_agent.run_research(plan)
        
        st.session_state.agent_status['Researcher'] = 'complete'
        render_agent_status("Researcher", "🔍", "Gathering information", "complete", researcher_placeholder)
        progress_placeholder.progress(50)
        
        # Checker Agent
        st.session_state.agent_status['Checker'] = 'active'
        render_agent_status("Checker", "✅", "Verifying accuracy", "active", checker_placeholder)
        progress_placeholder.info("🔄 Verifying facts and accuracy...")
        
        checked = checker_agent.evaluate(query, findings)
        
        st.session_state.agent_status['Checker'] = 'complete'
        render_agent_status("Checker", "✅", "Verifying accuracy", "complete", checker_placeholder)
        progress_placeholder.progress(75)
        
        # Reporter Agent
        st.session_state.agent_status['Reporter'] = 'active'
        render_agent_status("Reporter", "📄", "Generating PDF", "active", reporter_placeholder)
        progress_placeholder.info("🔄 Creating PDF report...")
        
        result = report_gen.invoke({"rewritten_output": checked.rewritten_output})
        
        st.session_state.agent_status['Reporter'] = 'complete'
        render_agent_status("Reporter", "📄", "Generating PDF", "complete", reporter_placeholder)
        progress_placeholder.progress(95)
        
        # Supervisor completes
        st.session_state.agent_status['Supervisor'] = 'complete'
        render_agent_status("Supervisor", "🎯", "Orchestrating workflow", "complete", supervisor_placeholder)
        progress_placeholder.progress(100)
        
        # Final Completion
        pdf_path = result.get("pdf_path")
        st.session_state.pdf_path = pdf_path
        
        progress_placeholder.success("🎉 All agents completed successfully!")

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": f"The report for your query has been generated! You can now download the PDF or start a new query."}
        )
        
        # Run Streamlit balloons effect
        st.balloons()
        
    except Exception as e:
        # Error Handling
        error_message = f"❌ An error occurred during agent execution: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        progress_placeholder.error(error_message)
        import traceback
        st.code(traceback.format_exc())
        
    finally:
        st.session_state.processing = False
        # Rerun to display final state, error, and re-enable input
        st.rerun() 

# UI Layout 

# Header
st.markdown('<h1 class="main-title">📚 Historical Research Report Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Multi-Agent AI System for Historical Research</p>', unsafe_allow_html=True)

keys_ok, missing = check_api_keys()
if not keys_ok:
    st.error(f"⚠️ Missing API Keys: {', '.join(missing)}")
    st.stop()

col1, col2 = st.columns([1.3, 1])
with col2:
    st.subheader("📊 Agent Status")
    
    status_placeholders = {
        'Supervisor': st.empty(),
        'Planner': st.empty(),
        'Researcher': st.empty(),
        'Checker': st.empty(),
        'Reporter': st.empty()
    }
    progress_placeholder = st.empty()
    
    for name, desc, icon in [
        ('Supervisor', "Orchestrating workflow", "🎯"),
        ('Planner', "Creating research plan", "📋"),
        ('Researcher', "Gathering information", "🔍"),
        ('Checker', "Verifying accuracy", "✅"),
        ('Reporter', "Generating PDF", "📄")
    ]:
        render_agent_status(name, icon, desc, st.session_state.agent_status[name], status_placeholders[name])

with col1:
    st.subheader("💬 Research Conversation")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.pdf_path is not None or len(st.session_state.messages) > 1:
        st.markdown("---")
        
        col_d, col_n = st.columns([1, 1])

        if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
            st.subheader("Final Report")
            pdf_filename = os.path.basename(st.session_state.pdf_path)
            st.success(f"✅ Report Generated: `{pdf_filename}`")
            st.info(f"📊 Size: {os.path.getsize(st.session_state.pdf_path) / 1024:.2f} KB")

            with col_d:
                with open(st.session_state.pdf_path, "rb") as f:
                    st.download_button("📥 Download PDF", f, f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", 
                                     mime="application/pdf", use_container_width=True)

            with st.expander("📄 View PDF Report", expanded=True):
                with open(st.session_state.pdf_path, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)

        with col_n:
            if st.button("🔄 New Query", use_container_width=True):
                st.session_state.pdf_path = None
                st.session_state.processing = False
                st.session_state.agent_status = {k: 'waiting' for k in st.session_state.agent_status}
                st.session_state.messages = [{"role": "assistant", "content": "Hello! Enter your historical research query below to generate a report."}]
                st.rerun()


    with st.expander("💡 Example Query Ideas"):
        examples = [
            "Apollo 11 mission with primary sources and recent analysis",
            "Civil War Battle of Gettysburg with soldiers' letters",
            "Women's Suffrage Movement with speeches and documents",
            "Industrial Revolution workers' conditions with primary sources"
        ]
        
        for idx, ex in enumerate(examples):
            st.button(ex, key=f"ex_{idx}", on_click=set_example_query, args=(ex,), use_container_width=True)


#  Chat Input and Submission Logic 

should_hide_input = st.session_state.processing or (st.session_state.pdf_path is not None)

if not should_hide_input:
    user_query = st.chat_input(
        "Enter your research query (Press Enter to submit)...", 
        key="chat_input", 
        disabled=st.session_state.processing 
    )

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        st.session_state.messages.append({"role": "assistant", "content": PROCESSING_MESSAGE})
        
        st.session_state.processing = True 
        st.rerun() 
        
if st.session_state.processing:
    last_message = st.session_state.messages[-1]["content"] if st.session_state.messages else ""
    
    if last_message.startswith("Assistant is processing"):
        if len(st.session_state.messages) >= 2 and st.session_state.messages[-2]["role"] == "user":
            last_user_query = st.session_state.messages[-2]["content"]
            
            st.session_state.messages.pop() 
            
            run_agent_workflow(last_user_query, status_placeholders, progress_placeholder)