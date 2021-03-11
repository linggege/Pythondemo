import sqlite3
import json
import platform
import os
import locale
locale.setlocale(locale.LC_ALL,'')
datestr = input("缴费开始日期：")
datesrt1 = input("缴费截止日期：")
allfee=0
conn = sqlite3.connect("school_fee.db")
c = conn.cursor()
sql = "select distinct DEPTNAME from sc_order where paymentdate >='%s' and paymentdate <='%s'" % (
    datestr, datesrt1)
cursor = c.execute(sql)
scl_list = []
for row in cursor:
    scl_list.append(row[0])
if len(scl_list) == 0:
    print('未查询到缴费学校')
else:
    for school in scl_list:
        sql_fs = "select sum(paymentTotal) from sc_order where paymentdate >='%s' and paymentdate <='%s'\
      and deptname like \'%s\' and datatype=1" % (datestr, datesrt1, school)
        sql_wl = "select sum(paymentTotal) from sc_order  where paymentdate >='%s' and paymentdate <='%s'\
      and deptname like \'%s\' and datatype=2" % (datestr, datesrt1, school)
        print('----------')
        print(school)
        c1 = c.execute(sql_fs)
        for row1 in c1:
            if row1[0] is None:
                fs = 0
            else:
                fs = row1[0]
        c2 = c.execute(sql_wl)
        for row2 in c2:
            if row2[0] is None:
                wl = 0
            else:
                wl = row2[0]
        print(" 非税资金：", locale.currency(fs,grouping=True))
        print(" 往来资金：", locale.currency(wl,grouping=True))
        hj=fs+wl
        allfee=allfee+hj
        print(' 合计：', locale.currency(hj,grouping=True))
        print("===========")
        print("到账合计：",locale.currency(allfee,grouping=True))

conn.close()