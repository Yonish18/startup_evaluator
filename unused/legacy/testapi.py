from openai import OpenAI

client = OpenAI()  # This uses your OPENAI_API_KEY from environment automatically

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "what's RAG"}]
)

print(response.choices[0].message.content)


