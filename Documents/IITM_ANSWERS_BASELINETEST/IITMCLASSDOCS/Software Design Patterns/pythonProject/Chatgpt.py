import openai
import tkinter as tk

# Initialize the OpenAI API with your API key
api_key = "your_api_key_here"
openai.api_key = api_key


def chatbot_response(user_input):
    # Define the user's message and prompt for the chatbot
    user_message = f"User: {user_input}\n"
    chat_prompt = f"{user_message}ChatBot:"

    # Generate a response from GPT-3
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=chat_prompt,
        max_tokens=50  # Adjust the response length as needed
    )

    # Extract and return the chatbot's reply
    chatbot_reply = response.choices[0].text.strip().replace("ChatBot:", "")
    return chatbot_reply


def send_message():
    user_input = entry.get()
    entry.delete(0, tk.END)  # Clear the user input field

    chatbot_reply = chatbot_response(user_input)
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_input}\n", "user")
    chat_history.insert(tk.END, f"ChatBot: {chatbot_reply}\n", "bot")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)


# Create the main window
window = tk.Tk()
window.title("ChatBot")

# Create a scrolled text widget for chat history
chat_history = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
chat_history.pack(fill=tk.BOTH, expand=True)

# Create an entry field for user input
entry = tk.Entry(window, width=50)
entry.pack()

# Create a send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

# Define text styles
chat_history.tag_config("user", foreground="blue")
chat_history.tag_config("bot", foreground="green")

# Start the Tkinter main loop
window.mainloop()
