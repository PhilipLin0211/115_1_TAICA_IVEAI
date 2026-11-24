# docs/CONTRACT.md — 跨區塊通訊契約（Single Source of Truth）

本文件完整定義 `agent-browser` ↔ `backend-relay` ↔ `ios-app` 之間的所有資料交換結構（REST API 與 WebSocket），涵蓋收發訊息、已讀回執、多媒體格式、心跳機制與斷線重連。
**開發任一區塊時，請以此文件為唯一規範，嚴禁在沒有同步更新本文件的情況下私自變更傳輸欄位。**

---

## 1. 核心資料模型（Core Models）

### 1.1 訊息型態列舉（Message Types）
- `text`: 一般純文字訊息
- `image`: 圖片訊息（包含原圖 URL 或 Base64 預覽）
- `post_share`: 分享的 IG 貼文/Reels 連結
- `system`: 系統事件訊息（如加載歷史、安全提醒）

### 1.2 訊息物件（Message Object）
```json
{
  "id": "msg_1732246800_001",
  "thread_id": "thread_123456789",
  "sender_id": "user_instagram_id",
  "sender_name": "對方顯示名稱",
  "sender_username": "對方帳號",
  "type": "text",
  "content": "訊息文字內容",
  "media_payload": null,
  "timestamp": 1732246800000,
  "is_from_me": false,
  "status": "delivered"
}
```

#### 多媒體訊息範例（圖片）：
```json
{
  "id": "msg_1732246800_002",
  "thread_id": "thread_123456789",
  "sender_id": "user_instagram_id",
  "sender_name": "對方顯示名稱",
  "sender_username": "對方帳號",
  "type": "image",
  "content": "[圖片]",
  "media_payload": {
    "url": "https://instagram.fsjc1-1.fna.fbcdn.net/...",
    "preview_base64": null,
    "width": 1080,
    "height": 1920
  },
  "timestamp": 1732246805000,
  "is_from_me": false,
  "status": "delivered"
}
```

### 1.3 對話執行緒物件（Thread Object）
```json
{
  "thread_id": "thread_123456789",
  "title": "對話名稱或對方名稱",
  "is_group": false,
  "participants": [
    {
      "user_id": "user_instagram_id",
      "username": "帳號名稱",
      "display_name": "暱稱",
      "avatar_url": "https://..."
    }
  ],
  "last_message": {
    "content": "最新一則訊息...",
    "timestamp": 1732246800000,
    "sender_username": "對方帳號"
  },
  "unread_count": 0,
  "updated_at": 1732246800000
}
```

---

## 2. `agent-browser` ↔ `backend-relay` 通訊規格

### 2.1 瀏覽器 Agent 傳送新訊息給後端（HTTP POST / WS）
- **Endpoint**: `POST /api/v1/agent/messages/incoming`
- **Request Body**:
```json
{
  "event": "NEW_MESSAGE",
  "message": {
    "id": "msg_1732246800_001",
    "thread_id": "thread_123456789",
    "sender_id": "user_instagram_id",
    "sender_username": "對方帳號",
    "type": "text",
    "content": "哈囉！這是一則測試訊息",
    "media_payload": null,
    "timestamp": 1732246800000,
    "is_from_me": false
  }
}
```

### 2.2 瀏覽器 Agent 傳送「已讀狀態同步」給後端
- **Endpoint**: `POST /api/v1/agent/threads/read_receipt`
- **Request Body**:
```json
{
  "event": "THREAD_READ_SYNC",
  "thread_id": "thread_123456789",
  "last_read_watermark_timestamp": 1732246800000
}
```

### 2.3 後端派發「發送訊息」指令給瀏覽器 Agent（WebSocket）
- **Direction**: `backend-relay` -> `agent-browser`
- **Payload**:
```json
{
  "action": "SEND_MESSAGE",
  "task_id": "task_send_001",
  "thread_id": "thread_123456789",
  "content": "這是從 iOS App 發出的回覆",
  "created_at": 1732246850000
}
```

