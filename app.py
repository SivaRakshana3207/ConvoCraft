from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def get_groq_response(user_message, model='llama-3.1-8b-instant'):
    """
    Generate response from Groq Llama model.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[{'role': 'user', 'content': user_message}],
            model=model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "Error communicating with Groq API"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = get_groq_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
