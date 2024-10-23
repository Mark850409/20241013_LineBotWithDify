# 1. 【自動化爬蟲】人工智慧工作坊-娛樂新聞助手-實作流程

## 1.1. 簡介

如何將爬蟲的資料建立成知識庫並串接`LLM模型`最後部署到`LINEBOT`

## 1.2. 目錄

- [1. 【自動化爬蟲】人工智慧工作坊-娛樂新聞助手-實作流程](#1-自動化爬蟲人工智慧工作坊-娛樂新聞助手-實作流程)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. 使用docker安裝dify](#131-使用docker安裝dify)
    - [1.3.2. dify基礎配置與設定](#132-dify基礎配置與設定)
      - [1.3.2.1. 設定`dify`管理員帳號](#1321-設定dify管理員帳號)
      - [1.3.2.2. 設定`dify`語言與時區](#1322-設定dify語言與時區)
      - [1.3.2.3. 設定`模型供應商`](#1323-設定模型供應商)
    - [1.3.3. 建立`dify`新聞小助手應用](#133-建立dify新聞小助手應用)
      - [1.3.3.1. 建立空白應用\&相關設定](#1331-建立空白應用相關設定)
    - [1.3.4. python爬蟲程式撰寫\&dify知識庫API串接](#134-python爬蟲程式撰寫dify知識庫api串接)
      - [1.3.4.1. yahoo奇摩娛樂新聞爬蟲程式碼](#1341-yahoo奇摩娛樂新聞爬蟲程式碼)
      - [1.3.4.2. dify知識庫API串接範例](#1342-dify知識庫api串接範例)
    - [1.3.5. `LINEBOT`與`dify知識庫`進行串接](#135-linebot與dify知識庫進行串接)
      - [1.3.5.1. `LINEBOT`與\`dify參數設定](#1351-linebot與dify參數設定)
      - [1.3.5.2. LINEBOT WEBHOOK CALLBACK程式](#1352-linebot-webhook-callback程式)
      - [1.3.5.3. LINEBOT 相關事件邏輯處理](#1353-linebot-相關事件邏輯處理)
      - [1.3.5.4. LINEBOT 主程式邏輯處理(負責接收使用傳遞過來的訊息與回應)](#1354-linebot-主程式邏輯處理負責接收使用傳遞過來的訊息與回應)
      - [1.3.5.5. 使用`python flask`啟動`server`](#1355-使用python-flask啟動server)
    - [1.3.6. 部署`LINEBOT`到`docker`](#136-部署linebot到docker)
      - [1.3.6.1. 撰寫dockerfile](#1361-撰寫dockerfile)
      - [1.3.6.2. 撰寫docker-compose.yml](#1362-撰寫docker-composeyml)
      - [1.3.6.3. 部署到docker](#1363-部署到docker)
    - [1.3.7. 部署 Stable Diffusion WebUI到`docker`](#137-部署-stable-diffusion-webui到docker)
    - [1.3.8. Stable Diffusion WebUI基礎設定](#138-stable-diffusion-webui基礎設定)
    - [1.3.9. Stable Diffusion 自定義API串接](#139-stable-diffusion-自定義api串接)
      - [1.3.9.1. 撰寫dockerfile](#1391-撰寫dockerfile)
      - [1.3.9.2. 撰寫docker-compose.yml](#1392-撰寫docker-composeyml)
      - [1.3.9.3. 撰寫app.py](#1393-撰寫apppy)
    - [1.3.10. dify工作流建立](#1310-dify工作流建立)
      - [1.3.10.1. 問題分類](#13101-問題分類)
      - [1.3.10.2. 知識庫建立](#13102-知識庫建立)
      - [1.3.10.3. 判斷提問相關性-LLM](#13103-判斷提問相關性-llm)
      - [1.3.10.4. JSON Parse](#13104-json-parse)
      - [1.3.10.5. 條件判斷](#13105-條件判斷)
      - [1.3.10.6. GoogleSearch](#13106-googlesearch)
      - [1.3.10.7. Json格式轉字串程式碼](#13107-json格式轉字串程式碼)
      - [1.3.10.8. 根據google回覆-LLM](#13108-根據google回覆-llm)
      - [1.3.10.9. GOOGLESEARCH問題回覆](#13109-googlesearch問題回覆)
      - [1.3.10.10. 根據知識庫回覆-LLM](#131010-根據知識庫回覆-llm)
      - [1.3.10.11. 知識庫問題回覆](#131011-知識庫問題回覆)
      - [1.3.10.12. 建立自定義小工具](#131012-建立自定義小工具)
      - [1.3.10.13. 自定義小工具流程設定](#131013-自定義小工具流程設定)
      - [1.3.10.14. 判斷條件設定](#131014-判斷條件設定)
      - [1.3.10.15. 圖檔語法轉換](#131015-圖檔語法轉換)
      - [1.3.10.16. dify圖檔呈現結果](#131016-dify圖檔呈現結果)
      - [1.3.10.17. LINEBOT圖檔呈現結果](#131017-linebot圖檔呈現結果)
    - [1.3.11. LINEBOT圖檔回傳邏輯撰寫](#1311-linebot圖檔回傳邏輯撰寫)
    - [1.3.12. 測試結果](#1312-測試結果)

## 1.3. 操作步驟

### 1.3.1. 使用docker安裝dify

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


<!--more-->

### 1.3.2. dify基礎配置與設定
#### 1.3.2.1. 設定`dify`管理員帳號

安裝完成後，請先進入dify主畫面
```
http://localhost:[ports]/install
```

#### 1.3.2.2. 設定`dify`語言與時區

到右上角點擊頭像->設定 -> 語言

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131933305.png)


#### 1.3.2.3. 設定`模型供應商`

到右上角點擊頭像->設定 -> 模型供應商

這邊會看到 Dify 有支援的所有 LLM API (超級多...)，包含會用到的 OpenAI,gemini, 和本地的 Ollama 等等，按下設定然後輸入 `API Key` 即可使用，完成後如下圖

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410131938562.png)


### 1.3.3. 建立`dify`新聞小助手應用

#### 1.3.3.1. 建立空白應用&相關設定

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


### 1.3.4. python爬蟲程式撰寫&dify知識庫API串接

#### 1.3.4.1. yahoo奇摩娛樂新聞爬蟲程式碼

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

#### 1.3.4.2. dify知識庫API串接範例


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


### 1.3.5. `LINEBOT`與`dify知識庫`進行串接


#### 1.3.5.1. `LINEBOT`與`dify參數設定

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


#### 1.3.5.2. LINEBOT WEBHOOK CALLBACK程式

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

#### 1.3.5.3. LINEBOT 相關事件邏輯處理
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


#### 1.3.5.4. LINEBOT 主程式邏輯處理(負責接收使用傳遞過來的訊息與回應)

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

#### 1.3.5.5. 使用`python flask`啟動`server`

```python
if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5000)
```


### 1.3.6. 部署`LINEBOT`到`docker`

#### 1.3.6.1. 撰寫dockerfile

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

#### 1.3.6.2. 撰寫docker-compose.yml

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

#### 1.3.6.3. 部署到docker

將相關python檔案及上面寫好的腳本放置同一個目錄，執行以下命令

```docker
docker-compose up -d
```

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410132025602.png)

進入docker-desktop 查看，確認容器正常執行

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410132026478.png)


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410132027084.png)


### 1.3.7. 部署 Stable Diffusion WebUI到`docker`

確認Docker認得到你的Nvidia顯示卡驅動版本

```docker
docker run --rm --runtime=nvidia --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi
```

複製AbdBarho的儲存庫

```bash
git clone https://github.com/AbdBarho/stable-diffusion-webui-docker.git

cd stable-diffusion-webui-docker
```


下載必要Stable Diffusion模型

```docker
docker compose --profile download up --build
```


啟動容器

```docker
docker compose --profile auto up
```


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162106841.png)


等待容器啟動完成，用瀏覽器開啟`http://localhost:7860`進入WebUI

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162106459.png)

### 1.3.8. Stable Diffusion WebUI基礎設定

點擊Extensions->Install from URL -> URL for extension's git repository ->將下方網頁說明的內容覺得有需要就`安裝`，算是`外掛增強`的一部分

https://www.chias.com.tw/%e3%80%90stable-diffusion%e3%80%91%e5%bf%85%e8%a3%9d%e6%93%b4%e5%85%85/

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162109566.png)


### 1.3.9. Stable Diffusion 自定義API串接

1. 因為dify現有的功能`非常簡陋`，這邊建議手動開發
2. 此步驟有用到`Firebase Storage`，用來將模型生成的圖片上傳至公開平台，取得網址後回傳，因此`stable-diffusion-customapi-firebase-adminsdk-bzguv-d0beefeec8.json`是Firebase的設定檔
#### 1.3.9.1. 撰寫dockerfile

```docker
# 使用官方 Python 映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製當前目錄的內容到容器中
COPY . /app

# 安裝必要的 Python 套件
RUN pip install flask requests flask_cors flask-openapi3 firebase-admin

# 對外暴露 5000 port
EXPOSE 5000

# 執行 Flask 應用程式
CMD ["python", "app.py"]
```

#### 1.3.9.2. 撰寫docker-compose.yml

```docker
version: '3.8'

services:
  stable-diffusion-flask-api:
    build: .
    ports:
      - "5001:5000"
    volumes:
      - C:\WorkSpace\stable-diffusion-customAPI:/app  # 掛載 volume
```

#### 1.3.9.3. 撰寫app.py

```python
from flask import Flask, request, jsonify
from flask_openapi3 import OpenAPI, Info, Tag, Server
from flask_openapi3.models import Response
from pydantic import BaseModel, Field
from flask_cors import CORS
import requests
import base64
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, storage

info = Info(title='Stable Diffusion API', version='1.0', description='使用 Stable Diffusion WebUI 生成圖像的 API')
servers = [
    Server(url="http://163.14.137.66:5001", description="地端Stable Diffusion WebUI")
]
generate_tag = Tag(name='generate', description='圖像生成操作')
app = OpenAPI(__name__, info=info, servers=servers)


# 初始化 Firebase Admin SDK
cred = credentials.Certificate("/app/stable-diffusion-customapi-firebase-adminsdk-bzguv-d0beefeec8.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'stable-diffusion-customapi.appspot.com'
})

# 圖片儲存路徑
IMAGE_FOLDER = '/app/images'
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Stable Diffusion WebUI API endpoint (預設網址)
STABLE_DIFFUSION_API = "http://163.14.137.66:7860/sdapi/v1/txt2img"

class GenerateImageParams(BaseModel):
    prompt: str = Field(..., description='用於生成圖像的提示')  # 必填
    steps: int = Field(30, description='取樣步驟數')  # 預設值 30，非必填
    width: int = Field(512, description='圖像寬度')  # 預設值 512，非必填
    height: int = Field(512, description='圖像高度')  # 預設值 512，非必填
    cfg_scale: float = Field(7.0, description='CFG 比例')  # 預設值 7.0，非必填
    negative_prompt: str = Field('', description='生成圖像時要避免的內容')  # 預設值 空字串，非必填
    seed: int = Field(-1, description='隨機種子')  # 預設值 -1，非必填
    sampler_name: str = Field('DPM++ 2M', description='取樣方法')  # 預設值 'DPM++ 2M'，非必填
    batch_size: int = Field(1, description='批次大小')  # 預設值 1，非必填
    face_detector: str = Field('face_yolov8n.pt', description='使用的臉部檢測模型')  # 預設值 'face_yolov8n.pt'，非必填
    hand_detector: str = Field('hand_yolov8n.pt', description='使用的手部檢測模型')  # 預設值 'hand_yolov8n.pt'，非必填
    person_detector: str = Field('person_yolov8n-seg.pt', description='使用的人體檢測模型')  # 預設值 'person_yolov8n-seg.pt'，非必填

class GenerateImageResponse(BaseModel):
    image_url: str = Field(..., description='生成圖像的公開 URL')

class ErrorResponse(BaseModel):
    status: str = Field('error', description='錯誤狀態')
    message: str = Field(..., description='錯誤信息')

@app.post(
    '/generate',
    tags=[generate_tag],
    summary='使用 Stable Diffusion 生成圖像',
    description='根據提供的提示生成圖像',
    responses={'200': GenerateImageResponse, '500': ErrorResponse}
)
def generate_image(body: GenerateImageParams):
    """
    Generate an image using Stable Diffusion based on the provided parameters.
    """
    try:
        # 發送 API 請求至 Stable Diffusion WebUI
        payload = {
            "prompt": body.prompt,
            "negative_prompt": body.negative_prompt,
            "steps": body.steps,
            "width": body.width,
            "height": body.height,
            "cfg_scale": body.cfg_scale,
            "seed": body.seed,
            "sampler_name": body.sampler_name,
            "batch_size": body.batch_size,
            "face_detector": body.face_detector,
            "hand_detector": body.hand_detector,
            "person_detector": body.person_detector,
        }
        response = requests.post(STABLE_DIFFUSION_API, json=payload)

        if response.status_code == 200:
            result = response.json()
            # 解碼 Base64 圖片
            image_data = result['images'][0]
            image_bytes = base64.b64decode(image_data)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f'generated_image_{timestamp}.png'

            # 將圖片存為 PNG 檔案
            image_path = os.path.join(IMAGE_FOLDER, filename)
            with open(image_path, 'wb') as f:
                f.write(image_bytes)

            # 將圖片上傳至 Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(f"images/{filename}")
            blob.upload_from_filename(image_path)
            blob.make_public()

            # 獲取公開的圖片 URL
            image_url = blob.public_url

            # 回傳圖片的公開 URL
            return image_url,200
        else:
            return ErrorResponse(message=f"Stable Diffusion API error: {response.text}"), 500
    except Exception as e:
        return ErrorResponse(message=f"Internal server error: {str(e)}"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```


啟動容器

```docker
docker-compose up -d
```


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162124891.png)

### 1.3.10. dify工作流建立

#### 1.3.10.1. 問題分類

主要分為新聞、圖片、問候語、其他，根據不同的流程會到達不同的地方

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162127158.png)

#### 1.3.10.2. 知識庫建立

這邊將先前撰寫的`python爬蟲程式`結果會寫入這個`知識庫`，這裡就可以直接使用

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162129907.png)


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162129527.png)


#### 1.3.10.3. 判斷提問相關性-LLM

這個步驟是判斷使用者的提問和知識庫是否有相關，會回傳一個結果，用於後續的判斷

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162131168.png)

#### 1.3.10.4. JSON Parse

這個步驟是為了解析剛才的結果，因為回傳是JSON格式

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162133054.png)

