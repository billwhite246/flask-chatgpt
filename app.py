import os
import openai
from flask import Flask, request, jsonify

# 从环境变量中获取API密钥
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# 初始化OpenAI库
openai.api_key = api_key

app = Flask(__name__)


@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    try:
        # 调用ChatGPT API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"User: {user_message}\nChatbot:",
            temperature=0.8,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\nUser:", "\nChatbot:"],
        )

        bot_response = response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        bot_response = "抱歉，我无法回答你的问题。"

    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
