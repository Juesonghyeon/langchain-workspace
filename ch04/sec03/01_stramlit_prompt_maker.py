import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import glob

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if "task_input" not in st.session_state:
    st.session_state["task_input"] = ""

st.title("🤖 나만의 랭체인 챗봇")
st.caption("랭체인을 사용하여 챗봇을 만들었습니다.")

with st.sidebar:
    clear_btn = st.button("초기화")

    prompt_files = glob.glob("prompts/*.yaml")
    prompt_labels = {
        'prompts\\general.yaml': "일반 프롬프트", 
        'prompts\\prompt-maker.yaml': "프롬프트 생성기", 
        'prompts\\summary.yaml': "요약 프롬프트"
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

print("선택한 프롬프트:", selected_prompt)
print("선택한 프롬프트의 내용:", load_prompt(selected_prompt))

if "messages" not in st.session_state:
    st.session_state.messages = []

def print_messages():
    for lang_message in st.session_state["messages"]:
        if lang_message.type == "human":
            st_role = "user"
        elif lang_message.type == "ai":
            st_role = "assistant"
        else:
            st_role = "assistant" 
            
        st.chat_message(st_role).markdown(lang_message.content)

def add_message(role, message):
    if role == "user":
        msg_obj = HumanMessage(content=message)
    elif role == "assistant":
        msg_obj = AIMessage(content=message)
    else:
        return
        
    st.session_state["messages"].append(msg_obj)

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

print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요..."):
    st.chat_message("user").markdown(prompt)
    add_message("user", prompt)

    chain = create_chain(selected_prompt, task_input)

    response = chain.invoke(
        {
            "question": prompt
        }
    )

    st.chat_message("assistant").markdown(response)

    add_message("assistant", response)

print(st.session_state.messages)