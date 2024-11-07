# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import emoji
import re

# 設定 URL 和 headers
url = "https://rent.591.com.tw/list?section=8,9&price=5000_10000,10000_20000&sort=posttime_desc"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# 發送請求並解析網頁
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, "html.parser")

# 查找所有租屋項目的 div
rental_items = soup.find_all("div", class_="content")
token = "04TBGaQS4upFGvoWwTpfsEIUUFBdbnmum666Y8ZgqY2"

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type":  "application/x-www-form-urlencoded"
    }
    message = {'message': msg}
    req = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=message)
    return req.status_code

# 遍歷每個租屋項目並提取信息
for item in rental_items:
    # 提取標題及鏈接
    title_tag = item.find("a", class_="title")
    title = title_tag.get_text().strip() if title_tag else "無標題"
    link = title_tag['href'] if title_tag else "無連結"
    
    # 提取地址
    address_tag = item.find("div", class_="address-info")
    address = address_tag.get_text().strip() if address_tag else "無地址"
    
    # 提取距離信息
    distance_tag = item.find("div", class_="distance-info")
    distance_info = distance_tag.get_text().strip() if distance_tag else "無距離信息"
    
    # 提取價格
    price_tag = item.find("div", class_="price-info")
    price = price_tag.get_text().strip() if price_tag else "無價格"
    
    # 提取更新信息
      # 提取更新信息
    update_tag = item.find("div", class_="item-info-txt role-name ml-2px mt-2px mb-8px")
    if update_tag:
        update_info = update_tag.find_all("span", class_="line")[-2].get_text().strip() if len(update_tag.find_all("span", "line")) > 1 else "無更新信息"
        match = re.search(r'(\d+)', update_info)
        if match:
            hours = match.group(1)
    else:
        update_info = "無更新信息"
    hours = re.search(r'(\d+)', update_info).group(1) if update_tag and re.search(r'(\d+)', update_info) else 0

    # 構建推播訊息
    if int(hours) <= 24:
        msg = (
            emoji.emojize('\nDenny推播小幫手~ :flexed_biceps: \n591士林、北投區，網站更新啦!  \n ') +
            f"\n標題: {title}" +
            emoji.emojize('\n :world_map: ') + f"地址: {address}" +
            emoji.emojize('\n :train: ') + f"距離: {distance_info}" +
            emoji.emojize('\n :money_with_wings: ') + f"價格: {price}" +
            emoji.emojize('\n :alarm_clock: ') + f"更新信息: {update_info}" +
            emoji.emojize('\n\n :globe_with_meridians: 看更詳細點↓網址 \n ') + f"{link}"
        )
        if title == "無標題":
            continue        
        print(msg)
        lineNotifyMessage(token, msg)
        print('-------------')
