# uv add streamlit

import streamlit as st

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

    st.session_state.messages.append({"role": "assistant", "content": prompt})
    with st.chat_message("assistant"):
        st.markdown(prompt)
