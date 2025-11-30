import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

st.title("🤖 나만의 챗봇 만들기")
st.caption("랭체인을 사용하여 챗봇을 만들었습니다.")

with st.sidebar:
    clear_btn = st.button("초기화")

    selected_prompt = st.selectbox(
        "언어를 선택해 주세요", ("Korean", "English"), index=0
    )

print(selected_prompt)

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

def create_chain():
    if selected_prompt == "Korean":
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage("당신은 한국어로 대답하는 친절한 AI 어시스턴트입니다."), 
                MessagesPlaceholder(variable_name="messages"), 
            ]
        )

    if selected_prompt == "English":
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage("당신은 영어로 대답하는 친절한 AI 어시스턴트입니다. 답변은 반드시 영어로 해야합니다."),
                MessagesPlaceholder(variable_name="messages"), 
            ]
        )

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

    chain = create_chain()

    response = chain.invoke(
        {
            "messages": st.session_state.messages
        }
    )

    st.chat_message("assistant").markdown(response)

    add_message("assistant", response)

print(st.session_state.messages)
