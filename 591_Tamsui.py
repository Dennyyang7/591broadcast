# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import emoji
import re

# 設定瀏覽器選項
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 不開啟實體瀏覽器介面
options.add_argument('--disable-gpu')

# 要抓取頁面的 URL
url = "https://rent.591.com.tw/list?section=50&price=6000$_20000$&region=3&sort=posttime_desc"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
# 啟動瀏覽器
driver = webdriver.Chrome(options=options)
driver.get(url)

# 獲取完整頁面
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# 正則
import requests
from bs4 import BeautifulSoup

import emoji
import re

# 发送GET请求
response = requests.get(url, headers=headers)

# 使用BeautifulSoup解析網頁內容
soup = BeautifulSoup(response.text, "html.parser")

# 查找所有租屋項目的div
rental_items = soup.find_all("div", class_="item-info")

response = requests.get(url, headers=headers)

# 使用BeautifulSoup解析網頁內容
soup = BeautifulSoup(response.text, "html.parser")

# 查找所有租屋項目的div
rental_items = soup.find_all("div", class_="item-info")
token = "04TBGaQS4upFGvoWwTpfsEIUUFBdbnmum666Y8ZgqY2"

def lineNotifyMessage(token, msg):
    # headers 這兩項必帶
    # token 為 LINE Notify 申請的權杖
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type":  "application/x-www-form-urlencoded"
    }

    # message: 要顯示的文字
    message = {'message': msg}
    
    #透過 POST 傳送
    req = requests.post("https://notify-api.line.me/api/notify", headers = headers, data = message)
    
    return req.status_code

#print(rental_items)
# 遍歷每個租屋項目並提取信息
for item in rental_items:
    # 提取標題和鏈接
    title_tag = item.find("a", class_="link")
    title = title_tag.get_text().strip() if title_tag else "non title"
    link = title_tag['href'] if title_tag else "non link"
    
    # 提取房型
    house_tag = item.find("div", class_="item-info-txt")
    house = house_tag.find_all("span")
    for allhouse in house:
        if "淡水區" in allhouse.get_text():
            house_tag = allhouse.get_text(strip=True)
            break

    # 取得地址
    address_tag = item.find_all("span")
    address = "無地址"
    for alladdress in address_tag:
        if "區" in alladdress.get_text():
            address = alladdress.get_text(strip=True)
            break

    # 提取坪數和樓層
    details_tags = item.find_all("span", class_="line")
    area = details_tags[0].get_text().strip() if len(details_tags) > 0 else "no area"
    floor = details_tags[1].get_text().strip() if len(details_tags) > 1 else "no floors"
    
    # 提取距離信息
    distance_info = "無距離信息"
    distance_divs = item.find_all("div", class_="item-info-txt")
    for div in distance_divs:
        if "距" in div.get_text():
            distance_info = div.get_text(strip=True)
            break

    # 提取價格
    price_tag = item.find("div", class_="item-info-price")
    price = price_tag.find("strong").get_text().strip() if price_tag else "no price"

    # 提取更新信息
    update_tag = item.find("div", class_="item-info-txt role-name ml-2px mt-2px mb-8px")
    if update_tag:
        update_info = update_tag.find_all("span", class_="line")[-2].get_text().strip() if len(update_tag.find_all("span", "line")) > 1 else "無更新信息"
        match = re.search(r'(\d+)', update_info)
        if match:
            hours = match.group(1)
    else:
        update_info = "無更新信息"
    
    #圖片
    img = item.find("div").get("image-slider")

    # 輸出結果
    '''print(f"標題: {title}")
    print(f"房型: {house_tag}")
    print(f"地址: {address}")
    print(f"坪數: {area}")
    print(f"樓層: {floor}")
    print(f"距離: {distance_info}")
    print(f"價格: {price} 元/月")
    print(f"更新信息: {update_info}")
    print("-" * 30)'''

# 表情符號

    # 取得24小時內更新的內容
    pattern = re.compile('小時內更新')  
    if int(hours) <= 24:
        # LINE訊息
        msg = (
            emoji.emojize('\nDenny推播小幫手~ :flexed_biceps: \n591網站更新啦!  \n ') +
            f"\n標題: {title}" +
            emoji.emojize('\n :house: ') + f"房型: {house_tag}" +
            emoji.emojize('\n :world_map: ') + f"地址: {address}" +
            emoji.emojize('\n :bed: ' ) + f"坪數: {area}" +
            emoji.emojize('\n :department_store: ') + f"樓層: {floor}" +
            emoji.emojize('\n :train: ') + f"距離: {distance_info}" +
            emoji.emojize('\n :money_with_wings: ') + f"價格: {price} 元/月" +
            emoji.emojize('\n :alarm_clock: ') + f"更新信息: {update_info}" +
            emoji.emojize('\n\n :globe_with_meridians: 看更詳細點↓網址 \n ') + f"{link}"
        )
        print(msg)
        lineNotifyMessage(token, msg)
        print('-------------')

# 傳送LINE訊息
lineNotifyMessage("permission", msg)  