# Marp Assist API仕様書 v1

## エンドポイント

### `POST /api/generate`

フロントエンドからお題を受け取り、Marp原稿を生成して返します。

#### リクエストボディ (JSON)
```json
{
  "topic": "string"
}
