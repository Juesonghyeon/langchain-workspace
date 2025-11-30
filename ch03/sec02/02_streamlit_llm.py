import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

# ====================================================================
# gemini 모델 연동
# genai.Client 객체를 st.cache_resource로 캐싱하여 안정적으로 관리합니다. (핵심 수정)
@st.cache_resource
def get_gemini_client():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=gemini_api_key)

client = get_gemini_client()
# ====================================================================

# 대화 내용 유지 목적
# 스트림릿을 프롬프트를 작성해서 보내면 코드가 처음 부터 다시 실행됨
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = client.chats.create(model="gemini-2.5-flash")

st.title("🤖 나만의 챗봇 만들기")

st.caption("랭체인을 사용하지 않고 만들어 보는 챗봇")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "대화를 시작해 볼까요? 👇"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("궁금한 내용을 물어보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    print("질문 전달>>>", st.session_state)
    response = st.session_state.chat_session.send_message(message=prompt)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)
