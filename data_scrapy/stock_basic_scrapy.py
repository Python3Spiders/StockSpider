# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/12/1 19:24
# file_name:        stock_basic_scrapy.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

import requests

import pymongo


client = pymongo.MongoClient(host="localhost",port=27017)
db = client['stock']
table_basic = db['basic']
table_quotes = db['quotes']

from lxml import etree
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

response = requests.get(url='http://quote.eastmoney.com/stock_list.html',headers=headers)

html = etree.HTML(response.text.encode(response.encoding).decode('gbk'))

location = '上海'

print(len(html.xpath('//div[@id="quotesearch"]/ul/li/a/text()')))

for stock in html.xpath('//div[@id="quotesearch"]/ul/li/a/text()'):
    left = stock.index('(')
    name = stock[0:left]
    code = stock[left+1:-1]
    if name=='凌云B股':
        location = '深圳'
        print(name,code)
    data = {
        'location':location,
        'name':name,
        'code':code
    }
    # 上海和深圳可能有两个同名的股票
    # 上海股市也可能有同名股票，但是code不一样
    res = table_basic.update_one({'code':code}, {'$set': data}, True)
    # if res.modified_count>0:
    #     print(name,code)

