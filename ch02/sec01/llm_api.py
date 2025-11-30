# 모듈 설치
# 1. Gemini 모델
# uv add google-genai
# https://ai.google.dev/gemini-api/docs/quickstart
# 
# 2. 환경 변수
# uv add python-dotenv
# https://pypi.org/project/python-dotenv/
from google import genai

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
# print(gemini_api_key)

client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="대한민국의 수도는 어디야?"
)

print(response)
print("---")
print(response.text)