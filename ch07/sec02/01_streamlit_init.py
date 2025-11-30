import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser 

from dotenv import load_dotenv
load_dotenv()

st.title("🛠️도구 호출 챗봇")
st.caption("⏰시계 + 📉주가 검색 도구 장착!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chain" not in st.session_state:
    st.session_state["chain"] = None

def clear_task():
    st.session_state["messages"] = []
    st.session_state["chain"] = None
    
with st.sidebar:  
    clear_btn = st.button("대화 초기화", on_click=clear_task)

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role, message):
    st.session_state["messages"].append(
        ChatMessage(role=role, content=message))

def create_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트입니다."),
            ("user", "#Question:\n{question}"),
        ]
    )
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    output_parsers = StrOutputParser()

    chain = prompt | model | output_parsers

    return chain

print_messages()

if st.session_state["chain"] is None:
    st.session_state["chain"] = create_chain()

if user_input := st.chat_input("시간 또는 주식에 대해 물어 보세요!"):
    if st.session_state["chain"] is not None:
        st.chat_message("user").write(user_input)
        add_message("user", user_input)

        # 타이핑하듯이 답변 출력
        response = st.session_state["chain"].stream(
            {"question": st.session_state.messages})
        
        with st.chat_message("assistant"):
            container = st.empty()  # 페이지 전체를 다시 로드하지 않고도 콘텐츠를 동적으로 업데이트하는 빈 컨테이너 생성

            ai_answer = ""

            for token in response:  # response는 generator
                ai_answer += token
                container.markdown(ai_answer)

        add_message("assistant", ai_answer)

print(st.session_state["messages"])