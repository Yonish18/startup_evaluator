import requests
import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
serper_key = os.getenv("SERPER_API_KEY")

url = "https://google.serper.dev/search"
headers = {
    "X-API-KEY": serper_key,
    "Content-Type": "application/json"
}
data = {
    "q": "What is RAG?"
}

response = requests.post(url, headers=headers, json=data)
results = response.json()
print(results)