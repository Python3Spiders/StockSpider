# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/12/1 23:07
# file_name:        history_stock_quotes_scrapy.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

import requests

from lxml import etree

from stock_analysis.utils import myDict

import pymongo

client = pymongo.MongoClient(host="localhost",port=27017)
db = client['stock']
table_basic = db['basic']

basis = table_basic.find()
print(basis.count())
stock_basis = myDict.AllowKeyRepeatDict()
for basic in basis:
    stock_basis.add(key=basic['name'],value=basic['code'])

stock_name = '中信证券'
stock_code = stock_basis.query(key=stock_name)[0]
table_quotes = db[stock_name+'_'+stock_code]


headers = {
    'Referer': 'http://quotes.money.163.com/trade/lsjysj_600030.html?year=2019&season=4',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

base_url = 'http://quotes.money.163.com/trade/lsjysj_{code}.html'
# 2019 年
year = 2019
season = 1
# 四季度
for season in range(1,5):
    params = {
        'year':year,
        'season':season
    }
    response = requests.get(url=base_url.format(code=stock_code),headers=headers,params=params)

    html = etree.HTML(response.text)
    for tr in html.xpath('//table[@class="table_bg001 border_box limit_sale"]/tr'):
        tds = tr.xpath('.//td/text()')
        date = tds[0].replace('-','')
        open,high,low,close = tds[1],tds[2],tds[3],tds[4]
        change,change_pencentage = tds[5],tds[6]
        deal_amount,deal_money = tds[7].replace(',',''),tds[8].replace(',','') # 成交量，成交金额（万元）
        print(date,open,high,low,close,change,change_pencentage,deal_amount,deal_money)
        data = {
            'date': int(date),
            'open': open,
            'high': high,
            'low': low,
            'close': close,
            'change': change,
            'change_pencentage': change_pencentage,
            'deal_amount': deal_amount,
            'deal_money': deal_money
        }
        # 上海和深圳可能有两个同名的股票
        # 上海股市也可能有同名股票，但是code不一样
        table_quotes.update_one({'date': date}, {'$set': data}, True)