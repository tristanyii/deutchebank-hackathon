# Excess - AI Voice Support Line

**🏆 1st Place Winner - Deutsche Bank Hackathon 2024**

An AI-powered voice support line that helps underrepresented communities discover verified local aid programs through simple, human-like interactions. Using voice as the interface makes it accessible to people who may not have internet access or experience with technology.

## 🎯 **Project Overview**

**Excess** addresses a critical problem: millions of people across the U.S. qualify for housing, food, and energy assistance, yet many never receive it because the information is confusing, scattered, or entirely offline.

### **Our Solution:**
- **🎙️ Voice-First Interface**: Makes aid discovery accessible to people without internet access or technology experience
- **🌍 Multilingual Support**: Serves diverse and rural communities in their native languages  
- **🗺️ Real-Time Visualization**: Web app shows nearby resources and assistance options
- **💰 Cost Effective**: Operates at ~60% lower cost than traditional human-operated support lines

## 🚀 **How It Works**

1. **Voice Input**: Users call the support line and speak naturally
2. **AI Processing**: Anthony (our AI agent) understands their needs in multiple languages
3. **Resource Matching**: System identifies relevant U.S. government and nonprofit programs
4. **Guided Assistance**: Provides step-by-step guidance and application links
5. **Visualization**: Web app shows nearby resources on an interactive map

## 🛠️ **Components**

### **1. Voice AI Backend** (`flask_backend/`)
- **Anthony Persona**: Multilingual AI agent for natural conversations
- **Retell AI Integration**: Processes voice calls and SMS
- **Resource Matching**: Connects users to LIHEAP, Housing, and Benefits programs
- **Conversation Management**: Tracks user needs and provides personalized assistance

### **2. Web Application** (`webapp/`)
- **Interactive Map**: Visualizes nearby resources in real-time
- **Resource Browser**: Browse available housing, food, and energy programs
- **User Interface**: Clean, accessible design for all users

### **3. Resource Discovery System**
- **Multi-Agent AI**: Specialized agents for needs analysis and resource finding
- **Government Programs**: LIHEAP, HUD housing, SNAP, Medicaid, and more
- **Nonprofit Resources**: Community organizations and local assistance

## 🚀 **Quick Start**

### **Setup**
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   SERP_API_KEY=your_serpapi_key
   ```

### **Usage Options**

#### **1. Voice AI Backend** (New!)
```bash
cd flask_backend
./start.sh
```
- **Anthony AI Agent**: Multilingual voice support for phone calls
- **Retell AI Integration**: Handles voice calls and SMS
- **Real-time Processing**: Instant responses in 10 languages

#### **2. Web Application**
```bash
cd webapp/my-app
npm install
npm run dev
```
- **Interactive Map**: Visualize nearby resources
- **Resource Browser**: Browse available programs
- **Modern UI**: Clean, accessible design

#### **3. Resource Discovery System**
```bash
streamlit run resource_app.py
```
- **Multi-Agent AI**: Specialized agents for needs analysis
- **Government Programs**: LIHEAP, HUD housing, SNAP, Medicaid
- **Nonprofit Resources**: Community organizations and local assistance

## 📋 **Example Use Cases**

- **"I need help with my energy bills"** → Anthony connects to LIHEAP programs
- **"I'm looking for affordable housing"** → System finds HUD and local housing resources  
- **"I need food assistance"** → Connects to SNAP, food banks, and community programs
- **"I lost my job and need help"** → Provides unemployment, job training, and emergency assistance

## 🏛️ **U.S. Resources Provided**

Anthony always provides these three core resources to ensure comprehensive assistance:

### **1. LIHEAP (Energy Bill Help)**
- **Purpose**: Helps pay heating or cooling bills
- **Eligibility**: Based on ZIP code and income
- **Link**: https://www.acf.hhs.gov/ocs/energy-assistance
- **Requirements**: photo ID, proof of address, recent bill, income proof

### **2. Housing Resources**
- **Purpose**: HUD helps find rental and affordable housing
- **Coverage**: State-specific housing programs
- **Link**: https://www.hud.gov/states

### **3. Unclaimed Benefits Finder**
- **Purpose**: Checks for food, health, cash aid, tax credits
- **Process**: Quick and private screening
- **Link**: https://www.benefits.gov/benefit-finder

## 🛠️ **File Structure**

### **Voice AI Backend** (`flask_backend/`)
- `app.py` - Main Flask application with Anthony persona
- `utils.py` - Utility functions for voice formatting
- `run_server.py` - Server runner script
- `test_integration.py` - Integration testing script

### **Web Application** (`webapp/`)
- `my-app/` - Next.js web application
- `components/` - React components for map and chatbot
- `data/` - Resource data and placeholders

### **Resource Discovery System**
- `resource_app.py` - Main Streamlit web application
- `resource_main.py` - Command line resource discovery workflow
- `Research_Planning_Agent.py` - Needs analysis agent
- `Researcher_Agent.py` - Resource finding agent  
- `Checker_Agent.py` - Verification and refinement agent

## 🔧 API Keys Required

- **GROQ_API_KEY**: For LLM functionality
- **SERP_API_KEY**: For web search capabilities

## 🎯 **Impact & Results**

- **🏆 1st Place**: Deutsche Bank Hackathon 2024
- **💰 Cost Reduction**: ~60% lower operational costs than human support lines
- **🌍 Accessibility**: Serves communities without internet access
- **📞 Voice-First**: Natural conversation interface for all users
- **🔍 Comprehensive**: Covers energy, housing, food, and financial assistance

## 👥 **Team**
**Excess** was created by the winning team at Deutsche Bank Hackathon 2024:
- **Uttam Dev Sapkota**
- **Anna Benbow** 
- **Tahia Islam**
- **Rama Yakkala**

**Mentors**: Meghna Gaddam and Anil Pandya

## 🎉 **Recognition**
- **🏆 1st Place Winner** - Deutsche Bank Hackathon 2024
- **💡 Innovation Award** - AI-powered accessibility solution
- **🌍 Social Impact** - Serving underrepresented communities

## 📝 **Mission**

This system is designed to help people discover resources they might not know about, including:
- Government benefits and programs
- Nonprofit organizations
- Community assistance programs
- Emergency financial aid
- Healthcare resources
- Housing assistance
- Employment programs

**Bridge the gap for people who don't have access.**


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
