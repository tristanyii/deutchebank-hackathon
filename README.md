# Untapped Resource Discovery System

A multi-agent AI system designed to help users discover government and non-government resources based on their specific situation and needs.

## 🚀 Quick Start

### Setup
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   SERP_API_KEY=your_serpapi_key
   ```

### Usage Options

#### 1. **Resource Discovery Web App** (Recommended)
```bash
streamlit run resource_app.py
```
- Interactive web interface for resource discovery
- Real-time agent status updates
- Downloadable recommendations

#### 2. **Command Line Resource Discovery**
```bash
python resource_main.py
```
- Command line interface for resource discovery workflow
- Good for testing and automation

#### 3. **Legacy Historical Research** (Not fully functional)
- `main.py` and `app.py` were originally for historical research
- These files need updates to work with the current agent structure

## 🤖 How It Works

The system uses three specialized AI agents:

1. **Planning Agent** (`Research_Planning_Agent.py`): Analyzes user needs and situation
2. **Resource Finder** (`Researcher_Agent.py`): Finds government and community resources
3. **Checker Agent** (`Checker_Agent.py`): Verifies and refines recommendations

## 📋 Example Queries

- "Single mother with two kids, struggling to pay rent and buy groceries"
- "Elderly person on fixed income needing help with medical bills" 
- "Recent college graduate looking for job training and student loan help"
- "Veteran dealing with disability and housing issues"

## 🛠️ File Structure

- `resource_app.py` - Main Streamlit web application
- `resource_main.py` - Command line resource discovery workflow
- `Research_Planning_Agent.py` - Needs analysis agent
- `Researcher_Agent.py` - Resource finding agent  
- `Checker_Agent.py` - Verification and refinement agent
- `report_agent.py` - PDF report generation (used by legacy system)

## 🔧 API Keys Required

- **GROQ_API_KEY**: For LLM functionality
- **SERP_API_KEY**: For web search capabilities

## 📝 Notes

This system is designed to help people discover resources they might not know about, including:
- Government benefits and programs
- Nonprofit organizations
- Community assistance programs
- Emergency financial aid
- Healthcare resources
- Housing assistance
- Employment programs

Bridge the gap for people who don’t have access. 

Look into different groups to help out with unclaimed resoures.


# History_Report_Generator

## Multi-Agent Historical Research System
### Overview
This project implements a multi-agent system designed to generate structured historical research reports from a user-provided query. Each agent in the system has a specific role, allowing the workflow to be modular, flexible, and scalable.

### Architecture
The system consists of the following agents:
#### Research Planning Generator
 - Extracts the main topic, time period, location, and relevant groups from the user's research query.
 - Produces a structured research plan.

#### Supervisor
 - Supervises the flow of information between agents.
 - Validates outputs, ensures quality, and decides the next agent to call.

#### Search Agent
 - Performs targeted searches based on the structured plan.
 - Collects relevant historical information, and sources.

#### Report Generator Agent
 - Takes the outputs from previous agents and compiles them into a final historical report (PDF format).
 - Ensures clarity, structure, and readability.


### Setup

#### API Keys

To use this project, you’ll need **three separate API keys** from different services.  
All of these services provide **free tiers** suitable for development.

#### Groq API Key

1. Visit [GroqCloud Console](https://console.groq.com/).  
2. **Sign up** for a new account or **log in**.  
3. Go to API Keys.  
4. Click Create API Key.  
5. Save the generated key as **GROQ_API_KEY**


#### SerpApi API Key (for Google Search)

1. Go to [SerpApi website](https://serpapi.com/).  
2. Sign up for a free account.  
3. After logging in, open your Dashboard.  
4. In the left-hand menu, click API Keys.  
5. Save the generated key as **SERP_API_KEY**.


#### DPLA API Key (for Primary Source Archives)

1. Get an API key by sending a HTTP POST request,Run the following command in your cmd
   ```bash
   # Replace EXAMPLE@gmail.com with your gmail
   curl -v --ssl-no-revoke -XPOST https://api.dp.la/v2/api_key/EXAMPLE@gmail.com 
2. The API key will be sent to your email instantly.  
3. Save the generated key as **DPLA_API_KEY**.
