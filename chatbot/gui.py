import tkinter as tk
from tkinter import scrolledtext
import threading
from main import GeminiChatBot

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Chatbot")
        self.root.geometry("500x600")

        self.chat_history = scrolledtext.ScrolledText(root, state='disabled', wrap='word')
        self.chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10, padx=10, fill=tk.X)

        self.user_input = tk.Entry(self.input_frame, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        try:
            self.bot = GeminiChatBot()
            self.append_message("Bot", "Chatbot initialized. How can I help you?")
        except ValueError as e:
            self.append_message("System", f"Error: {e}\nPlease check your .env file.")
            self.user_input.config(state='disabled')
            self.send_button.config(state='disabled')

    def send_message(self, event=None):
        message = self.user_input.get()
        if not message:
            return

        self.append_message("You", message)
        self.user_input.delete(0, tk.END)

        # Run chat in a separate thread to keep GUI responsive
        threading.Thread(target=self.get_bot_response, args=(message,)).start()

    def get_bot_response(self, message):
        response = self.bot.chat(message)
        self.root.after(0, self.append_message, "Bot", response)

    def append_message(self, sender, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_history.see(tk.END)
        self.chat_history.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
