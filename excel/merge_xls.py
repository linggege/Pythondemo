import os
import xlrd
import pandas as pd
from pathlib import Path

def get_filename(file_dir):
    list=[]
    for file in os.listdir(file_dir):
        if os.path.splitext(file)[1] == '.xls' or os.path.splitext(file)[1] == '.xlsx':
            list.append(file)
    return list
def merge_xlsx(path,filenames,output_filename):
    data = []   #定义一个空list
    title = []
    path_folder = Path(path)
    for i in range(len(filenames)):
        wb = xlrd.open_workbook(path_folder / filenames[i])
        title = wb.sheets()[0].row_values(0)
        sheets=wb.nsheets
        for k in range(sheets):
        	sheet_num_data = wb.sheets()[k]
	        for j in range(1,sheet_num_data.nrows): #逐行打印
	            data.append(sheet_num_data.row_values(j))
    content= pd.DataFrame(data)
    #修改表头
    content.columns = title
    #写入excel文件
    output_path = path_folder / 'output'
    output_filename_xlsx = output_filename + '.xlsx'
    if not os.path.exists(output_path):
        print("output folder not exist, create it")
        os.mkdir(output_path)
    content.to_excel((output_path / output_filename_xlsx), header=True, index=False)
    print(filenames,"merge success")

if __name__ == "__main__":
    path = r'./' #这里无论什么平台都按照unix风格来输入文件路径
    filenames = get_filename(path)
    merge_xlsx(path,filenames,"output") #合并文件中第一个表的数据，输出到 output/sheet1.xlsx中
