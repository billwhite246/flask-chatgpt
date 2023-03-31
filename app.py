from uuid import uuid4

import openai
import os
from flask import Flask, render_template, request, session

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-3.5-turbo"

app.secret_key = 'your_secret_key_here'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/img')
def hello_world_img():
    return render_template('img.html')


@app.route('/gpt35')
def hello_world_gpt35():
    return render_template('gpt35.html')


@app.route('/start_chat', methods=['POST'])
def start_chat():
    session_id = str(uuid4())
    session['messages'] = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        }
    ]
    return {"session_id": session_id}


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    session_id = request.form['session_id']

    messages = session.get('messages', [])
    gpt_response = send_message_to_gpt(user_message, messages)

    session['messages'] = messages

    return {"response": gpt_response}


def send_message_to_gpt(message, messages):
    user_message = {
        "role": "user",
        "content": message
    }
    messages.append(user_message)

    data = {
        'model': MODEL,
        'messages': messages
    }

    response = openai.ChatCompletion.create(**data)
    assistant_message = response.choices[0].message['content'].strip()

    messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message


if __name__ == '__main__':
    app.run(debug=True)

# =================================
# import os
# import sys
#
# import openai
# from flask import Flask, request, jsonify, render_template
#
# # 从环境变量中获取API密钥
# api_key = os.getenv('OPENAI_API_KEY')
#
# if not api_key:
#     raise ValueError("OPENAI_API_KEY environment variable is required")
#
# # 初始化OpenAI库
# openai.api_key = api_key
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return render_template('index.html')
#
#
# @app.route('/img')
# def hello_world_img():
#     return render_template('img.html')
#
#
# @app.route('/gpt35')
# def hello_world_gpt35():
#     return render_template('gpt35.html')
#
#
# @app.route('/test/chat', methods=['GET'])
# def chat_with_gpt():
#     prompt = "What is the capital of France?"
#     response = openai.Completion.create(
#         engine="davinci-codex",
#         prompt=prompt,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
#
#     message = response.choices[0].text.strip()
#     return message
#
#
# @app.route('/api/chat', methods=['POST'])
# def chat():
#     conversation = request.json.get('conversation', '')
#
#     try:
#         # 调用ChatGPT API
#         response = openai.ChatCompletion.create(
#             engine="gpt-3.5-turbo",
#             prompt=f"{conversation}\nChatbot:",
#             temperature=0.8,
#             max_tokens=150,
#             top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0,
#             stop=["\nUser:", "\nChatbot:"],
#         )
#
#         bot_response = response.choices[0].text.strip()
#     except Exception as e:
#         print(f"Error: {e}")
#         bot_response = "抱歉，我无法回答你的问题。"
#
#     return jsonify({'response': bot_response})
#
#
#
# @app.route('/api/generate_image', methods=['POST'])
# def generate_image():
#     text_description = request.json.get('description', '')
#
#     try:
#         # 调用 DALL-E API
#         response = openai.Image.create(
#             prompt=text_description,
#             n=1,
#             size="1024x1024"
#         )
#
#         image_url = response['data'][0]['url']
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"error": "抱歉，无法生成图片。"})
#
#     return jsonify({"image_url": image_url})
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
