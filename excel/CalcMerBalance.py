# -*- coding: utf-8 -*-
#Calculate the average daily balance of the merchant
import os
import pandas as pd
import datetime



def date_range(beginDate, endDate):
    ##获取指定日期范围所有日期列表
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
    #dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
        #date = dt.strftime("%Y-%m-%d")
    return dates


def get_files(path):
    fs = []
    for root, dirs, files in os.walk(path):
        for file in files:
            fs.append(os.path.join(root, file))
    return fs


def get_excel_data(path):
    dt = []
    tp = "1"  #1-三峡付商户，2-全景平台商户
    if tp == "1":
        dtype = {'三峡付商户号': str, '三峡付商户收单日期': str}
        df = pd.read_excel(path, dtype=dtype)
        data = df.loc[:, ['三峡付商户收单日期', '三峡付商户收单金额', '该商户结算账号转出金额']].values
    elif tp == "2":
        dtype = {'全景平台商户号': str, '全景平台商户收单日期': str}
        df = pd.read_excel(path, dtype=dtype)
        data = df.loc[:, ['全景平台商户收单日期', '全景平台商户收单金额', '该商户结算账号转出金额']].values

    mer = df.iloc[0, 0]  #读取第0行第0列的值，这里不需要嵌套列表
    # print("读取指定行的数据：\n{0}".format(mer))
    for t in data:
        dt.append(t[0])
    return (data, mer, dt[0], dt[-1])


def calc_avg_balance(a, b, mode):
    #计算日均余额，a为结算金额，b为转出金额
    size = len(a)
    n = []
    if a[0] - b[0] < 0:
        n.append(0)
    else:
        n.append(a[0] - b[0])
    #第一天的累积数
    for i in range(1, size):
        if n[i - 1] + a[i] - b[i] < 0:
            n.append(0)
        else:
            n.append(n[i - 1] + a[i] - b[i])
    #第n天的累积数
    if mode == "1":
        banlce = int(sum(n) / 365)
    elif mode == "2":
        banlce = int(sum(n) / len(n))
    else:
        print("不支持的模式！")
        exit(0)
    # print("年日均余额：", int(sum(n) / 365))
    print("年日均余额：", banlce)
    d = banlce / sum(a)
    print('留存率: {:.2%}'.format(d))
    print("-------------------")
    return (banlce)


def excel2list(path):
    #读取电子表格文件存入list
    data_excle = get_excel_data(path)
    begin = data_excle[2]
    end = data_excle[3]
    dates = []
    dates = date_range(begin, end)
    amount = []
    transfer = []
    flag = True
    for i in dates:
        for j in data_excle[0]:
            if j[0] == i:
                amount.append(j[1])
                transfer.append(j[2])
                flag = True
                break
            else:
                flag = False
        if flag == False:
            amount.append(0)
            transfer.append(0)
    Merchant = data_excle[1]
    return (Merchant, amount, transfer)


if __name__ == '__main__':
    Clearing = []
    Balance = []
    print("日均余额结算模式：\r\n 1-按365天计算\r\n 2-按实际收单日期计算")
    mode = input("请选择计算模式：")
    files = get_files('./test-sxp/')
    for i in files:
        lists = excel2list(i)
        Clearing.append(sum(lists[1]))
        print("商户号：", lists[0])
        avg_balance = calc_avg_balance(lists[1], lists[2], mode)
        Balance.append(avg_balance)
    print("所有商户总结算金额：", int(sum(Clearing)))
    print("所有商户年日均余额：", int(sum(Balance)))
    print("收单资金留存率：{:.2%}".format(sum(Balance) / sum(Clearing)))