import sqlite3
import json
import platform
import os
# if platform.system()=="Windows":
#     os.system('cls')
# else:
#     os.system('clear')

datestr = input("缴费日期：")
datesrt1 = input("缴费截止日期：")

conn = sqlite3.connect("school_fee.db")
c = conn.cursor()
#sql = "select distinct DEPTNAME from sc_order where confirmdate like \'%s%%\'" % (
#    datestr)
#select * from sc_items WHERE paymentdate >='2019-07-27' and paymentdate<='2019-07-29'
sql = "select distinct DEPTNAME from sc_order where paymentdate >='%s' and paymentdate <='%s'" % (
    datestr,datesrt1)
cursor = c.execute(sql)
# if len(list(cursor)) == 0:
#     print('未查询到当日缴费数据')
# else:
#     print('youshuj')
#     #os.exit()
scl_list = []
for row in cursor:
    #print(row)
    #print(row[0])
    scl_list.append(row[0])
if len(scl_list)==0:
    print('未查询到缴费学校')
else:
    for school in scl_list:
        sql_fs = "select sum(paymentTotal) from sc_order where paymentdate >='%s' and paymentdate <='%s'\
      and deptname like \'%s\' and datatype=1" % (datestr,datesrt1, school)
        sql_wl = "select sum(paymentTotal) from sc_order  where paymentdate >='%s' and paymentdate <='%s'\
      and deptname like \'%s\' and datatype=2" % (datestr,datesrt1, school)
        # print(sql_fs)
        # print(sql_wl)
        print(school)
        c1 = c.execute(sql_fs)
        for row1 in c1:
            if row1[0] is None:
                fs=0
            else:
                fs=row1[0]
        c2 = c.execute(sql_wl)
        for row2 in c2:
            if row2[0] is None:
                wl=0
            else:
                wl=row2[0]        
        print(" 非税资金：", fs)
        print(" 往来资金：", wl)
        print (' 合计：',fs+wl)
conn.close()
