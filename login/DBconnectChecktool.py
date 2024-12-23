import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

# 連線資訊
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
user =  os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

try:
    # 建立連線
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    print("連線成功！")

except Exception as e:
    print(f"連線失敗：{e}")


try:
    cursor = conn.cursor()


    cursor.execute(
        "select * from files"
    )
    rows = cursor.fetchall()
    for row in rows:
        print(row) #tuple
    
    # 提交變更
    conn.commit()
    print("查詢資料成功！")
except Exception as e:
    print(f"查詢資料發生錯誤：{e}")
finally:
    cursor.close()
    conn.close()
