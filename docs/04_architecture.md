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
- **topic**: (必須) AIに生成させたいお題やキーワード。

#### 成功レスポンス (200 OK)
```json
{
  "marp_content": "string"
}
```
- **marp_content**: AIが生成したMarp形式のテキスト。

#### エラーレスポンス (400 Bad Request)
```json
{
  "error": "No topic provided"
}
```

#### エラーレスポDンス (500 Internal Server Error)
```json
{
  "error": "Failed to generate content from AI"
}
```
