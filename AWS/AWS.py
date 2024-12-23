import argparse
import Authenticate
import os

auth = Authenticate.Authenticate()
def login(acc, pwd):
    state = auth.normal_login(acc, pwd)
    if state:
        print(f"Sucess！Hello Account：{acc}")
    else:
        print("Login Fail! pls check your account or password")
def checkToken():
    # 執行其他指令的邏輯
    auth.check_expiration()
    

def main():
    parser = argparse.ArgumentParser(description="This is AWS Access CLI")
    subparsers = parser.add_subparsers(dest="command")

    # 登入指令，帳號與密碼作為位置參數
    login_parser = subparsers.add_parser("login", help="<acc> <pwd>")
    login_parser.add_argument("acc", help="使用者帳號")
    login_parser.add_argument("pwd", help="使用者密碼")

    # checkToken
    checkToken_parser = subparsers.add_parser("checkToken", help="(no parameter)")

    args = parser.parse_args()

    # 處理登入
    if args.command == "login":
        login(args.acc, args.pwd)
    elif args.command == "checkToken":
        checkToken()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
