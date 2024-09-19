import os
import platform
import pandas as pd
list1=[]
if platform.system() == "Windows":
    os.system('cls')
else:
    os.system('clear')
f = open("order.txt", 'r', encoding='UTF-8')
lines = f.readlines()
f.close
for line in lines:
    index=line.find("G")
    gsnum=line[index:index+24]
    if len(gsnum)==24:
        list1.append(gsnum)
list1.sort()
print('接龙订单数：',len(list1))
print('接龙全局流水号：\n',list1)
excel=pd.read_excel('重庆三峡银行代销贵金属订单登记表.xlsx')
data=excel.values
list2=excel['全局流水号'].values.tolist()
list3=list(dict.fromkeys(list2))
list3.sort()
print('在线表单订单数：',len(list3))
print('在线表单全局流水号：',list3)
diff_l1_l2=set(list1).difference(set(list3))
diff_l3_l1=set(list3).difference(set(list1))
print('未填写表单流水号：',diff_l1_l2)
print('-------------------')
print('未接龙流水号：',diff_l3_l1)
