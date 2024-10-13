import requests
from bs4 import BeautifulSoup
import csv
# Yahoo 台灣娛樂新聞的 URL
url = 'https://tw.news.yahoo.com/entertainment/archive/'

# 發送請求
response = requests.get(url)

# 檢查請求是否成功
if response.status_code == 200:
    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有目標區塊程式碼 (根據 class 名稱)
    items = soup.find_all('li', class_='StreamMegaItem')

    # 開啟 CSV 檔案以供寫入
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # 定義欄位名稱
        fieldnames = ['標題', '內文摘要', '圖片網址', '文章網址', '來源摘要', '時間']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 寫入標題列
        writer.writeheader()

        # 遍歷每個區塊，提取所需資訊
        for item in items:
            # 標題
            title_element = item.find('h3', class_='Mb(5px)')
            title = title_element.get_text(strip=True) if title_element else 'N/A'

            # 內文摘要
            summary_element = item.find('p', class_='Mt(8px) Lh(1.4) Fz(16px) C($c-fuji-grey-l) LineClamp(2,44px) M(0)')
            summary = summary_element.get_text(strip=True) if summary_element else 'N/A'

            # 圖片網址
            image_element = item.find('img')
            image_url = image_element['src'] if image_element and 'src' in image_element.attrs else 'N/A'

            # 文章網址
            link_element = item.find('a', class_='mega-item-header-link')
            article_url = 'https://tw.news.yahoo.com/' + link_element[
                'href'] if link_element and 'href' in link_element.attrs else 'N/A'

            # 時間
            # 時間和來源摘要
            time_element = item.find('div', class_='C(#959595) Fz(13px) C($c-fuji-grey-f) Fw(n)! Mend(14px)! D(ib) Mb(6px)')
            if time_element:
                time_info = time_element.get_text(strip=True)
                # 分割時間和來源摘要
                source, time_posted = time_info.split(' • ')
            else:
                source, time_posted = 'N/A', 'N/A'

            # 寫入到 CSV 檔案
            writer.writerow({
                '標題': title,
                '內文摘要': summary,
                '圖片網址': image_url,
                '文章網址': article_url,
                '來源摘要': source,
                '時間': time_posted
            })

            # 輸出取得的資訊
            print(f'標題: {title}')
            print(f'內文摘要: {summary}')
            print(f'圖片網址: {image_url}')
            print(f'文章網址: {article_url}')
            print(f'來源摘要: {source}')
            print(f'時間: {time_posted}')
            print('-' * 30)

else:
    print(f"無法訪問頁面，狀態碼：{response.status_code}")
