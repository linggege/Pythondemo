# -*- coding: utf-8 -*-
import scrapy
from todayMovie.items import TodaymovieItem
import re
import xlrd
import xlwt
import xlutils
from xlutils import copy    #xlutils中导入copy
from openpyxl import load_workbook

class DashiyetspiderSpider(scrapy.Spider):
    name = 'dashiyetSpider'
    allowed_domains = ['http://www.dashiyetouzi.com']

    start_urls = []
    data = xlrd.open_workbook('股票分析1.xlsm')  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):  # 循环逐行打印
        if i == 0:  # 跳过第一行
            continue
        # print(table.row_values(i)[:10])  # 取前十列
        stockCode = table.row_values(i)[:10][1][2:]
        print(stockCode)
        start_urls.append('http://basic.10jqka.com.cn/' + stockCode + '/worth.html')
        start_urls.append('http://basic.10jqka.com.cn/' + stockCode + '/equity.html')
    # start_urls.append('http://basic.10jqka.com.cn/' + "002027" + '/equity.html')

    def parse(self, response):
        pass
