from flask import Flask, render_template, request, jsonify
from rag_service import RAGChatbot
import os

app = Flask(__name__)
bot = RAGChatbot()

@app.route('/chat')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = bot.generate_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5009))
    app.run(host='0.0.0.0', port=port)
