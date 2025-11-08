import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

#gemini 모델 연동
@st.cache_resource
def get_gemini_client():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=gemini_api_key)
client = get_gemini_client()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(model="gemini-2.5-flash")

st.write("🤖 나만의 챗봇 만들기")

st.caption("랭체인을 사용하지 않고 만드는 챗봇")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "대화를 시작해 볼까요? 👇"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.chat_session.send_message(message=prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)
