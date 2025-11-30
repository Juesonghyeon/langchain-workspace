from google import genai

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
MODEL_ID = "gemini-2.5-flash"

def summarize_txt(file_path: str) -> str:
    client = genai.Client(api_key=gemini_api_key)

    file_ref = client.files.upload(file=file_path)

    system_prompt = """
이 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약하라.
작성해야하는 포맷은 다음과 같다.

# 제목

## 저자의 문제 인식 및 주장 (15문장 이내)

## 저자 소개
"""

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[file_ref, system_prompt]
    )

    return response.text


summary = summarize_txt("output\\output_pypdf.txt")

# print(summary)

with open("output/out_pypdf_summary.md", "w", encoding="utf-8") as f:
    f.write(summary)