import os
import openai
import tkinter as tk
from tkinter import scrolledtext, ttk

from config import config
from chatbot import ChatBot


def handle_user_input(event=None):
    global user_input, chat_history

    user_content = user_input.get()
    if not user_content.strip():
        return  # Don't send empty messages

    user_input.delete(0, tk.END)  # Clear the input field

    chat_history.configure(state=tk.NORMAL)  # Enable editing
    chat_history.insert(tk.END, f"You: {user_content}\n", "user")
    chat_history.insert(tk.END, "\n", "space")  # Add a newline
    chat_history.configure(state=tk.DISABLED)  # Disable editing
    chat_history.see(tk.END)  # Scroll to the end of the chat history

    assistant_content = chatbot.get_answer(user_content)

    chat_history.configure(state=tk.NORMAL)  # Enable editing
    chat_history.insert(tk.END, f"GPT: {assistant_content}\n", "assistant")
    chat_history.insert(tk.END, "\n", "space")  # Add a newline
    chat_history.configure(state=tk.DISABLED)  # Disable editing
    chat_history.see(tk.END)


def on_entry_click(event):
    """Function to act as the Entry placeholder."""
    if user_input.get() == 'Type your message here...':
        user_input.delete(0, tk.END)
        user_input.config(foreground='black')


def on_focusout(event):
    if user_input.get() == '':
        user_input.insert(0, 'Type your message here...')
        user_input.config(foreground='grey')


def main():
    global user_input, chat_history, messages, chatbot

    chatbot = ChatBot()
    openai.api_key = config.api_key

    # Create the Tkinter window and widgets
    root = tk.Tk()
    root.title("GPT Chat")
    root.geometry("800x600")

    # Define styles
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 11), padding=5)
    style.configure('TEntry', font=('Arial', 12), foreground='grey')

    chat_frame = ttk.Frame(root)
    chat_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    user_input_frame = ttk.Frame(root)
    user_input_frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

    chat_history = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=80, height=20, state=tk.DISABLED)
    chat_history.pack(expand=True, fill=tk.BOTH)
    chat_history.tag_config("user", foreground="blue", font=("Arial", 12, "bold"), justify=tk.RIGHT)
    chat_history.tag_config("assistant", foreground="darkgreen", font=("Arial", 12), justify=tk.LEFT)
    chat_history.tag_config("welcome", foreground="purple", font=("Arial", 12, "italic"), justify=tk.CENTER)

    chat_history.configure(state=tk.NORMAL)
    chat_history.insert(tk.END, "Welcome to GPT Chat!\n\n", "welcome")
    chat_history.configure(state=tk.DISABLED)
    chat_history.see(tk.END)

    user_input = ttk.Entry(user_input_frame, width=80, style='TEntry')
    user_input.insert(0, 'Type your message here...')
    user_input.bind('<FocusIn>', on_entry_click)
    user_input.bind('<FocusOut>', on_focusout)
    user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    user_input.bind("<Return>", handle_user_input)

    send_button = ttk.Button(user_input_frame, text="Send", command=handle_user_input, style='TButton')
    send_button.pack(side=tk.RIGHT)

    root.mainloop()

    if config.save_messages:
        chatbot.save_messages_to_csv()


if __name__ == '__main__':
    main()
