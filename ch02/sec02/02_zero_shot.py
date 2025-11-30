from google import genai
from google.genai import types

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

system_instruction = "너는 유치원 학생이야. 유치원생처럼 답변해줘"

# 프롬프트 엔지니어링
# 대규모 언어 모델(LLM)과 같은 인공지능이
# 최적의 결과를 생성하도록 
# 입력 프롬프트를 설계하고 
# 최적화하는 기술
# - 원샷 프롬프팅(예제 1개 있음)
# - 퓨샷 프롬프팅(예제 2개 이상 있음)

# - 제로샷 프롬프팅(예제 없음)
prompt = "참새"

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction
    )
)

print(response.text)