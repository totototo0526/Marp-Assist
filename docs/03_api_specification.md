# Marp Assist API仕様書 v1.1

## 1. 概要
このドキュメントは、Marp Assist バックエンドAPIの仕様を定義します。

## 2. ベースURL
`/api`

## 3. エンドポイント

### 3.1. テンプレート一覧取得
- **エンドポイント:** `GET /templates`
- **説明:** 利用可能なすべてのMarpテンプレートの一覧を取得します。
- **リクエストボディ:** なし
- **成功レスポンス (200 OK):**
  ```json
  [
    {
      "name": "template_simple",
      "label": "シンプル"
    },
    {
      "name": "template_business",
      "label": "ビジネス"
    }
  ]
  ```
- **エラーレスポンス (500 Internal Server Error):**
  ```json
  {
    "error": "エラーメッセージ"
  }
  ```

### 3.2. Marp原稿生成
- **エンドポイント:** `POST /generate`
- **説明:** 指定されたお題とテンプレートに基づき、Marp形式の原稿を生成します。
- **リクエストボディ:**
  ```json
  {
    "topic": "string",
    "template_name": "string"
  }
  ```
- **成功レスポンス (200 OK):**
  ```json
  {
    "content": "生成されたMarp原稿のテキスト"
  }
  ```
- **エラーレスポンス:**
  - **400 Bad Request:**
    ```json
    {
      "error": "topicとtemplate_nameは必須です"
    }
    ```
  - **404 Not Found:** (指定されたテンプレートが存在しない場合)
    ```json
    {
      "error": "Template 'template_name' not found."
    }
    ```
  - **500 Internal Server Error:**
    ```json
    {
      "error": "サーバー内部エラーメッセージ"
    }
    ```

### 3.3. PDFダウンロード
- **エンドポイント:** `POST /download_pdf`
- **説明:** 指定されたMarkdownコンテンツをPDFファイルに変換して返します。
- **リクエストボディ:**
  ```json
  {
    "markdown": "string"
  }
  ```
- **成功レスポンス (200 OK):**
  - **Content-Type:** `application/pdf`
  - **Content-Disposition:** `attachment; filename=presentation.pdf`
  - **Body:** (PDFのバイナリデータ)
- **エラーレスポンス:**
  - **400 Bad Request:**
    ```json
    {
      "error": "markdown content is required"
    }
    ```
  - **503 Service Unavailable:** (marp-apiへの接続に失敗した場合)
    ```json
    {
      "error": "Failed to connect to marp-api: ..."
    }
    ```
  - **500 Internal Server Error:**
    ```json
    {
      "error": "サーバー内部エラーメッセージ"
    }
    ```
