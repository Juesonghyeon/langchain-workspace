import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt

import os
from dotenv import load_dotenv
load_dotenv()

st.title("📄PDF 기반 QA")

if not os.path.exists(".cache"): # * 폴더 앞에 .을 붙이면 숨김 처리함(Linux, macOS)을 의미
    os.mkdir(".cache")
    # * Windows에서 .cache 폴더를 숨김 처리
    if os.name == 'nt':
        os.system('attrib +h .cache')

if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

@st.cache_resource(show_spinner="업로드한 파일을 처리 중입니다...")
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

def create_chain(prompt_filepath):
    prompt = load_prompt(prompt_filepath, encoding="utf-8")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0)

    output_parsers = StrOutputParser()

    chain = prompt | llm | output_parsers

    return chain


def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role, message):
    st.session_state["messages"].append(
        ChatMessage(role=role, content=message))

# * 대화 초기화
def clear_task():
    st.session_state["messages"] = []

with st.sidebar:
    clear_btn = st.button("대화 초기화", on_click=clear_task) # * on_click 인자로 clear_task 함수를 직접 호출

    uploaded_file = st.file_uploader("파일 업로드", type=["pdf"])

    selected_prompt = "prompts/pdf-rag.yaml"

# print("selected_prompt:", selected_prompt)

if uploaded_file:
    embed_file(uploaded_file)

user_input = st.chat_input("궁금한 내용을 물어보세요!")

print_messages()

if user_input:
    st.chat_message("user").write(user_input)

    chain = create_chain(selected_prompt)
    response = chain.stream({"question": user_input, "context": ""})

    with st.chat_message("assistant"):
        container = st.empty()

        ai_answer = ""

        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    add_message("user", user_input)
    add_message("assistant", ai_answer)

print("st.session_state.messages:", st.session_state.messages)

#  본 연구에서 Private LLM 구축을 위해 수집한 문서의 총 페이지 수와 문서 유형별 비율은 어떻게 되나요?
