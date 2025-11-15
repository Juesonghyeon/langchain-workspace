import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=gemini_api_key)

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory


# 대화 기록을 저장할 히스토리 클래스 불러오기
chat_history = ChatMessageHistory()

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory


# 대화 기록을 저장할 히스토리 클래스 불러오기
chat_history = ChatMessageHistory()

chat_history.messages

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """당신은 끝말잇기 게임을 진행하는 AI 챗봇입니다. 아래는 게임 규칙입니다. 당신과 user 의 입력에서 아래 규칙이 꼭 지켜져야 하며, 지키지 않은 사람에게 패배를 알린 뒤, 끝말잇기 게임을 종료합니다.
                1. 주어진 대화 기록에서 이미 나왔던 단어를 다시 말했을 경우 패배합니다.
                2. 두음법칙을 허용합니다. (ex. 리 -> 이, 력 -> 역, 락 -> 낙)
                3. 국어사전에 존재하는 단어이자, 명사여야 합니다.
                4. 아무런 설명 없이, 끝말잇기 단어만 한글로 한 단어만 출력하세요.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
    ]
)

chain = prompt | llm

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

from langchain_core.runnables import RunnablePassthrough

def summarize_messages(chain_input):
    stored_messages = chat_history.messages
    if len(stored_messages) == 0:
        return False
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            (
                "user",
                "위 채팅 메시지는 끝말잇기 게임을 진행한 대화내용입니다. 언급한 단어들만 나열하여 저장해주세요.",
            ),
        ]
    )
    summarization_chain = summarization_prompt | llm

    # chat_history 에 저장된 대화 기록을 요약프롬프트에 입력 & 결과 저장
    summary_message = summarization_chain.invoke({"chat_history": stored_messages})

    # chat_history 에 저장되어있던 기록 지우기
    chat_history.clear()

    # 생성된 새로운 요약내용으로 기록 채우기
    chat_history.add_message(summary_message)

    return True

chain_with_summarization = (
    # RunnablePassthrough는 LCEL에서 사용, 입력값을 다음 단계로 그대로 통과시키는 역할
    # assign() 메서드는 체인에 들어오는 딕셔너리에 새로운 키-값 추가
    RunnablePassthrough.assign(messages_summarized=summarize_messages) # 새로운 키 messages_summarized에 값(True 또는 False) 할당, 이 값은 조건부 요약에 활용 가능
    | chain_with_message_history
)

# while True:
#     user_input = input("🧑 YOUR TURN : ")
#     if user_input == "종료": break
#     response = chain_with_summarization.invoke(
#                 {"input": user_input},
#                 {"configurable": {"session_id": "unused"}},
#             )
#     print("🤖 AI TURN : ", response.content) # AIMessage 객체에서 .content 추출

import random
import gradio as gr

def word_chain_response(message, history):
        response = chain_with_summarization.invoke(
                {"input": message},
                {"configurable": {"session_id": "unused"}},
            )
        return response.content

demo = gr.ChatInterface(
     word_chain_response,
     type="messages",
     autofocus=False,
     title=" 끝말잇기 게임",
     description="AI와 함께 끝말잇기 게임을 해보세요! 단어만 입력하면 됩니다.")

if __name__ == "__main__":
    demo.launch()