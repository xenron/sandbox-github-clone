# Django_modelform_validation_sample

## セットアップ
```
# 任意のGit用ディレクトリへ移動
>cd path\to\dir

# GitHubからカレントディレクトリへclone
path\to\dir>git clone https://github.com/thinkAmi-sandbox/Django_modelform_validation_sample.git

# virtualenv環境の作成とactivate
# *Python3.5は、`c:\python35-32\`の下にインストール
path\to\dir>virtualenv -p c:\python35-32\python.exe env
path\to\dir>env\Scripts\activate

# requirements.txtよりインストール
(env)path\to\dir>pip install -r requirements.txt

# マイグレーション
(env)path\to\dir>python manage.py migrate

# 動作確認
## ブラウザによる方法
### 開発サーバの起動
(env)path\to\dir>python manage.py runserver
### ブラウザで入力
>start http://localhost:8000/mysite/create

## テストコードによる方法
(env)path\to\dir>python manage.py test
```

　  
## テスト環境

- Windows10
- Python 3.5.1
- Django 1.9.2

　  
## 関係するブログ

[Djangoで、CreateViewでPOST後に動作する、ModelFormやModelのバリデーションを試した - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2016/02/18/215236)