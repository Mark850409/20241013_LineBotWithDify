# 【自動化爬蟲】人工智慧工作坊-娛樂新聞助手-實作流程

## 1. 簡介

如何將爬蟲的資料建立成知識庫並串接`LLM模型`最後部署到`LINEBOT`

## 2. 目錄

- [【自動化爬蟲】人工智慧工作坊-娛樂新聞助手-實作流程](#自動化爬蟲人工智慧工作坊-娛樂新聞助手-實作流程)
  - [1. 簡介](#1-簡介)
  - [2. 目錄](#2-目錄)
  - [3. 操作步驟](#3-操作步驟)
    - [3.1. 使用docker安裝dify](#31-使用docker安裝dify)
    - [3.2. dify基礎配置與設定](#32-dify基礎配置與設定)
      - [3.2.1. 設定`dify`管理員帳號](#321-設定dify管理員帳號)
      - [3.2.2. 設定`dify`語言與時區](#322-設定dify語言與時區)
      - [3.2.3. 設定`模型供應商`](#323-設定模型供應商)
    - [3.3. 建立`dify`新聞小助手應用](#33-建立dify新聞小助手應用)
      - [3.3.1. 建立空白應用\&相關設定](#331-建立空白應用相關設定)
    - [3.4. python爬蟲程式撰寫\&dify知識庫API串接](#34-python爬蟲程式撰寫dify知識庫api串接)
      - [3.4.1. yahoo奇摩娛樂新聞爬蟲程式碼](#341-yahoo奇摩娛樂新聞爬蟲程式碼)
      - [3.4.2. dify知識庫API串接範例](#342-dify知識庫api串接範例)
    - [3.5. `LINEBOT`與`dify知識庫`進行串接](#35-linebot與dify知識庫進行串接)
      - [3.5.1. `LINEBOT`與\`dify參數設定](#351-linebot與dify參數設定)
      - [3.5.2. LINEBOT WEBHOOK CALLBACK程式](#352-linebot-webhook-callback程式)
      - [3.5.3. LINEBOT 相關事件邏輯處理](#353-linebot-相關事件邏輯處理)
      - [3.5.4. LINEBOT 主程式邏輯處理(負責接收使用傳遞過來的訊息與回應)](#354-linebot-主程式邏輯處理負責接收使用傳遞過來的訊息與回應)
      - [3.5.5. 使用`python flask`啟動`server`](#355-使用python-flask啟動server)
    - [部署`LINEBOT`到`docker`](#部署linebot到docker)
      - [撰寫dockerfile](#撰寫dockerfile)
      - [撰寫docker-compose.yml](#撰寫docker-composeyml)
      - [部署到docker](#部署到docker)


## 3. 操作步驟

### 3.1. 使用docker安裝dify

git clone指令，將 Dify 複製到你的裝置中

```bash
git clone https://github.com/langgenius/dify.git
```

進到 `dify/docker` 中，這邊放了所有和 docker 有關的設定

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131919941.png)


建立環境檔案 (`.env`) 這邊直接複製他的範例即可，並修改紅框處的參數

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131922329.png)

這邊 Dify 有 nginx 的 container，會將服務開在我們電腦的 80 port 和 443 port (如果有啟動 https)，如果你不想開在這些 port 或者電腦這些 port 已經被使用了可以自行修改 `.env`

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131923361.png)

啟動 docker compose

```bash
docker compose up -d # 這邊的 -d 是背景執行的意思
```


可以在windows安裝`docker desktop`，檢查這些容器是否有`正常運行`

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131926785.png)


### 3.2. dify基礎配置與設定
#### 3.2.1. 設定`dify`管理員帳號

安裝完成後，請先進入dify主畫面
```
http://localhost:[ports]/install
```

#### 3.2.2. 設定`dify`語言與時區

到右上角點擊頭像->設定 -> 語言

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131933305.png)


#### 3.2.3. 設定`模型供應商`

到右上角點擊頭像->設定 -> 模型供應商

這邊會看到 Dify 有支援的所有 LLM API (超級多...)，包含會用到的 OpenAI,gemini, 和本地的 Ollama 等等，按下設定然後輸入 `API Key` 即可使用，完成後如下圖

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131938562.png)


### 3.3. 建立`dify`新聞小助手應用

#### 3.3.1. 建立空白應用&相關設定

到最上方點擊工作室->建立空白應用 -> 選擇聊天助手->基礎編排->`名稱`可以`任意取`->點擊建立

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131940094.png)


 提示詞配置(可以chatgpt協助生成)

```
若有人詢問你是誰或是親切的問候時，請回覆：

「您好！我是您的人工智慧新聞助手，很高興能為您提供幫助。」

請根據使用者輸入的【關鍵字】在知識庫中搜尋相關新聞，並按照以下格式整理輸出：

回覆格式：

根據我的搜尋結果，我找到了以下的新聞：

新聞標題：

【標題1】

新聞摘要：

【摘要1】

新聞日期：

【日期1】

新聞來源：

【來源1】

完整內容連結：

連結1

（依此格式繼續列出最多 5 則新聞）

📌 注意事項：

列出最多 5 則新聞，並按照日期由近至遠的順序排序。

若新聞標題或摘要內容過於相似，僅顯示其中一則，並用其他不重複的新聞替換。
```


選擇引用知識庫

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131952045.png)


這裡可以自己測試並選擇適當的模型

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131954599.png)


每次配置完之後，都要選擇`發佈->更新`才會生效喔

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131955698.png)


### 3.4. python爬蟲程式撰寫&dify知識庫API串接

#### 3.4.1. yahoo奇摩娛樂新聞爬蟲程式碼

這邊以yahoo奇摩娛樂新聞為主，可自行調整撰寫，主要爬蟲片段如下

```python
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager  
import time  
import csv  
import dateparser  
import requests  
import json  
from setting import ENV_URL, CSV_FILENAME, API_ENDPOINT, DATASET_ID, DOCUMENT_ID, DOCUMENT_API_KEY, DIFY_API_KEY,TXT_FILENAME,JSON_FILENAME  
import os  
  
# 設定 Chrome 瀏覽器選項  
chrome_options = Options()  
chrome_options.add_argument("--headless")  # 無頭模式  
chrome_options.add_argument("--no-sandbox")  # 避免沙盒問題  
chrome_options.add_argument("--disable-dev-shm-usage")  # 解決資源限制問題  
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速  
chrome_options.add_argument("--window-size=1920x1080")  # 設定窗口大小  
  
  
# 初始化 driver 變數  
driver = None  
  
# 設定摘要最大長度  
MAX_SUMMARY_LENGTH = 100  # 你可以根據需要修改這個長度  
  
try:  
    # 使用 WebDriverManager 自動獲取 ChromeDriver    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  
    # Yahoo 台灣娛樂新聞的 URL    url = ENV_URL  
  
    # 打開網頁  
    driver.get(url)  
  
    # 滾動頁面至少五次  
    scroll_times = 5  
    for _ in range(scroll_times):  
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  
        time.sleep(1)  # 等待頁面載入  
  
    # 顯性等待，確保內容載入  
    wait = WebDriverWait(driver, 2)  
  
    # 找到所有目標區塊 (根據 class 名稱)  
    items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'StreamMegaItem')))  
  
    # 檢查是否有現存的 CSV 檔案，讀取其內容並儲存現有的標題  
    existing_rows = set()  
    if os.path.exists(CSV_FILENAME):  
        with open(CSV_FILENAME, 'r', encoding='utf-8-sig') as csvfile:  
            reader = csv.DictReader(csvfile)  
            for row in reader:  
                key = (row['Title'], row['Source_Summary'], row['Time'])  
                existing_rows.add(key)  
  
    # 儲存要匯出成 JSON 和 TXT 的資料列表  
    json_data = []  
    txt_content = ""  
  
    # 開啟 CSV 檔案以供寫入 (覆蓋或新增)  
    with open(CSV_FILENAME, 'w', newline='', encoding='utf-8-sig') as csvfile:  
        # 定義欄位名稱  
        fieldnames = ['Title', 'Summary', 'Article_URL', 'Source_Summary', 'Time']  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  
  
        # 寫入標題列  
        writer.writeheader()  
  
        # 遍歷每個區塊，提取所需資訊  
        for item in items:  
            try:  
                title = item.find_element(By.CSS_SELECTOR, 'h3').text.strip()  
            except:  
                title = 'N/A'  
  
            try:  
                summary = item.find_element(By.CSS_SELECTOR, 'p').text.strip()  
                if len(summary) > MAX_SUMMARY_LENGTH:  
                    summary = summary[:MAX_SUMMARY_LENGTH] + '...'  
                summary = summary.replace('\n', '\n\n')  
            except:  
                summary = 'N/A'  
  
            try:  
                article_url = item.find_element(By.CLASS_NAME, 'mega-item-header-link').get_attribute('href')  
            except:  
                article_url = 'N/A'  
  
            try:  
                time_info = item.find_element(By.XPATH, ".//div[contains(@class, 'C(#959595)')]").text.strip()  
                source, time_posted_relative = time_info.split(' • ')  
                time_posted = dateparser.parse(time_posted_relative)  
                time_posted = time_posted.strftime('%Y-%m-%d %H:%M:%S') if time_posted else 'N/A'  
            except:  
                source, time_posted = 'N/A', 'N/A'  
  
            # 檢查是否重複（Title, Source_Summary, Time）  
            data_key = (title, source, time_posted)  
            if data_key in existing_rows:  
                print(f"重複資料，跳過: {data_key}")  
                continue  # 跳過重複資料  
  
            row_data = {  
                'Title': title,  
                'Summary': summary,  
                'Article_URL': article_url,  
                'Source_Summary': source,  
                'Time': time_posted  
            }  
  
            writer.writerow(row_data)  
            json_data.append(row_data)  
            txt_content += f"標題: {title}\n內文摘要: {summary}\n文章網址: {article_url}\n來源摘要: {source}\n時間: {time_posted}\n{'-' * 30}\n"  
  
            # 輸出取得的資訊  
            print(f'標題: {title}')  
            print(f'內文摘要: {summary}')  
            print(f'文章網址: {article_url}')  
            print(f'來源摘要: {source}')  
            print(f'時間: {time_posted}')  
            print('-' * 30)  
  
    # 將資料匯出為 JSON 檔案  
    with open(JSON_FILENAME, 'w', encoding='utf-8') as jsonfile:  
        json.dump(json_data, jsonfile, ensure_ascii=False, indent=4)  
  
    # 將資料匯出為 TXT 檔案  
    with open(TXT_FILENAME, 'w', encoding='utf-8') as txtfile:  
        txtfile.write(txt_content)  
  
except Exception as e:  
    print("An error occurred:", e)  
  
finally:  
    if driver:  
        driver.quit()
```

#### 3.4.2. dify知識庫API串接範例


檢查資料集是否存在
```python

def check_dataset_exists(dataset_id, api_key):  
    api_endpoint = API_ENDPOINT + "/v1/datasets?page=1&limit=20"  
  
    headers = {  
        'Authorization': f'Bearer {api_key}'  
    }  
  
    response = requests.get(api_endpoint, headers=headers)  
  
    if response.status_code == 200:  
        datasets = response.json().get('data', [])  
        # 檢查指定的 dataset_id 是否存在於資料集中  
        for dataset in datasets:  
            if dataset['id'] == dataset_id:  
                return True  
        return False    else:  
        print(f'無法獲取資料集列表，狀態碼: {response.status_code}, 回應: {response.text}')  
        return False

```

檢查資料集當中文件是否存在

```python

def check_document_exists(dataset_id, document_id, api_key):  
    # 定義列出資料集中所有文件的 API 端點  
    api_endpoint = f"{API_ENDPOINT}/v1/datasets/{dataset_id}/documents"  
    headers = {  
        'Authorization': f'Bearer {api_key}'  
    }  
  
    response = requests.get(api_endpoint, headers=headers)  
  
    if response.status_code == 200:  
        documents = response.json().get('data', [])  
        # 檢查文件 ID 是否在文件列表中  
        for document in documents:  
            if document.get('id') == document_id:  
                return True  # 找到對應的文件 ID，回傳 True        return False  # 沒有找到對應的文件 ID，回傳 False    else:  
        print(f'檢查文件失敗，狀態碼: {response.status_code}, 回應: {response.text}')  
        return False
```

更新已存在的知識庫
```python

def update_existing_document(file_path, dataset_id, document_id, api_key):  
    # 定義更新文件的 API 端點  
    api_endpoint = f"{API_ENDPOINT}/v1/datasets/{dataset_id}/documents/{document_id}/update_by_file"  
  
    # 定義請求標頭  
    headers = {  
        'Authorization': f'Bearer {api_key}'  
    }  
  
    # 定義表單資料（將資料轉為 JSON）  
    data = {  
        'data': json.dumps({  
            "name": "Dify",  
            "indexing_technique": "high_quality",  
            "process_rule": {  
                "rules": {  
                    "pre_processing_rules": [  
                        {"id": "remove_extra_spaces", "enabled": True},  
                        {"id": "remove_urls_emails", "enabled": False}  
                    ],                    "segmentation": {  
                        "separator": "------------------------------",  
                        "max_tokens": 1000  
                    }  
                },                "mode": "custom"  
            }  
        })    }  
    # 設定檔案  
    files = {  
        'file': open(file_path, 'rb')  
    }  
    # 發送 POST 請求更新文件  
    response = requests.post(api_endpoint, headers=headers, data=data, files=files)  
  
    # 檢查回應  
    if response.status_code == 200:  
        print('文件成功更新至 Dify')  
    else:  
        print(f'更新失敗，狀態碼: {response.status_code}, 回應: {response.text}')

```

上傳知識庫
```python
def upload_to_dify(file_path, dataset_id, document_id, api_key):  
    # 檢查資料集是否存在  
    if not check_dataset_exists(dataset_id, api_key):  
        print(f'資料集 {dataset_id} 不存在')  
        return  
  
    # 檢查文件是否已存在  
    if check_document_exists(dataset_id, document_id, api_key):  
        print(f'文件 {document_id} 已存在於資料集 {dataset_id}，將更新該文件。')  
        # 更新現有文件  
        update_existing_document(file_path, dataset_id, document_id, api_key)  
    else:  
        print('文件不存在，進行上傳。')  
        # 文件不存在，進行上傳  
        api_endpoint = f"{API_ENDPOINT}/v1/datasets/{dataset_id}/document/create_by_file"  
  
        # 定義請求標頭  
        headers = {  
            'Authorization': f'Bearer {api_key}'  
        }  
  
        # 定義表單資料  
        data = {  
            'data': json.dumps({  
                "indexing_technique": "high_quality",  
                "process_rule": {  
                    "rules": {  
                        "pre_processing_rules": [  
                            {"id": "remove_extra_spaces", "enabled": True},  
                            {"id": "remove_urls_emails", "enabled": False}  
                        ],                        "segmentation": {  
                            "separator": "------------------------------",  
                            "max_tokens": 1000  
                        }  
                    },                    "mode": "custom"  
                }  
            })        }  
        # 設定檔案  
        files = {  
            'file': open(file_path, 'rb')  
        }        # 發送 POST 請求  
        response = requests.post(api_endpoint, headers=headers, data=data, files=files)  
  
        # 檢查回應  
        if response.status_code == 200:  
            print('文件成功上傳至 Dify')  
        else:  
            print(f'上傳失敗，狀態碼: {response.status_code}, 回應: {response.text}')
```

程式使用範例，以下參數皆來自`setting.py`參數設定檔傳入
```python
# 使用範例  
txt_filename = TXT_FILENAME  
dataset_id = DATASET_ID  # 請替換為您的 dataset_id
document_id = DOCUMENT_ID  # 替換為您的 document_id
api_key = DOCUMENT_API_KEY  # 請替換為您的 API 金鑰   
upload_to_dify(txt_filename, dataset_id, document_id, api_key)
```


### 3.5. `LINEBOT`與`dify知識庫`進行串接


#### 3.5.1. `LINEBOT`與`dify參數設定

```python
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
```


#### 3.5.2. LINEBOT WEBHOOK CALLBACK程式

```python
# Webhook 路徑，設定為 LINE Webhook URL@app.route("/callback", methods=['POST'])  
def callback():  
    signature = request.headers['X-Line-Signature']  
    body = request.get_data(as_text=True)  
  
    try:  
        handler.handle(body, signature)  
    except InvalidSignatureError:  
        abort(400)  
  
    return 'OK'
```

LINE WEBHOOK串接進入點 

```python
# LINE WEBHOOK串接進入點  
@app.route("/", methods=['POST'])  
def linebot():  
    body = request.get_data(as_text=True)  # 取得收到的訊息內容  
    signature = request.headers['X-Line-Signature']  # 加入回傳的 headers    try:  
        handler.handle(body, signature)  # 綁定訊息回傳的相關資訊  
        json_data = json.loads(body)  # json 格式化訊息內容  
    except InvalidSignatureError:  
        abort(400)  
    except Exception as e:  
        print(f"Error: {e}")  # 印出錯誤訊息  
        print(body)  # 印出收到的內容  
  
    return 'OK'  # 驗證 Webhook 使用，不能省略
```

#### 3.5.3. LINEBOT 相關事件邏輯處理
```python
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
```


#### 3.5.4. LINEBOT 主程式邏輯處理(負責接收使用傳遞過來的訊息與回應)

```python

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
            )        else:  
            print(f'API Error: {dify_response.status_code}, Response: {dify_response.text}')  
            line_bot_api.reply_message(  
                event.reply_token,  
                TextSendMessage(text=f'Dify 回應失敗，狀態碼: {dify_response.status_code}')  
            )    except Exception as e:  
        line_bot_api.reply_message(  
            event.reply_token,  
            TextSendMessage(text=f'發生錯誤: {str(e)}')  
        )
```

#### 3.5.5. 使用`python flask`啟動`server`

```python
if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5000)
```


### 部署`LINEBOT`到`docker`

#### 撰寫dockerfile

```docker
# 使用 Python部署Flask後端框架  
FROM python:3.8  
# 設定工作目錄  
WORKDIR /usr/src/app  
# 複製所需檔案到容器內  
COPY . .  
RUN pip install --no-cache-dir -r requirements.txt  
# 暴露端口  
EXPOSE 5000  
# 啟動Flask  
CMD ["python", "LinebotWithDify.py"]
```

#### 撰寫docker-compose.yml

```docker
version: '3.8'  
  
services:  
  python:  
    build:  
      context: .  # Dockerfile 的位置  
      dockerfile: Dockerfile  # 自定義 Dockerfile 的名稱  
    container_name: LinebotWithDify  
    ports:  
      - "5000:5000"  
    volumes:  
      - C:\WorkSpace\yahooNewFetch_LINEBOT:/usr/src/app  
    networks:  
      - python_network  
  
networks:  
  python_network:

```

#### 部署到docker

將相關python檔案及上面寫好的腳本放置同一個目錄，執行以下命令

```docker
docker-compose up -d
```

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410132025602.png)

進入docker-desktop 查看，確認容器正常執行

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410132026478.png)


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410132027084.png)


