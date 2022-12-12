# django-job-search 

## Environment

```
Python 3.9
MySQL 8.0
Django 4.0.2
```

## Local development

1. 建立Python虛擬環境

```shell
$ pip install virtualenv 
$ virtualenv venv     
```

2. 啟動虛擬環境
  
```shell
$ venv\Scripts\activate
```

3. 安裝套件

```shell
$ pip install -r requirements.txt
```

4. 在MySQL建立資料庫
```
create database [databasename]
```

5. 設定.env環境變數
```shell
$ cp .env.example ./djangotext1/.env
```
6. 編輯.env 內的SECRET_KEY、DATABASE_URL、DATABASE_NAME、DATABASE_USER、DATABASE_PASS

    取得隨機的SECRET_KEY:https://djskgen.herokuapp.com/ 


7. 更新資料庫
```shell
$ python manage.py migrate
```

8. 啟動 Django 
```shell
$ python manage.py runserver
```