#### 1.3.10.5. 條件判斷

這個步驟是為了判斷，若提問不相關就走上方，提問相關就走下方

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162134124.png)

#### 1.3.10.6. GoogleSearch

這個步驟是如果提問不相關，就串接此API直接從`網路查詢`資料

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162135551.png)

#### 1.3.10.7. Json格式轉字串程式碼

這個步驟是為了將google search的回傳結果轉換為字串，因為`LLM`的不吃`JSON格式`
```python
import json
def main(http_response: str) -> str:
    # 如果傳入的 http_response 已是 Python 物件（dict），則無需解析
    if isinstance(http_response, str):
        data = json.loads(http_response)  # 將 JSON 字串轉換為 Python 字典
    else:
        data = http_response  # 已是 Python 字典
    # 將 organic_results 轉為 JSON 字串格式
    return {'result':json.dumps(data, ensure_ascii=False, indent=4)}
```

#### 1.3.10.8. 根據google回覆-LLM

這個步驟用來撰寫一段提示詞，根據使用者的詢問回傳適當的結果

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162139647.png)

#### 1.3.10.9. GOOGLESEARCH問題回覆

用於最終結果呈現

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162141915.png)

#### 1.3.10.10. 根據知識庫回覆-LLM

這個步驟用來撰寫一段提示詞，根據使用者的詢問回傳適當的結果

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162142926.png)

