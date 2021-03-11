# -*- coding: UTF-8 -*-
import sqlite3
import json
import openpyxl

# import platform
# import os
# if platform.system() == "Windows":
#     os.system('cls')
# else:
#     os.system('clear')
#write_excel()

# 万州学校缴费往来资金交易明细
# 收款人账号   02260144000001391001    收款人户名   重庆市万州区财政局
# 付款人账号   0226015360101662    付款人户名   万州学校缴费支付宝待清算内部户
# 缴费日期    2020-1-21至2020-1-25 入账日期    2020-1-26
# 学校名称    缴费项目    交易笔数（单位笔）   缴费金额（单位元）
# 重庆市万州上海中学   高中代收课本费 1344    ¥241,920.00
# 合计      1344    ¥241,920.00
wb = openpyxl.load_workbook('template.xlsx')
sheet = wb['Sheet1']
datestr = input("缴费开始日期：")
datestr1 = input("缴费截止日期：")
date_tr = input("资金到账日期：")
# datestr = '2020-01-01'
# datestr1 = '2020-02-08'
# date_tr = '2020-02-09'
#datestr = '2019'
#str = 'There are %s, %s, %s on the table.' % (fruit1,fruit2,fruit3)
if datestr == datestr1:
    dateall = datestr
else:
    dateall = '%s至%s' % (datestr, datestr1)
#print(dateall)
sheet['B4'] = dateall
sheet['D4'] = date_tr
# wsheet.write(3,1,dateall)
# wsheet.write(3,3,date_tr)
conn = sqlite3.connect("school_fee.db")
c = conn.cursor()
sql = "select distinct DEPTNAME from sc_order where datatype=2 AND paymentdate >='%s' and paymentdate <='%s'" % (
    datestr, datestr1)
#print(sql)
cursor = c.execute(sql)
scl_list = []
sums = 0  #笔数
total = 0  #总金额
for row in cursor:
    #print(row[0])
    scl_list.append(row[0])
#print(scl_list)
if len(scl_list) == 0:
    print('未查询到缴费学校')
else:
    for school in scl_list:
        sql_item = "select DISTINCT itemName FROM SC_ITEMS WHERE datatype=2 and \
        paymentdate >='%s' and paymentdate <='%s' AND deptName like \'%s\'" % (
            datestr, datestr1, school)
        #print(sql_item)
        item_list = []
        c1 = c.execute(sql_item)
        for row1 in c1:
            item_list.append(row1[0])
        # print(item_list)
        if len(item_list) != 0:
            print('------')
            print(school)
            for item in item_list:
                # sheetrow=[]
                # sheetrow[0]=school
                # print('条目：',item)
                sql_1 = "select sum(actualAmt) FROM SC_ITEMS WHERE paymentdate >='%s' and paymentdate <='%s' \
                AND deptName like \'%s\' \
                AND itemName like \'%s\'" % (datestr, datestr1, school, item)
                sql_2 = "select count(actualAmt) FROM SC_ITEMS WHERE paymentdate >='%s' and paymentdate <='%s' \
                AND deptName like \'%s\' \
                AND itemName like \'%s\'" % (datestr, datestr1, school, item)
                #print(sql_1)
                c2 = c.execute(sql_1)
                for row in c2:
                    #print(row[0])
                    #学校名称    缴费项目    交易笔数（单位笔）   缴费金额（单位元）
                    # sheetrow=['学校名称','缴费项目','交易笔数','交易笔数（单位笔）']
                    sheetrow = []
                    sheetrow.append(school)
                    sheetrow.append(item)
                    sheetrow.append("")
                    sheetrow.append(row[0])
                    # sheetrow.
                    # sheetrow[0]=school
                    # sheetrow[1]=item
                    # sheetrow[3]=row[0]
                    print(" ", item, ":", row[0])
                    total = total + row[0]
                    # wsheet.write(r,0,school)
                    # wsheet.write(r,1,item)
                    # wsheet.write(r,3,row[0])
                c3 = c.execute(sql_2)
                for row in c2:
                    print("  交易笔数：", row[0])
                    sums = sums + row[0]
                    # wsheet.write(r,2,row[0])
                    sheetrow[2] = row[0]
                    #print(sheetrow)
                    sheet.append(sheetrow)

        else:
            print(school)
            print('没有缴费项目')
conn.close()
print("======\n交易总金额：%s \n交易总笔数：%s" % (total, sums))
# wsheet.write(r,0,"合计")
# wsheet.write(r,2,sums)
# wsheet.write(r,3,total)
row = ['合计', '', sums, total]
#print(row)
sheet.append(row)
#sheet.save
#print(type(wsheet))
# wfile.save("万州学校交费往来明细"+date_tr+'.xls')
wb.save("万州学校交费往来明细" + date_tr + '.xlsx')
