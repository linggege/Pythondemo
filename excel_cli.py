# -*- encoding: utf-8 -*-
_date_ = '2023/08/16 11:00:15'

import argparse
from math import ceil
import pandas as pd
from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text

parser = argparse.ArgumentParser(prog='ProgramName',
                                 description='What the program does',
                                 epilog='Text at the bottom of help')

#解析命令行参数
parser.add_argument('-f',
                    '--file-path',
                    metavar='file',
                    type=str,
                    help='Excel 文件路径')
parser.add_argument('-r', '--row', type=int, help='显示第几行')
parser.add_argument('-s', '--start', type=int, help='起始行')
parser.add_argument('-e', '--end', type=int, help='结束行')
parser.add_argument('-p', '--pagesize', type=int, help='每页显示的行数')
args = parser.parse_args()
#读取 Excel 文件
try:
    df = pd.read_excel(args.file_path)
except FileNotFoundError:
    print("文件不存在或路径错误!")
    exit()
#获取文档信息
num_rows = len(df)
file_info = f"文档路径:{args.file_path}\n总行数:{num_rows}"
if num_rows == 0:
    print('｛file_info｝内容为空')
    exit()
#默认每页显示10行
page_size = args.pagesize if args.pagesize else 10  #创建颜色样式
console = Console()
#创建表格对象
table = Table(show_header=True, header_style="bold", expand=True)
#添加列名
for column in df.columns:
    table.add_column(str(column), justify="left")  #处理可选参数
if args.row is not None:
    if args.row <= num_rows:
        row_data = [
            Text(str(data), style="bold") for data in df.iloc[args.row - 1]
        ]
        table.add_row(*row_data)
        console.print(table)
    else:
        print("行数超出范围！")
elif args.start is not None and args.end is not None:
    if args.start <= 0 or args.end <= 0:
        print("起始行或结束行数错误！")
    else:
        start_row = max(args.start - 1, 0)
        end_row = min(args.end, num_rows)
        for i in range(start_row, end_row):
            row_data = [Text(str(data), style="dim") for data in df.iloc[i]]
            table.add_row(*row_data)
        console.print(table)
else:
    num_pages = ceil(num_rows / page_size)
    current_page = 1
    start_row = (current_page - 1) * page_size
    end_row = min(start_row + page_size, num_rows)
    while True:
        #清空旧的表格内容
        table.rows.clear()
        del table
        #创建表格对象
        table = Table(show_header=True, header_style="bold", expand=True)  #添加列名
        for column in df.columns:
            table.add_column(str(column), justify="left")  #添加数据行
            for i in range(start_row, end_row):
                row_data = [
                    Text(str(data), style="green") for data in df.iloc[i]
                ]
                table.add_row(*row_data)
        #打印表格和分页信息
        console.print(table)
        console.print(f"[{current_page}/{num_pages}]")  #提示用户选择操作(翻页或退出）
        choice = input("输入命令：(n-下一页,p-上一页,q-退出）")
        if choice == "n":
            if current_page < num_pages:
                current_page += 1
        elif choice == "p":
            if current_page > 1:
                current_page -= 1
        elif choice == "q":
            break
        #计算新的起始行和结束行
        start_row = (current_page - 1) * page_size
        end_row = min(start_row + page_size, num_rows)
        if start_row < 0 or start_row >= num_rows:
            break
        #打印文档信息
console.print(file_info)