#### 1.3.10.11. 知識庫問題回覆

用於最終結果呈現

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162143590.png)


#### 1.3.10.12. 建立自定義小工具

請先進入這個網址
http://localhost:5001/openapi/swagger

點擊此連結

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162146474.png)

把這整段語法複製起來

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162147027.png)


點擊工具->自定義 -> 建立自定義工具
1. 輸入工具名稱
2. 貼上剛才複製的語法
3. 確認語法無誤，若有錯誤網站會直接跳出錯誤訊息
4. 可用工具旁邊有測試按鈕可點擊測試，這邊就不示範
5. 點擊儲存

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162148202.png)

#### 1.3.10.13. 自定義小工具流程設定

generate_image_generate_post

這裡唯一的必填欄位是promt，其餘都是非必填(超參數)

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162151974.png)


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162152075.png)


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162152714.png)


#### 1.3.10.14. 判斷條件設定

因為這邊想要串接到`LINEBOT`，但發現`dify`和`LINEBOT`回傳格式不同，因此這邊多了一個判斷條件，若字詞包含`dify`走上方，否則走下方

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162153639.png)


#### 1.3.10.15. 圖檔語法轉換

這邊多了一個語法轉換，語法如下

```jinja2
!["圖片1"]({{ imageURL  }})
```

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162155827.png)

