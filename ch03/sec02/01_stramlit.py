import streamlit as st

st.write("🤖 나만의 챗봇 만들기")

st.caption("랭체인을 사용하지 않고 만드는 챗봇")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "대화를 시작해 볼까요? 👇"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": prompt})
    with st.chat_message("assistant"):
        st.markdown(prompt)
