from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

messages = []

while True:
    user_input = input("User: ")

    if user_input.strip().lower() in ("exit","quit"):
        break

    messages.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )

    reply = response.text


    messages.append({
        "role": "model",
        "parts": [{"text": reply}]
    })

    print("Bot:", reply)


    
