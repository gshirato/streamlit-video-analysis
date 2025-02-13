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


## Reference
https://developers.google.com/drive/api/quickstart/python?hl=ja