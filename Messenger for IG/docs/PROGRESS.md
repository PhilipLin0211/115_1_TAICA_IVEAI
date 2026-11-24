# docs/PROGRESS.md — 專案開發進度追蹤

## 整體架構完成度總覽

- **區塊 0（基礎建設與通訊契約）**：`[██████████] 100%`
- **區塊 1（電腦端瀏覽器 Agent）**：`[░░░░░░░░░░] 0%`
- **區塊 2（中繼後端與推播服務）**：`[░░░░░░░░░░] 0%`
- **區塊 3（iOS 原生前端 App）**：`[░░░░░░░░░░] 0%`

---

## 各架構區塊詳細指標

### 區塊 0：基礎建設與通訊契約（`docs/`）
- [x] `[25%]` 建立專案骨架與六大核心管理文件（`README.md`、`AGENT_RULES.md`、`docs/*`）
- [x] `[50%]` 定義「收訊息 / 發訊息 / 已讀狀態」的標準 JSON 格式（`CONTRACT.md`）
- [x] `[25%]` 制定錯誤碼與斷線重連規範

### 區塊 1：電腦端瀏覽器 Agent（`agent-browser/`）
- [ ] `[20%]` 建立 Playwright 持久化設定檔（`user_data_dir`）腳本，支援手動登入並保存 E2EE PIN 碼狀態
- [ ] `[35%]` 實作網路層封包攔截（監聽 IG 網頁版新私訊 GraphQL/WS 封包並解析為標準 JSON）
- [ ] `[30%]` 實作擬真輸入發送器（定位 `div[role="textbox"]`，加入隨機打字延遲送出訊息）
- [ ] `[15%]` 串接中繼後端（收到新訊息時 POST 給後端；透過 WebSocket 接收後端傳來的發送指令）

### 區塊 2：中繼後端與推播服務（`backend-relay/`）
- [ ] `[25%]` 建置輕量後端框架與本地資料庫（儲存聯絡人列表與近期對話紀錄）
- [ ] `[35%]` 建立雙向 WebSocket 通道（同時管理電腦端 Agent 與 iOS App 的連線路由）
- [ ] `[20%]` 實作離線訊息佇列（當手機斷線時暫存訊息，重連後自動補發）
- [ ] `[20%]` 整合 APNs（Apple Push Notification service）推播模組

### 區塊 3：iOS 原生前端 App（`ios-app/`）
- [ ] `[25%]` 建立 SwiftUI 基礎專案與純淨雙頁面 UI（對話列表頁 + 單一聊天室頁面）
- [ ] `[35%]` 實作 WebSocket 連線管理員與本地狀態同步（對應 `CONTRACT.md` 格式）
- [ ] `[20%]` 實作訊息發送框、樂觀更新（Optimistic UI）與連線狀態指示燈
- [ ] `[20%]` 註冊系統推播權限並處理點擊通知跳轉至指定聊天室

---

## 每日開發日誌

### 2026-11-22
- **[區塊 0] 建立專案骨架與基礎記憶庫**：
  - 建立專案目錄結構（`docs/`、`agent-browser/`、`backend-relay/`、`ios-app/`）。
  - 配置 `.gitignore` 嚴格隔離敏感 Session、E2EE PIN、憑證與金鑰。
  - 初始化 `AGENT_RULES.md`、`README.md`、`docs/TESTING.md`、`docs/IDEAS.md`。
  - 收錄 `QA-001`（Windows 舊筆電運作可行性）與 `QA-002`（iOS 免費側載與推播方案）至 `docs/ISSUES_AND_QA.md`。
- **[區塊 0] 完善通訊契約與自動化驗證腳本**：
  - 完成 `docs/CONTRACT.md` 規格設計：擴充文字/多媒體訊息模型、已讀同步、雙向 WebSocket 事件、30 秒心跳 Ping/Pong 與指數退避重連策略。
  - 撰寫 `tests/test_contract.py`，通過 Markdown 提取 JSON 並進行語法與必要事件檢測。
  - **進度變更**：區塊 0 進度由 `25%` 提升至 `100%`（區塊 0 正式交付完成）。
  - **對應測試**：請參閱 `docs/TESTING.md` 中的 `TEST-0.1` 與 `TEST-0.2`。
