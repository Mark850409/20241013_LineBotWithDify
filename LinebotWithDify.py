from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,FollowEvent, UnfollowEvent
import requests
import re
import json
from urllib.parse import unquote
from setting import ACCESS_TOKEN, SECRET,API_ENDPOINT,DIFY_API_KEY
app = Flask(__name__)

# LINE Bot 資訊
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

# Dify API URL
DIFY_API_URL = f'{API_ENDPOINT}/v1/chat-messages'
DIFY_API_KEY = DIFY_API_KEY


# Webhook 路徑，設定為 LINE Webhook URL
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 處理 LINE 傳送過來的訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 傳送訊息到 Dify
    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "abc-123"
    }

    try:
        dify_response = requests.post(DIFY_API_URL, headers=headers, json=payload)

        if dify_response.status_code == 200:
            # 提取 JSON 回應內容
            dify_reply = dify_response.json()

            # 假設 'answer' 欄位中包含所需的內容
            answer_content = dify_reply.get('answer', '')

            # 使用正規表示式移除 <context> 和 </context> 標籤及其中的內容
            cleaned_content = re.sub(r'<context>.*?</context>', '', answer_content, flags=re.DOTALL).strip()

            # 使用正規表示式找到 URL，並解碼它
            url_pattern = r'https?://[^\s]+'
            urls = re.findall(url_pattern, cleaned_content)

            # 解碼 URLs
            for url in urls:
                decoded_url = unquote(url)
                cleaned_content = cleaned_content.replace(url, decoded_url)

            # 回傳 Dify 的回覆到 LINE
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=cleaned_content)
            )
        else:
            print(f'API Error: {dify_response.status_code}, Response: {dify_response.text}')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f'Dify 回應失敗，狀態碼: {dify_response.status_code}')
            )
    except Exception as e:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'發生錯誤: {str(e)}')
        )

# LINE WEBHOOK串接進入點
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)  # 取得收到的訊息內容
    signature = request.headers['X-Line-Signature']  # 加入回傳的 headers
    try:
        handler.handle(body, signature)  # 綁定訊息回傳的相關資訊
        json_data = json.loads(body)  # json 格式化訊息內容
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print(f"Error: {e}")  # 印出錯誤訊息
        print(body)  # 印出收到的內容

    return 'OK'  # 驗證 Webhook 使用，不能省略

# 處理加入好友事件
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name

    # 新用戶會看到的訊息
    welcome_message = f"您好：{user_name}\n感謝您加入好友😘\n歡迎使用娛樂新聞助手😎！\n你可以請AI做的事情有:\n1.廢話不多說，直接查驗AI身分\n2.命令AI叫他幫你查新聞，讓AI累死\n使用教學如下：\n1.範例1：你是誰???\n2.️ ️範例2：請告訴我最新的10則新聞"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_message)
    )


# 處理封鎖和重新加入好友事件
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name

    # 新用戶會看到的訊息
    welcome_message = f"歡迎您重新加入, {user_name}！\n你可以請AI做的事情有:\n1.廢話不多說，直接查驗AI身分\n2.命令AI叫他幫你查新聞，讓AI累死\n使用教學如下：\n1.範例1：你是誰???\n2.️ ️範例2：請告訴我最新的10則新聞"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_message)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
