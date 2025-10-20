import os
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from dotenv import load_dotenv

# Load environment variables for local execution
load_dotenv()


GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
  raise ValueError("GROQ_API_KEY key not found. Please add it to your .env file.")

llm = "meta-llama/llama-4-scout-17b-16e-instruct"
chat_groq_llm = ChatGroq(model_name=llm, groq_api_key=GROQ_API_KEY)

class ReportState(TypedDict):
    rewritten_output: str
    formatted_text: Optional[str]
    pdf_path: Optional[str]
    final_response: Optional[str]

def format_and_create_pdf(content:str, filename: str) -> str:
    file_path = f"./{filename}"

    doc = SimpleDocTemplate(file_path, pagesize=letter,
                            leftMargin=1*inch, bottomMargin=1*inch,
                            topMargin=1*inch, rightMargin=1*inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        spaceAfter=30,
        alignment=1
    )
    body_style = styles['BodyText']

    story = []

    title = Paragraph("Historical Research Report", title_style)
    story.append(title)

    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            story.append(Paragraph(line.lstrip('# ').strip(), styles['h2']))
        else:
            story.append(Paragraph(line, body_style))
        story.append(Spacer(1, 0.1*inch))

    doc.build(story)
    return file_path

def generator_node(state: ReportState) -> ReportState:
    rewritten_output = state["rewritten_output"]
    final_response = rewritten_output 

    pdf_path = format_and_create_pdf(final_response, "Historical_Research_Report.pdf")

    print(f"✅ PDF report generated: {pdf_path}")

    return {
        "rewritten_output": state["rewritten_output"],
        "pdf_path": pdf_path,
        "final_response": final_response
    }

def report_workflow():
    graph = StateGraph(ReportState)
    graph.add_node("report_generator", generator_node)
    graph.set_entry_point("report_generator")
    graph.add_edge("report_generator", END)
    return graph.compile()