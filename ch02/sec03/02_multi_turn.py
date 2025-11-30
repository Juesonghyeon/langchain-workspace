# Multi Turn
# 대화 내용을 기억
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

chat = client.chats.create(model="gemini-2.5-flash")

system_instruction = "너는 사용자를 도와주는 친절한 상담사야."

while True:
    prompt = input("사용자: ")

    if prompt == "종료":
        break

    chat_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
    )

    response = chat.send_message(message=prompt)

    print("AI상담사: " + response.text)