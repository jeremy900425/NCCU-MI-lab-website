import os
import bcrypt
from dotenv import load_dotenv, set_key
import secrets  # 用於生成隨機 token
from datetime import datetime, timedelta
import hmac
import hashlib
import time
import base64
import json
import DBconnector

class Authenticate:
    SECRET_KEY = "my_super_secret_key"  # 用來生成 HMAC

    def __init__(self, env_path='.env'):
        self.env_path = env_path
        self._ensure_env_file()
        load_dotenv(self.env_path)

    def _ensure_env_file(self):
        if not os.path.exists(self.env_path):
            with open(self.env_path, 'w') as f:
                f.write("DBtoken=\n")
    def normal_login(self, username, password):
        conn = DBconnector.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
            user = cursor.fetchone()
            if not user:
                return False
            if not bcrypt.checkpw(password.encode(), user[2].encode()):
                return False
            token = self._create_access_token(username)
            return True
        except Exception as e:
            print(f"Something error：{e}")
            return False
        finally:
            cursor.close()
            conn.close()


    def _create_access_token(self, username):
        expiration_time = datetime.now() + timedelta(days=1)
        expiration_timestamp = int(expiration_time.timestamp())
        
        # 將數據存為字典
        payload = {
            "username": username,
            "expire": expiration_timestamp
        }
        
        # JSON 序列化並進行 Base64 編碼
        payload_json = json.dumps(payload)
        payload_base64 = base64.urlsafe_b64encode(payload_json.encode()).decode()
        
        # 生成簽名 (HMAC)
        signature = hmac.new(self.SECRET_KEY.encode(), payload_base64.encode(), hashlib.sha256).hexdigest()
        
        # 組合成完整的 Token
        token = f"{payload_base64}.{signature}"
        
        # 更新到 .env 文件中
        set_key(self.env_path, "DBtoken", token)
        set_key(self.env_path, "DBuser", username)
        set_key(self.env_path, "DBexpire", str(expiration_timestamp))
        
        return token

    def check_expiration(self):
        """檢查 Token 的剩餘有效時間"""
        expiration_timestamp = os.getenv("DBexpire")
        if not expiration_timestamp:
            print("Error: Token no exist。")
            return
        
        current_timestamp = int(time.time())
        remaining_time = int(expiration_timestamp) - current_timestamp
        if remaining_time <= 0:
            print("Token Expired！")
        else:
            print(f"Token remaining time: {remaining_time} seconds")
    def _parse_token(self, token):
        try:
            # 分割 Token 為 Payload 和 Signature
            payload_base64, signature = token.split(".")
            
            # 驗證簽名
            expected_signature = hmac.new(self.SECRET_KEY.encode(), payload_base64.encode(), hashlib.sha256).hexdigest()
            if signature != expected_signature:
                print("Error：Token signature error！")
                return False
            
            # 解碼 Payload
            payload_json = base64.urlsafe_b64decode(payload_base64).decode()
            payload = json.loads(payload_json)
            # print(payload) {'username': 'test', 'expire': 1735022270}
            # 驗證過期時間
            current_timestamp = int(time.time())
            if current_timestamp > payload["expire"]:
                print("Error：Token expired！")
                return False
            
            print("Token verification success！")
            return True
        except Exception as e:
            print(f"Error： {e}")
            return False
# Example usage:
auth = Authenticate()
# token = auth.create_access_token("admin")
# auth.check_expiration()
# payload = auth.parse_token("eyJ1c2VybmFtZSI6ICJ0ZXN0IiwgImV4cGlyZSI6IDE3MzUwMjIyNzB9.b0195c657575e346158faefb3aa79cabc7c905d6fddfdcad0447b71c237fd178")