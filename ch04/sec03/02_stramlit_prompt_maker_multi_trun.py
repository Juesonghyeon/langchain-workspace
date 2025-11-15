import streamlit as st
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import glob

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

st.title("🤖 나만의 랭체인 챗봇")
st.caption("랭체인을 사용하여 챗봇을 만들었습니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "task_input" not in st.session_state:
    st.session_state.task_input = ""

if "runnable" not in st.session_state:
    st.session_state.runnable = None
    st.session_state.last_prompt = None
    st.session_state.last_task = ""

with st.sidebar:
    clear_btn = st.button("초기화")

    prompt_files = glob.glob("prompts_multi_turn/*.yaml")
    prompt_labels = {
        'prompts_multi_turn\\general.yaml': "일반 프롬프트", 
        'prompts_multi_turn\\prompt-maker.yaml': "프롬프트 생성기", 
        'prompts_multi_turn\\summary.yaml': "요약 프롬프트"
    }

    selected_prompt = st.selectbox(
        "프롬프트를 선택해 주세요", 
        prompt_files, 
        index=0,
        format_func=lambda x: prompt_labels.get(x)
    )

    task_input = st.text_input(
        "TASK 입력",
        key="task_input",
        value=st.session_state["task_input"]
    )

# print("선택한 프롬프트:", selected_prompt)
# print("선택한 프롬프트의 내용:", load_prompt(selected_prompt))

def print_messages():
    for msg in st.session_state.messages:
        st.chat_message(msg.role).write(msg.content)

def add_message(role, message):
    st.session_state["messages"].append(
        ChatMessage(role=role, content=message))

def create_chain(prompt_filepath, task=""):
    prompt = load_prompt(prompt_filepath, encoding="utf-8")

    if task:
        prompt = prompt.partial(task=task)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", google_api_key=gemini_api_key
    )
    output_parsers = StrOutputParser()

    chain = prompt | llm | output_parsers

    return chain

if clear_btn:
    st.session_state["messages"] = []

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}

print("chat_histories:", st.session_state.chat_histories)

def get_session_history(session_id):
    if session_id not in st.session_state.chat_histories:
        st.session_state.chat_histories[session_id] = ChatMessageHistory()
    return st.session_state.chat_histories[session_id]

# 프롬프트나 TASK가 변경되었을 경우에만 runnable을 새로 생성
if (
    st.session_state.runnable is None
    or st.session_state.last_prompt != selected_prompt
    or st.session_state.last_task != task_input
):
    st.session_state.last_prompt = selected_prompt
    st.session_state.last_task = task_input
    chain = create_chain(selected_prompt, task=task_input)
    st.session_state.runnable = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요..."):
    st.chat_message("user").markdown(prompt)
    add_message("user", prompt)

    response = st.session_state.runnable.invoke(
        {
            "question": prompt
        },
        config={"configurable": {"session_id": "any"}}
    )

    st.chat_message("assistant").markdown(response)

    add_message("assistant", response)

print(st.session_state.messages)