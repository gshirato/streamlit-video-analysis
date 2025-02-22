# streamlit-video-analysis


## Google Drive API のセットアップ
Google Drive API を使うために、Google Cloud Console で API の認証情報を取得

1. Google Cloud Console にログイン
    - Google Cloud Console にアクセス
    - 新しいプロジェクトを作成

2. Google Drive API を有効化
    - 「APIとサービス」→「ライブラリ」→「Google Drive API」を有効化

3. OAuth 2.0 認証情報を作成
    - 「認証情報」→「認証情報を作成」→「OAuth クライアント ID」
    - 「アプリケーションの種類」を「デスクトップアプリ」にする
    - `credentials.json` をダウンロード

## To deploy
- preparer `requirements.txt` using `rye list > requirements.txt`

## Reference
https://developers.google.com/drive/api/quickstart/python?hl=ja


## secrets.toml

```toml
[auth]
redirect_uri = "https://<your_app_domain>.streamlit.app/<callback_endpoint>"
cookie_secret = "<cookie_secret_of_your_choice>"
allowed_users = ["email@example.com"]

[auth.google]
client_id = "<id>"
client_secret = "<secret>"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```