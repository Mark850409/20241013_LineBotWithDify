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
    # 使用 WebDriverManager 自動獲取 ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Yahoo 台灣娛樂新聞的 URL
    url = ENV_URL

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
        return False
    else:
        print(f'無法獲取資料集列表，狀態碼: {response.status_code}, 回應: {response.text}')
        return False


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
                return True  # 找到對應的文件 ID，回傳 True
        return False  # 沒有找到對應的文件 ID，回傳 False
    else:
        print(f'檢查文件失敗，狀態碼: {response.status_code}, 回應: {response.text}')
        return False


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
                    ],
                    "segmentation": {
                        "separator": "------------------------------",
                        "max_tokens": 1000
                    }
                },
                "mode": "custom"
            }
        })
    }

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
                        ],
                        "segmentation": {
                            "separator": "------------------------------",
                            "max_tokens": 1000
                        }
                    },
                    "mode": "custom"
                }
            })
        }

        # 設定檔案
        files = {
            'file': open(file_path, 'rb')
        }
        # 發送 POST 請求
        response = requests.post(api_endpoint, headers=headers, data=data, files=files)

        # 檢查回應
        if response.status_code == 200:
            print('文件成功上傳至 Dify')
        else:
            print(f'上傳失敗，狀態碼: {response.status_code}, 回應: {response.text}')


# 使用範例
txt_filename = TXT_FILENAME
dataset_id = DATASET_ID  # 請替換為您的 dataset_id
document_id = DOCUMENT_ID  # 替換為您的 document_id
api_key = DOCUMENT_API_KEY  # 請替換為您的 API 金鑰

upload_to_dify(txt_filename, dataset_id, document_id, api_key)
