# PureIG Chat（純淨版 IG 私訊 iOS 客戶端）

專為個人打造的 iOS 原生聊天客戶端，徹底隔離 Instagram 推薦演算法（首頁推薦、Reels 短影音、探索動態），僅專注於「即時私訊收發」與「APNs 推播通知」。

---

## 系統架構：瀏覽器中間人（Browser-in-the-Middle）

```text
[Instagram 伺服器]
       │ (HTTPS / GraphQL / WebSocket)
       ▼
[區塊 1: agent-browser] (Python + Playwright 常駐掛載 IG 網頁版，攔截封包與擬真輸入)
       │ (REST / WebSocket: CONTRACT.md)
       ▼
[區塊 2: backend-relay] (FastAPI / Node.js + SQLite 訊息暫存、雙向路由、APNs 推播)
       │ (WebSocket: CONTRACT.md)
       ▼
[區塊 3: ios-app] (SwiftUI 原生純淨聊天前端，支援樂觀更新與通知跳轉)
```

---

## 專案目錄結構

```text
Messenger for IG/
├── README.md               # 專案總覽與地圖
├── AGENT_RULES.md          # Antigravity Agent 強制工作流與省 Token 規範
├── ig_app.md               # 專案原始企劃藍圖
├── SKILL.md                # 專案標準開發流程規範
├── .gitignore              # 敏感資料、Session 與環境忽略清單
├── docs/                   # [區塊 0] 管理文件與外部長期記憶
│   ├── CONTRACT.md         # 跨模組資料格式契約（JSON / WebSocket 規格）
│   ├── PROGRESS.md         # 開發進度與區塊百分比紀錄
│   ├── TESTING.md          # 驗收測試步驟與測試手冊
│   ├── IDEAS.md            # 分類想法庫與觸發提醒清單
│   └── ISSUES_AND_QA.md    # 錯誤踩坑日誌與專案問答知識庫
├── agent-browser/          # [區塊 1] 瀏覽器自動化 Agent (Python + Playwright)
├── backend-relay/          # [區塊 2] 中繼伺服器 (FastAPI / Node.js + SQLite)
└── ios-app/                # [區塊 3] 原生 iOS 客戶端 (SwiftUI)
```

---

## 快速導覽與文檔索引

- **通訊契約**：請參閱 [docs/CONTRACT.md](file:///Users/philiplin/Documents/NTUST/Course/115_1_TAICA_IVEAI/Messenger%20for%20IG/docs/CONTRACT.md)
- **最新進度與日誌**：請參閱 [docs/PROGRESS.md](file:///Users/philiplin/Documents/NTUST/Course/115_1_TAICA_IVEAI/Messenger%20for%20IG/docs/PROGRESS.md)
- **測試指南**：請參閱 [docs/TESTING.md](file:///Users/philiplin/Documents/NTUST/Course/115_1_TAICA_IVEAI/Messenger%20for%20IG/docs/TESTING.md)
- **專案 FAQ 與錯誤紀錄**：請參閱 [docs/ISSUES_AND_QA.md](file:///Users/philiplin/Documents/NTUST/Course/115_1_TAICA_IVEAI/Messenger%20for%20IG/docs/ISSUES_AND_QA.md)
