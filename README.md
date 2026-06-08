# 🔬 Multi-Agent Research Assistant

An AI-powered multi-agent research assistant that automatically searches the web, synthesizes data, and generates executive-ready Markdown reports based on your custom topic and project description.

Built with **Streamlit**, **CrewAI**, and **Google Gemini**.

---

## 🚀 Features

*   **Project-Driven Context:** Tailor the research depth and writing tone by providing a specific project description (e.g., *Executive Briefing, Technical Deep-Dive, Market Analysis*).
*   **Multi-Agent Coordination:** Leverages CrewAI to coordinate three specialized agents:
    1.  **Senior Research Analyst:** Hunts for high-quality data using optimized search queries.
    2.  **Data Synthesis Specialist:** Filters noise, groups themes, and extracts key metrics.
    3.  **Chief Technical Writer:** Polishes the final output into clean, structured Markdown.
*   **Smart Web Search:** Powered by Tavily API, an AI-native search engine designed to return clean snippets instead of messy HTML clutter.
*   **Instant Export:** Download your generated research report as a `.md` file with a single click.

---

## 🛠️ Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/)
*   **Agent Framework:** [CrewAI](https://www.crewai.com/)
*   **LLM Backend:** [Google Gemini 1.5 Flash](https://ai.google.dev/) (via LangChain)
*   **Search Tool:** [Tavily API](https://tavily.com/)

---

## 📋 Prerequisites

Before running the application, make sure you have:
1.  Python 3.10 or higher installed.
2.  A **Google Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/)).
3.  A **Tavily API Key** (Get one from [Tavily](https://tavily.com/)).

---

## 🔧 Installation & Setup

1. **Clone the Repository:**

         git clone https://github.com/at9596/multi_agent_research_assistant
         cd multi_agent_research_assistant

2. Install Dependencies:

         pip install streamlit crewai langchain-google-genai tavily-python

3. Run the Application:

         streamlit run app.py
          
