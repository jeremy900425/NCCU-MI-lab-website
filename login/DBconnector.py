import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

# 連線資訊
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
user =  os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

def get_db_connection():
    try:
        # 建立連線
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Data processing...")
        return conn

    except Exception as e:
        print(f"連線失敗：{e}")
        return None