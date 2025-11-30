import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

class GeminiChatBot:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.with_message_history = RunnableWithMessageHistory(
            self.llm,
            get_session_history,
        )
        self.config = {"configurable": {"session_id": "abc2"}}

    def chat(self, user_input: str) -> str:
        try:
            response = self.with_message_history.invoke(
                user_input,
                config=self.config,
            )
            return response.content
        except Exception as e:
            return f"An error occurred: {e}"

def main():
    try:
        bot = GeminiChatBot()
    except ValueError as e:
        print(e)
        print("Please create a .env file with your GOOGLE_API_KEY.")
        return

    print("Chatbot initialized. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        response = bot.chat(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
