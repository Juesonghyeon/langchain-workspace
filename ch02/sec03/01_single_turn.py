# LLM은 기본적으로 대화를 기억하지 못함!

# Single Turn
# Turn은 대화
# 대화 내용을 기억하지 않음
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

system_instruction = "너는 사용자를 도와주는 친절한 상담사야."

while True:
    prompt = input("사용자: ")

    if prompt == "종료":
        break

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        )
    )

    print("AI상담사: " + response.text)