# 📖 Local AI File Agent 詳細使用手冊與每週驗收指引書 (VERIFICATION_GUIDE.md)

> **國立臺灣科技大學 (NTUST) 人工智慧所**  
> **課程**：智慧虛擬實境與人工智慧 (115_1_TAICA_IVEAI) 期末專案  
> **研究生**：林宸平 (M11552010)  
> **硬體環境**：Apple MacBook Air M5 (16GB 統一記憶體 / 1TB SSD)  
> **目標截止日**：2026 年 11 月 30 日前全數完成並通過端到端驗收

---

## 🧭 文件導航

1. [第一篇：系統詳細操作手冊 (User Manual)](#第一篇系統詳細操作手冊-user-manual)
   * 1.1 快速啟動（三種使用模式）
   * 1.2 設定檔調整與目錄綁定 (`config.yaml`)
   * 1.3 Obsidian 第二大腦筆記檢視方式
   * 1.4 審計日誌與資料夾快照查詢 (`history/audit_log.json`)
2. [第二篇：每週完成項目驗收指引 (Weekly Verification Checklist)](#第二篇每週完成項目驗收指引-weekly-verification-checklist)
   * [Week 1 驗收：基礎管線、檔案鎖定與 MOVE-ONLY 權限守衛](#-week-1-驗收基礎管線檔案鎖定與-move-only-權限守衛已達標)
   * [Week 2 驗收：RAG 向量知識庫與毫秒級語意檢索](#-week-2-驗收rag-向量知識庫與毫秒級語意檢索進行中)
   * [Week 3 驗收：LLM 結構化決策與 Obsidian 知識庫整合](#-week-3-驗收llm-結構化決策與-obsidian-知識庫整合)
   * [Week 4 驗收：端到端全系統壓力測試與展示成果結案](#-week-4-驗收端到端全系統壓力測試與展示成果結案)
3. [第三篇：常見驗收異常與排查指南 (Troubleshooting FAQ)](#第三篇常見驗收異常與排查指南-troubleshooting-faq)

---

# 第一篇：系統詳細操作手冊 (User Manual)

### 1.1 快速啟動（三種使用模式）

#### 模式 A：乾式模擬測試模式 (Dry-Run Mode) —— 推薦首次使用！
**特點**：完整跑過所有感知、RAG 檢索、LLM 推論與 Markdown 生成流程，但**不實際搬動任何實體檔案**，終端機僅輸出模擬日誌，絕對安全。
```bash
cd "Local AI File Agent"
python3 main.py --dry-run
```

#### 模式 B：正式常駐守護模式 (Production Mode)
**特點**：在背景監聽 `~/Downloads`，一旦下載完成，自動執行安全搬移並產出具備雙向連結的 Obsidian 筆記。
```bash
cd "Local AI File Agent"
python3 main.py
```
> 若欲自訂 Obsidian Vault 路徑，可帶入參數：  
> `python3 main.py --vault ~/Documents/My_Obsidian_Vault`

#### 模式 C：Google Colab 免本地環境一鍵雲端執行
**特點**：免安裝本地環境，在任何裝置打開瀏覽器即可在 Colab 雲端 GPU 實機測試。
* 👉 **開啟筆記本**：[run_on_colab.ipynb](./run_on_colab.ipynb)
* 點擊儲存格上方「Open in Colab」圖示即可依序一鍵執行！

---

### 1.2 設定檔調整與目錄綁定 (`config.yaml`)

系統的核心設定均集中於 [config.yaml](./config.yaml)：

```yaml
# 監聽與知識庫路徑
watch_directory: "~/Downloads"
vault_directory: "~/Documents/Obsidian_Vault"

# 本地 Ollama 服務設定
ollama:
  host: "http://127.0.0.1:11434"
  llm_model: "qwen2.5-coder:7b"
  embed_model: "nomic-embed-text"
  timeout_seconds: 60

# 預設分類目錄指引 (可自由新增或修改)
categories:
  - name: "AI_Research/NLP"
    description: "自然語言處理、大型語言模型、Transformer、Attention 文獻"
  - name: "Course_Materials/IVEAI"
    description: "臺科大 TAICA_IVEAI 智慧虛擬實境與人工智慧課程講義與作業"
  - name: "Finance/Receipts"
    description: "電子發票、報稅單據、硬體採購收據憑證"
  - name: "Dev_Notes/Frontend"
    description: "前端技術、React、TypeScript、CSS 與介面設計筆記"
  - name: "General/Inbox"
    description: "暫時難以歸類之一般文件與雜項檔案"
```

---

### 1.3 Obsidian 第二大腦筆記檢視方式

1. 打開 **Obsidian** 軟體，點擊「Open folder as vault」（將資料夾作為知識庫開啟）。
2. 選擇路徑：`~/Documents/Obsidian_Vault`（或您在 `config.yaml` 設定的路徑）。
3. **檢視亮點**：
   * **總索引目錄**：開啟 `index.md`，可見由 Agent 自動維護的文獻清單與分類標籤。
   * **雙向連結圖譜 (Graph View)**：點擊左側「Graph view」圖示，即可看見論文與概念（如 `[[Transformer]]`、`[[Self-Attention]]`）交織成的立體星系圖譜！
   * **導讀筆記**：每一份被歸檔的文獻旁都會有一份同名的 `.md` 導讀筆記，含 YAML Frontmatter、導讀摘要與建議行動。

---

### 1.4 審計日誌與資料夾快照查詢 (`history/audit_log.json`)

本專案遵循嚴格的稽核標準，每次檔案操作均有完整跡證：
1. **結構化 JSON 日誌**：儲存於 `Local AI File Agent/history/audit_log.json`，可用以下指令檢視最近一筆操作與當時的目錄檔案清冊：
   ```bash
   cat "history/audit_log.json" | python3 -m json.tool | tail -n 40
   ```
2. **Obsidian 人類可讀表格**：開啟 `~/Obsidian_Vault/log.md`，可檢視歷次搬移時間、檔案名稱、分類目錄與當前檔案計數。

---

# 第二篇：每週完成項目驗收指引 (Weekly Verification Checklist)

本章節為您提供每一週里程碑的**明確驗收標準 (Acceptance Criteria)**、**具體驗證指令**與**合格判斷依據**：

---

## 🎯 Week 1 驗收：基礎管線、檔案鎖定與 MOVE-ONLY 權限守衛（已達標）

### 1. 驗收項目清單
* [x] 目錄監聽守護行程 (`main.py` 與 Watchdog macOS FSEvents 整合)。
* [x] 暫存檔自動排除（過濾 `.crdownload`, `.tmp`, `.part`）。
* [x] 檔案寫入鎖定機制（雙重比對大小穩定，避免讀取半形損毀檔）。
* [x] 文本萃取與 Token 防爆（`utils/file_parser.py` 首尾頁截斷至 4,000 字元）。
* [x] **嚴格 MOVE-ONLY 權限守衛**：Agent 僅具備移動權限，任何 DELETE 或未授權動作均被硬性攔截。
* [x] **每次動作自動審計與資料夾目錄快照**（`utils/audit_logger.py` 記錄至 `audit_log.json` 與 `log.md`）。

### 2. 驗收指令
在終端機執行全管線與安全性驗證腳本：
```bash
cd "Local AI File Agent"
python3 test_pipeline.py
```

### 3. 預期輸出與合格判定依據
終端機必須完整通過 7 項測試並輸出以下關鍵字：
```text
[Test 1] Extracting file content: attention_is_all_you_need.txt ... (Extracted length: 464 chars)
[Test 2] Initializing RAG Engine & LLM Caller
[Test 3] Simulating classification & reasoning ... (Category chosen: AI_Research/NLP)
[Test 4] Testing Safe File Movement (Dry-Run) ... (Permission Verified: MOVE)
[Test 5] Testing Obsidian LLMWiki Note Generation (Dry-Run)
[Test 6] Testing Security Permission Boundary (MOVE-ONLY)
  ✅ Authorized action 'MOVE' permitted.
  🛡️ Unauthorized action 'DELETE' successfully BLOCKED!
[Test 7] Testing Audit Logger & Folder Directory Snapshot
  📜 [Audit Log Recorded] Action ID: act_...
  ✅ Audit log entry saved
=================================================================
🎉 ALL PIPELINE & SECURITY BOUNDARY CHECKS PASSED!
=================================================================
```
> **合格判定**：7 項測試全數印出綠色勾號 `✅`，且 Test 6 成功攔截非法 `DELETE` 操作即為**合格**。

---

## 🎯 Week 2 驗收：RAG 向量知識庫與毫秒級語意檢索（⭐ 100% 提前達標）

### 1. 驗收項目清單
* [x] 向量嵌入模型接口串接（同時相容現代 `/api/embed`、舊版 `/api/embeddings` 與標準庫 `urllib` 備援）。
* [x] 本地向量資料庫建立與持久化儲存 (`vector_store/metadata.json` 與 `faiss_index.bin`)。
* [x] 多層級檢索容錯架構（FAISS 優先 ➔ Numpy Cosine 矩陣計算 ➔ CJK 雙字元 N-gram 關鍵字詞元加權兜底）。
* [x] 課程 01~08 週講義與經典文獻種子資料預置與標題去重 (`seed_vector_store.py`)。
* [x] 語意檢索響應時間遠低於 50 毫秒（實測平均 **4.58 毫秒**）。
* [x] 涵蓋多模態視覺、Transformer 與對話機器人三大多主題基準評測套件。

### 2. 驗收指令

#### 步驟 2-1：初始化/重建知識庫種子索引
```bash
python3 seed_vector_store.py
```
> 預期輸出：成功載入課程講義與經典論文，建立持久化向量與元數據索引。

#### 步驟 2-2：執行多主題 RAG 語意檢索基準評測
```bash
python3 test_rag_search.py
```
*(也可加上 `--query "自訂查詢字串"` 進行單項查詢)*

### 3. 預期輸出與合格判定依據
執行評測套件將自動測試三種不同領域之查詢：
```text
====================================================================
🧪 Local AI File Agent - Week 2 RAG 語意檢索效能基準全套測試
====================================================================

[Case 1] 查詢測試: 【多模態視覺與圖像理解】
  💬 查詢句: "哪份教材有說明多模態視覺模型或讓 AI 看懂圖片？"
  🎯 Top-1 匹配: - 文獻: 07 讓 AI 看懂你的世界 | 分類: Course_Materials/IVEAI | 相似度: 0.950
  ⚡ 單次耗時: 10.12 ms
  ✅ 語意關聯性驗證：通過 (正確命中目標文獻)

[Case 2] 查詢測試: 【Transformer 與注意力機制經典文獻】
  💬 查詢句: "經典 Transformer 架構與自注意力機制論文"
  🎯 Top-1 匹配: - 文獻: 04 LLM 只是在猜下一個字？ | 分類: Course_Materials/IVEAI | 相似度: 0.950
  ⚡ 單次耗時: 1.94 ms
  ✅ 語意關聯性驗證：通過 (正確命中目標文獻)

[Case 3] 查詢測試: 【對話機器人與 Prompt Engineering】
  💬 查詢句: "如何打造專屬對話機器人與設計 Prompt 做事方法"
  🎯 Top-1 匹配: - 文獻: 06 打造自己的對話機器人 | 分類: Course_Materials/IVEAI | 相似度: 0.950
  ⚡ 單次耗時: 1.68 ms
  ✅ 語意關聯性驗證：通過 (正確命中目標文獻)

====================================================================
📊 Week 2 RAG 效能與精準度綜合評測結果：
  • 測試樣本數: 3 筆
  • 平均檢索延遲 (Average Latency): 4.58 ms (目標 < 50 ms)
  • 毫秒級極速目標達成率: 100% (4.58 ms << 50 ms)
  • 測試通過狀態: 🎉 ALL BENCHMARK CHECKS PASSED!
====================================================================
```
> **合格判定**：
> 1. Top-1 檢索出的文獻高度吻合提問語意（命中率 100%）。
> 2. 總耗時 (Latency) 必須在 **50 ms 以下**（實測 4.58 ms，達成率 100%）。

---

## 🎯 Week 3 驗收：LLM 結構化決策與 Obsidian 知識庫整合（⭐ 100% 提前達標）

### 1. 驗收項目清單
* [x] 本地模型 `qwen2.5-coder:7b` 穩定輸出合法 JSON（含 `_extract_json` 代碼標籤剝離與 Rule Fallback）。
* [x] 決策 JSON 嚴格包含 `action: "MOVE"`, `category`, `sanitized_name`, `tags`, `double_links`, `summary`。
* [x] 檔案安全搬移至目標分類子目錄，同名檔案自動附加微秒時間戳記（零覆蓋風險）。
* [x] 自動在 Obsidian Vault 目錄下生成符合規格的 Markdown 閱讀筆記（含 YAML Frontmatter、導讀摘要與建議行動）。
* [x] 自動維護 `index.md`（知識總目錄）與 `log.md`（審計日誌與目錄快照）。
* [x] 向量資料庫即時在線增量更新，新歸檔知識立即支援再次語意搜尋。
* [x] 撰寫專屬驗收腳本 `test_week3_integration.py` 驗證端到端 8 步驟完整閉環。

### 2. 驗收指令

#### 步驟 3-1：執行全端到端決策與第二大腦閉環測試
```bash
python3 test_week3_integration.py
```

#### 步驟 3-2：實地模擬常駐守護行程 (Dry-Run 模式)
啟動守護行程：
```bash
python3 main.py --dry-run
```
在另一個終端機視窗，模擬下載一個測試檔案至 `~/Downloads`：
```bash
echo "Convolutional Neural Networks for Visual Recognition and Image Classification" > ~/Downloads/test_vision_paper.txt
```

### 3. 預期輸出與合格判定依據
執行 `python3 test_week3_integration.py` 之預期輸出：
```text
======================================================================
🧠 Local AI File Agent - Week 3 全端到端決策與第二大腦整合測試
======================================================================

[步驟 1] 模擬使用者下載新檔案: 2024_Multimodal_Vision_Language_Models_Survey.txt
  • 檔案大小: 562 bytes
[步驟 2] 萃取內文與元數據 (Token 防爆截斷)...
  • 成功解析文字長度: 562 字元
[步驟 3] 執行 RAG 本地語意相似度檢索 (查詢相關課程教材)...
  • RAG 檢索命中的相似歷史紀錄: 07 讓 AI 看懂你的世界
[步驟 4] 呼叫決策引擎 (Qwen 2.5 Coder / Few-Shot JSON 規範)...
  • 決定分類路徑: AI_Research/Vision
  • 正規化新檔名: 2024_Multimodal_Vision_Language_Models_Survey.txt
  • 筆記標題: Multimodal Vision-Language Models Survey
[步驟 5] 執行 MOVE-ONLY 權限核驗與防碰撞安全搬移...
  ✅ 檔案安全搬移成功 (MOVE-ONLY 權限核可)
[步驟 6] 自動產生 Obsidian 導讀筆記與更新總索引...
  ✅ Obsidian 筆記已建立: Multimodal Vision-Language Models Survey.md
  ✅ 總索引目錄 index.md 已成功更新雙向連結！
[步驟 7] 紀錄審計日誌與目標目錄快照...
  ✅ 動作審計紀錄完成: ID act_... | 目標目錄現有檔案快照數: 2 筆
[步驟 8] 即時增量更新向量資料庫並驗證再次檢索...
  🔍 新增後的即時檢索結果: 命中 Multimodal Vision-Language Models Survey (相似度: 0.810)
  ✅ 知識庫即時自我增長閉環驗證通過！

======================================================================
🎉 WEEK 3 全端到端決策、知識庫閉環與安全防禦測試全數通過 (8/8)！
======================================================================
```
> **合格判定**：
> 1. 端到端從感知、RAG 參考、LLM 決策、MOVE-ONLY 搬移、Obsidian 導讀卡片產出、總索引維護到向量自我更新，8 大關卡無任何中斷錯誤。
> 2. 目錄快照與審計日誌如實記載。

---

## 🎯 Week 4 驗收：端到端全系統壓力測試與展示成果結案

### 1. 驗收項目清單
* [ ] 邊界條件壓力測試：連續下載 5 個檔案、超大檔案（>50MB）、二進制安裝檔（`.dmg` / `.zip`）。
* [ ] GitHub Pages 成果展示中心正常在線運作 ([Live Demo](https://philiplin0211.github.io/115_1_TAICA_IVEAI/Local%20AI%20File%20Agent/))。
* [ ] Google Colab 一鍵雲端執行 Notebook ([run_on_colab.ipynb](./run_on_colab.ipynb)) 執行順暢。
* [ ] 所有文件（`README.md`、`ARCHITECTURE.md`、`PROGRESS.md`、`VERIFICATION_GUIDE.md`）內容與程式碼完全一致。
* [ ] 準備 1~2 分鐘實機操作影片/GIF，嵌入 README。

### 2. 驗收指令
```bash
# 開啟網頁展示中心檢驗
open "index.html"

# 檢查 Git 提交狀態
git status
```
> **合格判定**：工作區為 `working tree clean`，所有線上連結無 404，網頁展示各模組運作正常。

---

# 第三篇：常見驗收異常與排查指南 (Troubleshooting FAQ)

| 異常現象 | 可能原因 | 解決步驟 |
| :--- | :--- | :--- |
| **`PermissionDeniedError`** | 程式偵測到 `MOVE` 以外的操作意圖 | 此為系統安全保護生效。請確認呼叫 `safe_move_file` 時 `requested_action` 為 `"MOVE"`。 |
| **Watchdog 丟檔沒反應** | macOS 隱私權限阻擋終端機存取 `~/Downloads` | 前往 macOS **「系統設定」➔「隱私權與安全性」➔「完全磁碟取用權限」**，勾選允許您所使用的終端機軟體。 |
| **Ollama 連線失敗或逾時** | 本機 Ollama 服務未開啟 | 在終端機執行 `ollama serve` 或啟動 Ollama App，並確認 `ollama run qwen2.5-coder:7b` 可對話。 |
| **找不到 FAISS 套件** | 尚未安裝 `faiss-cpu` | 系統已內建 Numpy 矩陣降級備援，若欲獲得最高效能可執行 `pip install faiss-cpu`。 |
| **同名檔案被覆蓋了嗎？** | 目標資料夾已存在同名檔案 | 系統內建防覆蓋機制，目標檔案若已存在會自動重命名為 `檔名_YYYYMMDD_HHMMSS.ext`，絕不覆蓋舊檔。 |

---

> **國立臺灣科技大學 (NTUST) 人工智慧所**  
> 智慧虛擬實境與人工智慧 (115_1_TAICA_IVEAI) 期末專案  
> 研究生：林宸平 (M11552010)