### 2.4 瀏覽器 Agent 回報發送結果
- **Direction**: `agent-browser` -> `backend-relay`
- **Payload**:
```json
{
  "event": "SEND_RESULT",
  "task_id": "task_send_001",
  "status": "success",
  "sent_message_id": "msg_1732246851_002",
  "error": null
}
```

---

## 3. `backend-relay` ↔ `ios-app` 通訊規格（WebSocket）

### 3.1 握手連線與身份驗證
- **Client Connect**: `ws://<relay-host>:<port>/ws/client?token=<AUTH_TOKEN>`
- **Server Response**:
```json
{
  "type": "AUTH_SUCCESS",
  "server_time": 1732246800000,
  "agent_connected": true,
  "unread_total": 0
}
```

### 3.2 接收即時訊息（Server -> iOS Client）
```json
{
  "type": "MESSAGE_RECEIVED",
  "data": {
    "id": "msg_1732246800_001",
    "thread_id": "thread_123456789",
    "sender_name": "對方暱稱",
    "type": "text",
    "content": "哈囉！這是一則測試訊息",
    "media_payload": null,
    "timestamp": 1732246800000,
    "is_from_me": false
  }
}
```

### 3.3 發送訊息（iOS Client -> Server）
```json
{
  "type": "SEND_MESSAGE",
  "client_msg_id": "local_msg_abc123",
  "thread_id": "thread_123456789",
  "type": "text",
  "content": "這是回覆訊息"
}
```

### 3.4 發送狀態回執（Server -> iOS Client）
```json
{
  "type": "MESSAGE_ACK",
  "client_msg_id": "local_msg_abc123",
  "status": "queued",
  "server_msg_id": "msg_1732246851_002"
}
```

### 3.5 標記對話已讀（iOS Client -> Server）
```json
{
  "type": "MARK_READ",
  "thread_id": "thread_123456789",
  "watermark_timestamp": 1732246855000
}
```

---

## 4. 心跳保活與斷線重連機制（Heartbeat & Reconnect）

### 4.1 心跳 Ping / Pong 規範
- **週期**：iOS 客戶端與 Agent 需每隔 **30 秒** 發送一次 Ping。
- **Ping (Client -> Server)**:
```json
{
  "type": "PING",
  "timestamp": 1732246800000
}
```
- **Pong (Server -> Client)**:
```json
{
  "type": "PONG",
  "timestamp": 1732246800005
}
```
- **超時判定**：連續 **2 次（60 秒）** 未收到 Pong 回應，客戶端應立即主動斷開連線並啟動重連。

### 4.2 指數退避重連策略（Exponential Backoff）
當 WebSocket 異常中斷時，iOS 客戶端與 Agent 必須遵循以下重連間隔：
1. 第 1 次重試：間隔 1 秒
2. 第 2 次重試：間隔 2 秒
3. 第 3 次重試：間隔 4 秒
4. 第 4 次重試：間隔 8 秒
5. 第 5 次及以後：固定以 15 秒 間隔重試，直到重新連線成功。

---

## 5. 錯誤代碼與狀態定義（Error Codes）

| 錯誤碼 | 名稱 | 說明 | 處理建議 |
| :--- | :--- | :--- | :--- |
| `ERR_AGENT_OFFLINE` | 瀏覽器 Agent 未在線 | 瀏覽器常駐端斷線 | 訊息已進入伺服器 SQLite 暫存佇列，等 Agent 上線後自動發送 |
| `ERR_SEND_TIMEOUT` | 發送超時 | 瀏覽器 Agent 超過 15 秒未完成模擬點擊輸入 | 後端重試一次，若仍失敗回報 iOS 發送失敗 |
| `ERR_AUTH_INVALID` | 驗證無效 | Token 錯誤或過期 | iOS 提示重新驗證連線密鑰 |
| `ERR_INPUT_BLOCKED`| 輸入元素不可見 | IG 頁面出現異常彈窗阻擋或 Session 失效 | 電腦端 Agent 需通知發出告警，排查彈窗 |
| `ERR_PAYLOAD_INVALID`| 格式不符合規範 | JSON 缺少必要欄位 | 立即返回 400 錯誤與欄位明細 |
