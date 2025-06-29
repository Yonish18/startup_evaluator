from openai import OpenAI

chat_history = [{"role": "system", "content": "You are a FINRA approved financial analyst. You are also a CFA Institute certified Chartered Financial Analyst. You offer the best possible securities trading advice to your clients"}
                
                ]
client = OpenAI()

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "end"]:
        break
    chat_history.append({"role": "user", "content" : user_input})
    response = client.chat.completions.create( model="gpt-4o", 
                messages= chat_history)
    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    print("AI:", reply, sep = " ")