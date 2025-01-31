from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import tkinter as tk
from tkinter import scrolledtext

# Define the chatbot components
templates = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="deepseek-r1:1.5b")
prompt = ChatPromptTemplate.from_template(templates)
chain = prompt | model

# Initialize conversation history
context = ""

# Function to handle conversation
def handle_conversation():
    global context
    user_input = user_entry.get().strip()

    if not user_input:  # Ignore empty input
        return

    # Display user's message
    chat_display.config(state="normal")
    chat_display.insert(tk.END, f"You: {user_input}\n", "user")
    chat_display.config(state="disabled")
    user_entry.delete(0, tk.END)

    # Get chatbot response
    result = chain.invoke({"context": context, "question": user_input})
    bot_response = str(result)

    # Display bot response
    chat_display.config(state="normal")
    chat_display.insert(tk.END, f"Bot: {bot_response}\n", "bot")
    chat_display.config(state="disabled")
    chat_display.see(tk.END)  # Auto-scroll

    # Update conversation context
    context += f"\nUser: {user_input}\nAI: {bot_response}"

# Create Tkinter UI
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("600x400")
root.resizable(False, False)

# Chat display area
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=60, state="disabled")
chat_display.pack(pady=10, padx=10, fill="both", expand=True)
chat_display.tag_configure("user", foreground="blue")  # User message color
chat_display.tag_configure("bot", foreground="green")  # Bot message color
chat_display.config(state="normal")
chat_display.insert(tk.END, "Welcome to the AI Chatbot! Type 'exit' to quit.\n")
chat_display.config(state="disabled")

# Frame for user input and send button
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

# Input entry field
user_entry = tk.Entry(bottom_frame, width=40, font=("Arial", 14))
user_entry.pack(side="left", fill="x", expand=True, padx=10)

# Send button
send_button = tk.Button(bottom_frame, text="Send", font=("Arial", 12, "bold"), command=handle_conversation)
send_button.pack(side="right", padx=10)

# Run the Tkinter event loop
root.mainloop()
