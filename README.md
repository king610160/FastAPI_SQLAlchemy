# FastAPI實作 - Admin功能

## 使用之前...
請先確認有安裝python及pip

## 複製專案到本地
1. Fork
2. git clone + 專案網址

## 初始化
```
pip install -r requirements.txt # 安裝套件
```

## 啟動FastAPI伺服器
```
uvicorn main:app --reload
```

## 若看到此行訊息，請打開下列網址
```
Uvicorn running on http://127.0.0.1:8000 
```

請至 http://127.0.0.1:8000  開啟網站
<br/>
<br/>

## 如何使用API
1. 請至 http://127.0.0.1:8000/docs ，使用Swagger UI測試API
2. 請使用Postman測試API

# 此處使用http://127.0.0.1:8000/docs中的Swager UI介面操作
## 建立一名使用者



<br>

# 開發工具
- Python 3.9.7
- FastAPI 0.110.0
- Uvicorn 0.27.1
- Bcrypt 4.1.2
- Pytest 8.0.2
- Httpx 0.27.0