#### 1.3.10.16. dify圖檔呈現結果

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162156819.png)

#### 1.3.10.17. LINEBOT圖檔呈現結果

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410162157069.png)


### 1.3.11. 多圖檔回傳邏輯撰寫

主要是在`handle_message`增加邏輯判斷處理，這邊有個重要的地方是`image_url`必須是`公開的網址`，若是`私人網址`可能會導致圖片回傳呈現有問題。

```python
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
            image_url = None
            for url in urls:
                decoded_url = unquote(url)
                cleaned_content = cleaned_content.replace(url, decoded_url)
                # 如果是圖片 URL，就存記下來
                if decoded_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_url = decoded_url
            print(f'image_url: {image_url}')
            # 如果是圖片 URL，正確地使用 ImageSendMessage 回傳
            messages = [TextSendMessage(text=cleaned_content)]
            if image_url:
                messages = [ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)]
            line_bot_api.reply_message(event.reply_token, messages)
```


### 1.3.12. 增加關鍵字搜尋圖片功能

參數定義及測試可以參考 https://serpapi.com/playground

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231833269.png)


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231834468.png)


### 1.3.13. 解析JSON格式語法

按照以下步驟建立
1. 輸入變量名稱->http_response
2. 變數選擇body
3. 貼上下方的python語法
4. 輸出變量名稱->imageURLs
5. 回傳格式->這邊要選擇`Array[Object]`，不是`String`

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231837081.png)

