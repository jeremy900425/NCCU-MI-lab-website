
from DBconnector import get_db_connection
import bcrypt

def register_account(username, password):
    # 建立資料庫連線
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 檢查使用者帳號是否已存在
        cursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
        if cursor.fetchone():
            print("註冊失敗：帳號已存在")
            return False

        # 加密密碼
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # 新增使用者
        cursor.execute("INSERT INTO Users (Username, pwd) VALUES (%s, %s)", (username, hashed_password))

        conn.commit()
        print("註冊成功！")
        return True

    except Exception as e:
        print(f"發生錯誤：{e}")
        return False

    finally:
        cursor.close()
        conn.close()
register_account("test2", "123")