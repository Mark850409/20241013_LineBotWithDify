from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 設置 Chrome 參數
chrome_options = Options()
chrome_options.add_argument("--headless")  # 若需可視化，請移除此行
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # 若無需 GPU 加速，則可加入此行

# 初始化 driver 變數
driver = None

try:
    # 使用 WebDriverManager 自動獲取 ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # 訪問網站以測試功能
    driver.get("https://www.google.com")
    
    # 輸出當前標題
    print("Page title is:", driver.title)

except Exception as e:
    print("An error occurred:", e)

finally:
    # 確保 driver 被定義後再調用 quit()
    if driver:
        driver.quit()