```python
import json
import random
import re

def main(http_response: str) -> list:
    try:
        # 將 http_response 轉換為 Python 字典
        data = json.loads(http_response)
        
        # 確保 images_results 存在並且是列表
        images_results = data.get('images_results', [])
        
        if not isinstance(images_results, list):
            return [{'error': 'images_results is not a valid list'}]
            
        # 過濾出副檔名為 .jpg、.jpeg、.png 的圖片
        valid_images = [item for item in images_results if isinstance(item, dict) and 'thumbnail' in item and re.search(r'\.(jpg|jpeg|png)$', item['thumbnail'], re.IGNORECASE)]

  
        # 隨機選取 5 個 thumbnail URL（如果列表中少於 5 個，則返回所有）
        random_images = random.sample(valid_images, min(5, len(valid_images)))
        image_urls = [{'thumbnail': item['thumbnail']} for item in random_images]


        # 返回隨機 5 個圖片的 URL 列表
        return {
            'imageURLs': image_urls
        }

    except json.JSONDecodeError:
        # 捕捉 JSON 解析錯誤
        return [{'error': 'Invalid JSON format'}]

    except TypeError as e:
        # 捕捉其他可能的錯誤
        return [{'error': f'An unexpected error occurred: {str(e)}'}]

    except ValueError:
        # 捕捉 random.sample 的錯誤（如列表為空時）
        return [{'error': 'No images available to select'}]
```


