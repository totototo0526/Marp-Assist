# Marp Assist API仕様書 v1

## エンドポイント

### `POST /api/generate`

フロントエンドからお題を受け取り、Marp原稿を生成して返します。

#### リクエストボディ (JSON)
```json
{
  "topic": "string"
}
```

#### レスポンスボディ (成功時: 200 OK) (JSON)
```json
{
  "marp_content": "string"
}
```

#### レスポンスボディ (エラー時) (JSON)
- **400 Bad Request** (`topic`が提供されなかった場合)
```json
{
  "error": "No topic provided"
}
```
- **500 Internal Server Error** (AIのコンテンツ生成に失敗した場合)
```json
{
  "error": "Failed to generate content from AI"
}
