# -*- coding: UTF-8 -*-
import sqlite3
import json
import requests as re
from addict import Dict
import sys
import os
import math
from tqdm import tqdm
import platform
if platform.system()=="Windows":
	os.system('cls')
	os.system('del school_fee.db')
else:
	os.system('clear')
	os.system('rm school_fee.db')
#数据库存在时，直接连接；不存在时，创建相应数据库，此时当前目录下可以找到对应的数据库文件。
conn = sqlite3.connect("school_fee.db")
conn.commit()

conn.execute('''
  CREATE TABLE if not exists "SC_ORDER" (
  "clazz" TEXT(255),
  "confirmDate" TEXT(255),
  "paymentdate" TEXT(10),
  "confirmUser" TEXT(255),
  "dataType" TEXT(255),
  "deptId" TEXT(255),
  "deptName" TEXT(255),
  "docNumber" TEXT(255),
  "gmtCreate" TEXT(255),
  "gmtModified" TEXT(255),
  "grade" TEXT(255),
  "invKey" TEXT(255),
  "invalidDate" TEXT(255),
  "invalidUser" TEXT(255),
  "isConfirm" TEXT(255),
  "isInvalid" TEXT(255),
  "isPaPrint" TEXT(255),
  "isPayCodeSyn" TEXT(255),
  "nd" TEXT(255),
  "noticeNo" TEXT(255),
  "orderNo" TEXT(255),
  "paBatch" TEXT(255),
  "paNumber" TEXT(255),
  "payCode" TEXT(255),
  "paymentTotal" TEXT(255),
  "paymentUnit" TEXT(255),
  "phone" TEXT(255),
  "printPaDate" TEXT(255),
  "printPaUser" TEXT(255),
  "region" TEXT(255),
  "remark" TEXT(255),
  "tradingType" TEXT(255),
  "uId" TEXT(255),
  "userCode" TEXT(255)
);''')
#print("当前行数 :",__file__,sys._getframe().f_lineno )

conn.execute('''
    CREATE TABLE if not exists "SC_ITEMS" (
  "actualAmt" TEXT,
  "biNumber" text,
  "deptId" text,
  "fromId" text,
  "itemCode" TEXT,
  "itemName" TEXT,
  "shouldAmt" TEXT,
  "standard" TEXT,
  "uId" text,
  "docnum" text,
  "deptName" TEXT(255),
  "confirmDate" TEXT(255),
  "paymentdate" TEXT(10),
  "dataType" TEXT(255),
  CONSTRAINT "docnum" FOREIGN KEY ("docnum") REFERENCES "order" ("docNumber") ON DELETE NO ACTION ON UPDATE NO ACTION
);''')

#创建数据库完毕
cookies = {
    'JSESSIONID': '7C5D8FC443C3F589879448358FCD326F',
    'AlteonP': 'ARP0OQzXqMBa439ojolyBQ$$',
}
headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://wpps.ccqtgb.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://wpps.ccqtgb.com/tgBank-web/bill/billPrint',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}


def Pages(style):
    #通过获取一条数据获得数据总条数，然后计算应该获取数据的页数
    payload = {
        "docNumber": "",
        "paymentUnit": "",
        "type": style,
        "isConfirm": "1",
        "grade": "",
        "clazz": "",
        "isPaPrint": "0",
        "page": "1",
        "rows": "10"
    }
    r1 = re.post('https://wpps.ccqtgb.com/tgBank-web/bill/listPrintInfo',
                 headers=headers,
                 cookies=cookies,
                 data=payload)
    data = json.loads(r1.text)
    if style == 2:
        print("往来数据总数：", data['total'])
    else:
        print("非税数据总数：", data['total'])
    rows = data['total']
    pageSize = 50
    pageSum = pageSum = (rows - 1) / pageSize + 1
    pageSum = math.ceil(pageSum)
    print("页数：", pageSum)
    return pageSum


def GetData(style):
    #获取数据并写入数据库

    n = 0
    P = Pages(style)
    pbar = tqdm(total=P)
    while n <= P:
        n = n + 1
        pbar.update(1)
        payload = {
            "docNumber": "",
            "paymentUnit": "",
            "type": style,
            "isConfirm": "1",
            "grade": "",
            "clazz": "",
            "isPaPrint": "0",
            "page": n,
            "rows": "50"
        }
        r = re.post("https://wpps.ccqtgb.com/tgBank-web/bill/listPrintInfo",
                    data=payload,
                    cookies=cookies,
                    headers=headers)
        data = Dict(json.loads(r.text))
        for rows in data['rows']:
            docNumber = rows['docNumber']
            clazz = rows['clazz']
            confirmDate = rows['confirmDate']
            paymentdate=confirmDate[0:10]
            #print(paymentdate)
            confirmUser = rows['confirmUser']
            #print(confirmUser)
            dataType = rows['dataType']
            deptId = rows['deptId']
            docNumber = rows['docNumber']
            deptName = rows["deptName"]
            payCode = rows["payCode"]
            paymentTotal = rows["paymentTotal"]
            phone = rows["phone"]
            region = rows["region"]
            orderNo = rows['orderNo']
            sql_order="INSERT INTO SC_ORDER (clazz,confirmDate,paymentdate,confirmUser,dataType,deptId,deptName,docNumber,payCode,paymentTotal,phone,region,orderNo)\
            VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
            %(clazz,confirmDate,paymentdate,confirmUser,dataType,deptId,deptName,docNumber,payCode,paymentTotal,phone,region,orderNo)
            conn.execute(sql_order)
            #写入订单数据
            conn.commit()

            for items in rows['items']:
                itemCode = items['itemCode']
                itemName = items['itemName']
                standard = items['standard']
                actualAmt = items['actualAmt']
                sql_items="INSERT INTO SC_ITEMS (docnum,confirmDate,paymentdate,itemCode,itemName,actualAmt,deptId,deptName,dataType)\
            VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"       \
                %(docNumber,confirmDate,paymentdate,itemCode,itemName,actualAmt,deptId,deptName,dataType)
                conn.execute(sql_items)
                conn.commit()
    pbar.close()


if __name__ == "__main__":
    print('=====获取非税数据开始=====')
    GetData(1)
    print('=====获取往来数据开始=====')
    GetData(2)
    print('=====获取数据结束=====')
    for row in conn.execute(
            'SELECT COUNT(*) AS "Number of Orders" FROM SC_ORDER'):
        print("订单表数据条数:", row[0])
    for row in conn.execute(
            'SELECT COUNT(*) AS "Number of items" FROM SC_ITEMS'):
        print("项目表数据条数:", row[0])

conn.close()
