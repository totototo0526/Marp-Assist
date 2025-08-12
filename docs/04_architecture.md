# Marp Assist API Specification v2

This document outlines the API endpoints for the Marp Assist application.

## Endpoints

### `GET /api/templates`

Retrieves a list of available content generation templates.

#### Request
No request body.

#### Success Response (200 OK)
Returns a JSON array of template objects.
```json
[
  {
    "name": "internal_template_name",
    "label": "User-Facing Template Label"
  },
  {
    "name": "another_template",
    "label": "Another Template"
  }
]
```
- **name**: The internal identifier for the template, to be used in the `/api/generate` call.
- **label**: The user-friendly name to be displayed in the UI.

---

### `POST /api/generate`

Generates content based on a topic and a selected template.

#### Request Body (JSON)
```json
{
  "topic": "string",
  "template_name": "string"
}
```
- **topic**: (Required) The topic or keywords for the AI to generate content about.
- **template_name**: (Required) The `name` of the template to use, obtained from the `/api/templates` endpoint.

#### Success Response (200 OK)
```json
{
  "content": "string"
}
```
- **content**: The AI-generated text, formatted according to the template (e.g., as Marp Markdown).

#### Error Response (400 Bad Request)
If `topic` or `template_name` are missing.
```json
{
  "error": "topicとtemplate_nameは必須です"
}
```

#### Error Response (404 Not Found)
If the specified `template_name` does not exist.
```json
{
  "error": "テンプレート '...' が見つかりません。"
}
```

#### Error Response (500 Internal Server Error)
For general server-side errors, including issues with the AI gateway communication.
```json
{
  "error": "AIゲートウェイとの通信に失敗しました。"
}
```
