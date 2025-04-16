from flask import Flask
import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__)) #讓__file__可以在任何地方使用 
''''
PS:在 Python 的各種檔案路徑調用中,
常常會有因為當前所在資料夾與測試環境不同而導致抓不到檔案的情況,
因此通常會使用 os.path.dirname(__file__) 取得當前檔案的所在資料夾後轉為絕對路徑確保之後的操作路徑正確。
BY 翁好🐑
'''
load_dotenv(os.path.join(BASEDIR, '.env'),override=True) #從.env檔案讀取環境變數，override=True表示如果已經存在的環境變數會被覆蓋
TOKEN = os.getenv("TOKEN") # Token
CLIENT_ID = os.getenv("CLIENT_ID") # 客戶端ID
CLIENT_SECRET = os.getenv("CLIENT_SECRET") # 客戶端密鑰
REDIRECT_URI = os.getenv("REDIRECT_URI") # 重定向URI
OAUTH_URL ="https://discord.com/oauth2/authorize?client_id=" + CLIENT_ID +"&response_type=code&redirect_uri=" + REDIRECT_URI + "&scope=identify+email" 
#?key=value&key2=value2
#這個網址是用來讓使用者授權應用程式訪問他們的 Discord 帳戶資訊用的

class Config(object): #設定Flask的配置類別
    JSON_AS_ASCII = False #讓JSON的編碼不使用ASCII編碼，這樣可以正確顯示中文
    SECRET_KEY =os.urandom(24) #加密session資料