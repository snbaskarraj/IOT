from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]

    # Replace with your chatbot logic to generate a response
    if user_input.lower() == "hello":
        response = "Hello! How can I help you today?"
    elif user_input.lower() == "bye":
        response = "Goodbye! Have a great day!"
    else:
        response = "I'm sorry, I don't understand that."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