### 1.3.14. 搜圖圖檔語法轉換

按照以下步驟建立
1. 輸入變量名稱->imageURLs
2. 變數選擇解析完成後的`Array[Object]`
3. 貼上下方的python語法
4. 輸出變量名稱->imageURLs
5. 回傳格式->這邊要選擇`Array[Object]`，不是`String`

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231902898.png)

```Jinja2
{% for item in imageURLs %}
![圖片{{ loop.index }}]({{ item.thumbnail }})
{% endfor %}
```

### 1.3.15. 搜圖圖檔呈現

將前一步驟輸出的變數放入模板內即可

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231907038.png)


### 1.3.16. LINEBOT邏輯改寫

按照以下步驟建立
1. 增加問候語、AI文生圖判斷邏輯，符合條件回傳相對應的文字及貼圖
2. 宣告陣列存放`image_urls`，若生成的是圖片，則先回傳圖片再傳文字，若生成的是文字，則直接回傳文字訊息


```python
# 處理 LINE 傳送過來的訊息  
@handler.add(MessageEvent, message=TextMessage)  
def handle_message(event):  
    user_message = event.message.text  
  
    # 判斷是否為問候語  
    greetings = ["你好", "嗨", "哈囉", "您好", "早安", "晚安", "hi", "hello"]  
    if not any(greeting.lower() in user_message.lower() for greeting in greetings):  
        # 先使用 push_message 回應用戶一個「查詢中請稍候」的訊息和貼圖  
        line_bot_api.push_message(  
            event.source.user_id,  
            [                TextSendMessage(text="收到您的關鍵字輸入，我正在進行查詢處理...，請稍候大約一分鐘左右..."),  
                StickerSendMessage(package_id="6362", sticker_id="11087930"),  
                StickerSendMessage(package_id="6362", sticker_id="11087931")  
            ]        )    
    else:  
        line_bot_api.push_message(  
            event.source.user_id,  
            [                TextSendMessage(text="收到您的 AI 關鍵字輸入，我正在進行生成處理...，請稍候大約一分鐘左右..."),  
                StickerSendMessage(package_id="6362", sticker_id="11087930"),  
                StickerSendMessage(package_id="6362", sticker_id="11087931")  
            ]        )  
    # 傳送訊息到 Dify    headers = {  
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
  
            # 解碼 URLs 並收集圖片 URL            image_urls = []  
            for url in urls:  
                decoded_url = unquote(url)  
                cleaned_content = cleaned_content.replace(url, decoded_url)  
                # 如果是圖片 URL，就存記下來  
                if decoded_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  
                    image_urls.append(decoded_url)  
            print(f'image_url: {image_urls}')  
            # 分開回應每個圖片訊息  
            if image_urls:  
                for image_url in image_urls:  
                    line_bot_api.push_message(  
                        event.source.user_id,  
                        ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)  
                    )                    # 傳送圖片的連結  
                    line_bot_api.push_message(  
                        event.source.user_id,  
                        TextSendMessage(text=f"您好，根據您查詢的關鍵字【{user_message}】\n查詢的圖片結果如下↓\n圖片連結：{image_url}")  
                    )            
            else:  
                messages = [TextSendMessage(text=cleaned_content)]  
                line_bot_api.reply_message(event.reply_token, messages)  
  
        else:  
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

### 1.3.17. 測試結果

LINEBOT->查詢圖片

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231914451.png)



LINEBOT->查詢新聞

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231915578.png)


![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231916202.png)


LINEBOT->AI生成圖片

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231917339.png)

![](https://raw.githubusercontent.com/Mark850409/20241013_LineBotWithDify/refs/heads/master/images/202410231917943.png)