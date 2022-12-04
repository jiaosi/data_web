import db
import requests

import re

from bs4 import BeautifulSoup

import datetime

import pandas as pd
# - 从乐居https://sc.leju.com/news/shichangchengjiao/p-74.html获得数据
# 调整 https://sc.leju.com/news/loushi/p-1.html

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

# data = []
# pattern = re.compile('[\d\.]+')
# for i in range(1,2,1):
#     url = 'https://sc.leju.com/news/loushi/p-{}.html'.format(i)
#     resp = requests.get(url, headers = headers)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     raw_house_trade = soup.find_all(class_ = 'con-content', text = re.compile('(成都市住建局住建蓉e办|成都市住建局网上政务大厅)数据显示'))
#     for raw in raw_house_trade[0]:
#         str_ = re.sub('\.\.\.\.\.\.', '', raw.get_text())
#         data.append(pattern.findall(str_))
#         break
#     print(raw_house_trade[-1])
#     print(pattern.findall(str_))

url = 'https://sc.leju.com/news/shichangchengjiao/p-{}.html'.format(1)
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

data = []
# 首页抓取关键字所在条目
url_content = soup.find_all(class_='tit', text=re.compile('市场成交'))[0]
detail_url = url_content.a['href']
detail_resp = requests.get(detail_url, headers=headers)
detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
# 详情数据
raw = detail_soup.find_all('p', style="text-indent: 2em; text-align: left;")[0]
# 解析
pattern = re.compile('[\d\.]+')
data.append(pattern.findall(raw.get_text()))

house_trade_data = pd.DataFrame(data)

house_trade_data.columns = ['year','month','day','new_total_area','new_residence_num','new_residence_area','old_total_area','old_residence_num','old_residence_area']

house_trade_data['date'] = (datetime.datetime(int(house_trade_data['year'].values), int(house_trade_data['month'].values), int(house_trade_data['day'].values))).strftime('%Y/%m/%d')

house_trade_data.fillna(0, inplace = True)

sql = "INSERT INTO mytest_db.house_trade_data(year,month,day,new_total_area,new_residence_num,new_residence_area,old_total_area,old_residence_num,old_residence_area,date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

na = tuple(house_trade_data.values[0])
mydb = db.DB()
mydb.insert_record(sql, na)
mydb.close()
# house_trade_data.to_csv('./files/house_trade_data.csv', index = False)
