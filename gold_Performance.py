import pandas as pd
import sqlite3
import os
from tabulate import tabulate  # 用于表格美化

# 读取 Excel 文件
file_path = "重庆三峡银行代销贵金属订单登记表.xlsx"
df = pd.read_excel(file_path, sheet_name="数据统计")

# 连接 SQLite 数据库（如果不存在，则会创建）
conn = sqlite3.connect("database.db")  

# 将数据写入 SQLite 数据库（如果表不存在，会自动创建）
table_name = "my_table"
df.to_sql(table_name, conn, if_exists="replace", index=False)



start_date = input("请输入统计开始日期：")  # 开始日期
end_date = input("请输入统计结束日期：") # 结束日期

# SQL 查询语句（增加交易日期的时间范围筛选）
sql1 = f"""
SELECT 机构名称, 
       SUM(推荐绩效) AS 推荐绩效, 
       SUM(经办绩效) AS 经办绩效, 
       SUM(推荐绩效) + SUM(经办绩效) AS 合计绩效
FROM (
    -- 计算推荐机构的绩效
    SELECT "推荐机构（一级）" AS 机构名称, 
           SUM(推荐机构绩效) AS 推荐绩效, 
           0 AS 经办绩效
    FROM my_table
    WHERE 交易日期 BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY "推荐机构（一级）"

    UNION ALL

    -- 计算经办机构的绩效
    SELECT "经办机构（一级）" AS 机构名称, 
           0 AS 推荐绩效, 
           SUM(经办机构绩效) AS 经办绩效
    FROM my_table
    WHERE 交易日期 BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY "经办机构（一级）"
) AS 合并表
GROUP BY 机构名称
ORDER BY 合计绩效 DESC;
"""

# 读取查询结果
df_result = pd.read_sql(sql1, conn)


# 关闭数据库连接
conn.close()
print(tabulate(df_result, headers="keys", tablefmt="grid"))

# 指定 Excel 输出文件路径
output_file = f"绩效统计_{start_date}_to_{end_date}.xlsx"

# 将查询结果写入 Excel
df_result.to_excel(output_file, index=False)

print(f"数据导入并查询完成，{start_date} 至 {end_date} 的结果已导出到 {output_file}！")
os.system("pause")
