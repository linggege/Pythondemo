# -*- coding: utf-8 -*-
import os,time
from tqdm import tqdm
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def get_files(path):
    fs = []
    for root, dirs, files in os.walk(path):
        for file in files:
            fs.append(os.path.join(root, file))  
    return fs

# 合并文件
def merge():

    input("请按回车选择需要合并表格文件夹，文件夹中请不要放入其他文件！")
    root = tk.Tk()
    root.withdraw()
    Folderpath = filedialog.askdirectory() #获得选择好的文件夹
    files = get_files(Folderpath)
    excelfile=Folderpath+"/"+"merger.xlsx"
    print(excelfile)
    arr = []
    print("正在合并数据！")
    pbar=tqdm(total=len(files))
    for i in files:
        pbar.update(1)
        arr.append(pd.read_excel(i))
    pbar.close()
    print("开始写入数据，请稍候!")
    writer = pd.ExcelWriter(excelfile)
    pd.concat(arr).to_excel(writer, 'Sheet1', index=False)
    writer.save()
    print("写入数据完成，已保存为merge.xlsx")
#拆分文件
def split():
    #print("请将excel文件名修改为“all.xlsx”，并与程序放入同一文件夹")
    input("请按回车选择要拆分的表格!")
    root = tk.Tk()
    root.withdraw()
    Filepath = filedialog.askopenfilename() #获得选择好的文件
    data = pd.read_excel(Filepath)
    print("要拆分的表格为:",Filepath)
    splitname=input("请输入拆分列名：")
    # data = pd.read_excel("all.xlsx")
    rows = data.shape[0]  #获取行数 shape[1]获取列数
    department_list = []
    
    for i in range(rows):
        temp = data[splitname][i]
        if temp not in department_list:
            department_list.append(temp)
    
    for department in department_list:
        new_df = pd.DataFrame()
    
        for i in range (0, rows):
            if data[splitname][i] == department:
                new_df = pd.concat([new_df, data.iloc[[i],:]], axis = 0, ignore_index = True)
        new_df.to_excel(str(department)+".xlsx", sheet_name=department, index = False) 
        print(str(department)+"....OK")

if __name__ == '__main__':
    print("操作模式:","\r\n","1-拆分表格","\r\n","2-合并表格")
    nyg=input("请选择操作模式:")
    if nyg == "1":
        split()
        fuck=input("文件拆分完毕，请按回车关闭程序！")
    elif nyg == "2":
        merge()