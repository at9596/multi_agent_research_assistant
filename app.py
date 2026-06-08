import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
import os

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🔬", layout="wide")

st.title("🔬 Multi-Agent Research Assistant")
st.caption("Powered by Gemini, CrewAI, and Tavily")

# --- Sidebar for API Keys ---
with st.sidebar:
    st.header("🔑 API Configuration")
    gemini_key = st.text_input("Google Gemini API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("1. **Researcher Agent** finds high-quality sources.\n"
                "2. **Summarizer Agent** extracts key insights.\n"
                "3. **Writer Agent** compiles a polished Markdown report.")

# --- Verification & Setup ---
if not gemini_key or not tavily_key:
    st.info("Please enter your Gemini and Tavily API keys in the sidebar to get started.")
    st.stop()

# Set environment variables for CrewAI/LangChain internally
os.environ["GOOGLE_API_KEY"] = gemini_key

# --- Initialize Gemini LLM ---
# Using gemini-1.5-flash for speed and cost-efficiency, or gemini-1.5-pro for deeper reasoning
llm = LLM(
    model="gemini/gemini-2.5-flash", 
    temperature=0.3,
    api_key=gemini_key
)

# --- Define Custom Search Tool ---
@tool("Web Search Tool")
def web_search(query: str) -> str:
    """Searches the internet for highly relevant information on a given topic."""
    tavily = TavilyClient(api_key=tavily_key)
    response = tavily.search(query=query, max_results=5, search_depth="advanced")
    
    # Format results nicely for the agent
    results = []
    for item in response.get("results", []):
        results.append(f"Title: {item['title']}\nURL: {item['url']}\nSnippet: {item['content']}\n---")
    return "\n".join(results)


# --- User Input Form ---
with st.form("research_form"):
    topic = st.text_input("What topic do you want to research?", placeholder="e.g., Quantum Computing breakthroughs in 2026")
    specific_focus = st.text_area("Any specific focus areas or questions? (Optional)", placeholder="e.g., Focus on commercial viability and major tech players.")
    submit_button = st.form_submit_button("Launch Research Team")

# --- Agentic Workflow Execution ---
if submit_button and topic:
    with st.spinner("🤖 The agents are collaborating on your report... This may take a minute."):
        
        # 1. Define Agents
        researcher = Agent(
            role="Senior Research Analyst",
            goal=f"Gather comprehensive, accurate, and up-to-date data on: {topic}",
            backstory="You are an expert researcher known for finding hidden insights, vetting sources, and avoiding surface-level summaries.",
            tools=[web_search],
            llm=llm,
            verbose=True
        )

        summarizer = Agent(
            role="Data Synthesis Specialist",
            goal="Condense raw search data into highly structured, actionable insights and key takeaways.",
            backstory="You excel at filtering out noise, identifying core trends, cross-referencing facts, and organizing messy data.",
            tools=[], # Uses analytical skills, doesn't need to search
            llm=llm,
            verbose=True
        )

        writer = Agent(
            role="Chief Technical Writer",
            goal="Transform synthesis reports into beautiful, executive-ready Markdown documents.",
            backstory="You are a master of clarity, structure, and professional tone. You turn dry technical findings into engaging, easy-to-read reports.",
            tools=[],
            llm=llm,
            verbose=True
        )

        # 2. Define Tasks
        task_search = Task(
            description=f"Conduct thorough research on '{topic}'. Focus depth on: {specific_focus if specific_focus else 'General overview and recent developments'}. Find at least 3-5 distinct angles or data points.",
            expected_output="A raw compilation of verified search results, statistics, and source details.",
            agent=researcher
        )

        task_summarize = Task(
            description="Review the raw research results. Group findings into thematic categories, extract key metrics, and highlight conflicting viewpoints or consensus trends.",
            expected_output="A highly structured bulleted brief outlining the core pillars of the research.",
            agent=summarizer
        )

        task_write = Task(
            description=f"Take the summary brief and draft a comprehensive, professional research report about '{topic}'. Use clean Markdown headings, tables if applicable, bold terms for emphasis, and include a 'Key Takeaways' section at the top.",
            expected_output="A beautifully formatted Markdown report ready for presentation.",
            agent=writer
        )

        # 3. Assemble the Crew
        crew = Crew(
            agents=[researcher, summarizer, writer],
            tasks=[task_search, task_summarize, task_write],
            process=Process.sequential # Task 1 feeds into Task 2, which feeds into Task 3
        )

        # 4. Kickoff and Capture Output
        try:
            result = crew.kickoff()
            
            # --- Display Results ---
            st.success("✅ Research Complete!")
            
            st.markdown("---")
            st.header("📄 Generated Research Report")
            
            # CrewAI returns a CrewOutput object; raw contains the final string response
            st.markdown(result.raw)
            
            # Allow user to download the generated markdown file
            st.download_button(
                label="📥 Download Report as Markdown",
                data=result.raw,
                file_name=f"{topic.lower().replace(' ', '_')}_report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"An error occurred during execution: {e}")