import streamlit as st
from langchain.messages import HumanMessage, AIMessage

st.title("🤖 나만의 챗봇 만들기")

st.caption("랭체인을 사용하지 않고 만들어 보는 챗봇")

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

print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요..."):
    st.chat_message("user").markdown(prompt)
    st.chat_message("assistant").markdown(prompt)

    add_message("user", prompt)
    add_message("assistant", prompt)