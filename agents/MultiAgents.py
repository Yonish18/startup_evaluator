import warnings
warnings.filterwarnings('ignore')

import os
import crewai

openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4.1'
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

industry = 'Artificial Intelligence'

data_analyst_agent = Agent(
    role="Market Analyst Agent",
    goal= "Monitor and analyze market data in real-time "
         "to identify market trends and competitors in the client's startup's industry",
    backstory="Specializing in financial markets and venture capital, this agent "
              "uses statistical modeling and machine learning "
              "to provide crucial insights. With a knack for data, "
              "Agent is the cornerstone for "
              "informing Venture capital Funds about latest innovative startups.",
    verbose=True,
    allow_delegation=False,
    tools = [scrape_tool, search_tool]
)

data_analysis_task = Task(

    description=(
    "Continuously monitor and analyze market data for "
    "the selected startup industry ({{ industry }}). "
    "Use statistical modeling and machine learning to identify trends and competitors."
    )
    ),
expected_output=(
        "Insights and alerts about significant market "
        f"opportunities or threats for making a startup in {industry} industry."
    ),
agent=data_analyst_agent,
)

