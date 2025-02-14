"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

with open('instruction.txt', 'r') as f:
        system_instruction = f.read()

# Create the model
generation_config = {
  "temperature": 0.8,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 4096,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction=system_instruction,
  # Google Search as a tool is not available in this version of the SDK.
  # Please try the new genAI SDK (https://ai.google.dev/gemini-api/docs/sdks)
  # and see the docs here (https://ai.google.dev/gemini-api/docs/grounding?lang=python#search-tool)
)

history = []

print("Jeruyiq: Hello! How can I help you today?")

while True:

    user_input = input("You: ")

    chat_session = model.start_chat(
        history=history,
    )

    response = chat_session.send_message(user_input)

    model_response = response.text

    print(f'Jeruyiq: {model_response}')

    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})