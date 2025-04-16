from flask import Flask, render_template, request, redirect, url_for, session
from zenora import APIClient 
from config import Config,TOKEN,API_KEY,CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,OAUTH_URL
import random

app= Flask(__name__)
app.config.from_object(Config) #從Config類別讀取配置
client = APIClient(TOKEN, client_secret=CLIENT_SECRET, validate_token=False) #這個APIClient是用來跟Discord API溝通的，TOKEN是用來驗證身份的，client_secret是用來驗證應用程式的，validate_token=False表示不驗證token的有效性
@app.route('/')
def home():
    return redirect("/home") # 不想讓預設路徑只有一個"/"ouob

@app.route('/login')
def login():
    return redirect(OAUTH_URL)

@app.route('/oauth2/callback')
def oauth_callback():
    if "code" in request.args:  
        code = request.args["code"]  #從網址中取得code參數，
        access_token = client.oauth.get_access_token(code, REDIRECT_URI).access_token #使用code參數取得access token
        session["token"] = access_token #將access token存入session中，這樣就可以在之後的請求中使用這個token來驗證身份了
        session.permanent = True
        return redirect("/home")
    return "no code provided" ,400 #如果沒有提供code參數，就回傳400錯誤

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/home")

@app.route('/home')
def home_page():
    if "token"  in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user() #使用bearer_token來取得當前使用者的資訊
        return render_template("home.html", user=current_user)
    else:
        return redirect("/login")
@app.route('/draw-card', methods=['POST']) # 收到前端的請求(fetch)之後會執行這個函數 並回傳結果給home.html
def draw_card():
    if "token" not in session:
        return {"error": "Not authenticated"}, 401
    
    cards = ["SSR 卡片✨", "SR 卡片🌟", "R 卡片⭐", "N 卡片📄"]
    weights = [0.1, 0.2, 0.3, 0.49]  # 各種卡片的抽中機率
    result = random.choices(cards, weights=weights, k=1)[0]
    # random.choices() 函數會根據 weights 中的權重隨機選擇一個元素，k=1 表示選擇一個元素
    # 這裡的 weights 是一個列表，表示每個元素被選中的機率。權重的總和不需要等於 1。
    return {"result": result}


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
    

