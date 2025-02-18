from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Ensure your API key is set as an environment variable

generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config
)

history = []  # Store conversation history

@app.route("/")
def index():
    return render_template("startpage.html")

@app.route("/chat", methods=["POST"])
def chat():
    global history
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_message)
        model_response = response.text.strip()

        history.append({"role": "user", "parts": [user_message]})
        history.append({"role": "model", "parts": [model_response]})

        return jsonify({"response": model_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)