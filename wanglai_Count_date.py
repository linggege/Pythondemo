import sqlite3
import json
# import platform
# import os
# if platform.system() == "Windows":
#     os.system('cls')
# else:
#     os.system('clear')

datestr = input("缴费日期：")
datestr1 = input("缴费截止日期：")
#datestr = '2019'

conn = sqlite3.connect("school_fee.db")
c = conn.cursor()
sql = "select distinct DEPTNAME from sc_order where datatype=2 AND paymentdate >='%s' and paymentdate <='%s'" % (
    datestr,datestr1)
#print(sql)
cursor = c.execute(sql)
scl_list = []
for row in cursor:
    #print(row[0])
    scl_list.append(row[0])
#print(scl_list)
if len(scl_list) == 0:
    print('未查询到缴费学校')
else:
    for school in scl_list:
        sql_item = "select DISTINCT itemName FROM SC_ITEMS WHERE datatype=2 and \
        paymentdate >='%s' and paymentdate <='%s' AND deptName like \'%s\'" % (datestr,datestr1,school)
        #print(sql_item)
        item_list = []
        c1 = c.execute(sql_item)
        for row1 in c1:
            item_list.append(row1[0])
        # print(item_list)
        if len(item_list) != 0:
            print(school)
            for item in item_list:
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
                    # print(row[0])
                    print(" ", item, ":", row[0])
                c3 = c.execute(sql_2)
                for row in c2:
                    print("  交易笔数：", row[0])
        else:
        	print(school)
        	print('没有缴费项目')
conn.close()
