import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage # * 수정
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # * 추가
from langchain_google_genai import ChatGoogleGenerativeAI  # * 추가
from langchain_core.output_parsers import StrOutputParser  # * 추가

import os  # * 추가
from dotenv import load_dotenv  # * 추가
load_dotenv()  # * 추가

gemini_api_key = os.getenv("GEMINI_API_KEY")

st.title("🤖 나만의 챗봇 만들기")
st.caption("랭체인을 사용하여 챗봇을 만들었습니다.")

with st.sidebar:
    clear_btn = st.button("초기화")

if "messages" not in st.session_state:
    st.session_state.messages = []

def print_messages():  # 모든 메시지 출력
    for lang_message in st.session_state["messages"]:
        # LangChain 메시지 객체(HumanMessage, AIMessage)의 'type' 속성은 
        # 각각 'human', 'ai'로 반환됩니다. Streamlit의 역할명으로 매핑합니다.
        if lang_message.type == "human":
            st_role = "user"
        elif lang_message.type == "ai":
            st_role = "assistant"
        else:
            # SystemMessage 등 다른 메시지 유형 처리 (이 예시에서는 'ai'로 간주)
            st_role = "assistant" 
            
        st.chat_message(st_role).markdown(lang_message.content)

def add_message(role, message):  # * 메시지 저장
    # 역할 문자열에 따라 적절한 LangChain 메시지 객체를 생성하여 저장합니다.
    if role == "user":
        msg_obj = HumanMessage(content=message)
    elif role == "assistant":
        msg_obj = AIMessage(content=message)
    else:
        # 예상치 못한 역할은 저장하지 않습니다.
        return
        
    st.session_state["messages"].append(msg_obj)

def create_chain():  # * 체인
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage("당신은 친절하고 도움이 되는 AI 어시스턴트입니다."),
            # * 수정: 대화 기록(st.session_state.messages) 전체를 여기에 삽입합니다.
            MessagesPlaceholder(variable_name="messages"), # 대화의 연속성 유지
        ]
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", google_api_key=gemini_api_key
    )
    output_parsers = StrOutputParser()

    chain = prompt | llm | output_parsers

    return chain

if clear_btn:  # 추가
    st.session_state["messages"] = []

print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요..."):
    st.chat_message("user").markdown(prompt)
    add_message("user", prompt)

    chain = create_chain()

    print("prompt>>>", prompt)

    response = chain.invoke(
        {
            "messages": st.session_state.messages
        }
    )

    st.chat_message("assistant").markdown(response)

    add_message("assistant", response)

print(st.session_state.messages)