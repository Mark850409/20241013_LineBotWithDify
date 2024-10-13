import requests
import re
from urllib.parse import unquote

def translate_texts(texts):
    url = "https://c6f0-163-14-137-66.ngrok-free.app/v1/chat-messages"
    headers = {
        "Authorization": "Bearer app-n4eAhzkKVy7a8TMFyMzz0x09",
        "Content-Type": "application/json"
    }

    translated_texts = []

    for text in texts:
        data = {
            "inputs": {},
            "query": text,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "abc-123"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            # 提取 JSON 回應內容
            json_response = response.json()

            # 假設 'answer' 欄位中包含所需的內容
            answer_content = json_response.get('answer', '')

            # 使用正規表示式移除 <context> 和 </context> 標籤及其中的內容
            cleaned_content = re.sub(r'<context>.*?</context>', '', answer_content, flags=re.DOTALL).strip()

            # 使用正規表示式找到 URL，並解碼它
            url_pattern = r'https?://[^\s]+'
            urls = re.findall(url_pattern, cleaned_content)

            # 解碼 URLs
            for url in urls:
                decoded_url = unquote(url)
                cleaned_content = cleaned_content.replace(url, decoded_url)

            # 添加清理後的內容
            translated_texts.append(cleaned_content)

    return translated_texts


# 範例使用
texts_to_translate = [
    "請列出所有和米可白有關的新聞"
]

translations = translate_texts(texts_to_translate)

# 印出結果
for translation in translations:
    print(translation)
