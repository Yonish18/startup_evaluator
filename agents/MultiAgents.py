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

