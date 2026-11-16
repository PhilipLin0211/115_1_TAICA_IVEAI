# 115-1 生成式AI：文字與圖像生成的原理與實務 課程作業集

> **國立臺灣科技大學 (NTUST) 人工智慧所**  
> **學號**：M11552010  
> **姓名**：林宸平  
> **GitHub 儲存庫**：[https://github.com/PhilipLin0211/115_1_TAICA_IVEAI](https://github.com/PhilipLin0211/115_1_TAICA_IVEAI)  
> **GitHub Pages 線上作業總覽中心**：👉 **[https://philiplin0211.github.io/115_1_TAICA_IVEAI/](https://philiplin0211.github.io/115_1_TAICA_IVEAI/)**

[![GitHub Pages Portal](https://img.shields.io/badge/線上作業中心-GitHub%20Pages-success?style=for-the-badge&logo=github)](https://philiplin0211.github.io/115_1_TAICA_IVEAI/)
[![GitHub Repo](https://img.shields.io/badge/原始碼-GitHub%20Repo-blue?style=for-the-badge&logo=github)](https://github.com/PhilipLin0211/115_1_TAICA_IVEAI)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📚 課程作業列表 (Course Assignments)

| 作業編號 | 作業名稱 / 主題 | 專案成品 | 線上體驗與文件連結 | 狀態 |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **作業一 (HW 1)** | **用 Vibe Coding 做出一個互動網頁** | **《山岳馱獸包包 PackBeast Pro》**<br>登山輕量化負重與打包檢核 Web App | 🌐 [線上即時操作 (Live Demo)](https://philiplin0211.github.io/115_1_TAICA_IVEAI/%E7%94%A8%20Vibe%20Coding%20%E5%81%9A%E5%87%BA%E4%B8%80%E5%80%8B%E4%BA%92%E5%8B%95%E7%B6%B2%E9%A0%81/)<br>📖 [作業規格與開發歷程](./用%20Vibe%20Coding%20做出一個互動網頁/README.md)<br>🏗️ [系統架構圖 (Architecture)](./用%20Vibe%20Coding%20做出一個互動網頁/ARCHITECTURE.md)<br>📓 [Colab 雲端執行](./用%20Vibe%20Coding%20做出一個互動網頁/run_on_colab.ipynb) | ✅ 已發布 |
| **作業二 (HW 2)** | **建立一個自己的 AGENTS.md** | **《VS Code Dark+ 課程作業與知識中心》**<br>零透明度實色 IDE 風格入口 + 自動化資料流 (build_manifest.py + Actions) | 🌐 [線上即時操作 (Live Demo)](https://philiplin0211.github.io/115_1_TAICA_IVEAI/%E5%BB%BA%E7%AB%8B%E4%B8%80%E5%80%8B%E8%87%AA%E5%B7%B1%E7%9A%84%20%20AGENTS/)<br>📖 [AGENTS.md 規範手冊](./AGENTS.md)<br>📝 [W08 自動化架構筆記](./notes/W08_AGENTS_md_設計筆記.md)<br>📂 [作業二原始碼目錄](./建立一個自己的%20%20AGENTS/) | ✅ 已發布 |
| **期末專案 (Final Project)** | **本地 RAG 檔案管家與自動知識庫** | **《Local AI File Agent》**<br>macOS 下載目錄自動化管家 + 向量檢索 + Obsidian LLMWiki 自動筆記 | 🌐 [線上即時操作 (Live Demo)](https://philiplin0211.github.io/115_1_TAICA_IVEAI/Local%20AI%20File%20Agent/)<br>📖 [專案架構與技術文件](./Local%20AI%20File%20Agent/README.md)<br>🧪 [詳細使用與驗收指引書](./Local%20AI%20File%20Agent/VERIFICATION_GUIDE.md)<br>📅 [11月底進度追蹤與問題手冊](./Local%20AI%20File%20Agent/PROGRESS.md)<br>🏗️ [系統架構規格書](./Local%20AI%20File%20Agent/ARCHITECTURE.md)<br>📓 [Colab 雲端執行](./Local%20AI%20File%20Agent/run_on_colab.ipynb)<br>📂 [原始碼目錄](./Local%20AI%20File%20Agent/) | ✅ 已發布 (⭐ 100% 驗收結案) |
| **作業三 (HW 3)** | *規劃準備中* | *Coming Soon* | *即將推出* | ⏳ 規劃中 |

---

## 🗂️ 儲存庫目錄結構 (Repository Structure)

為利於本學期多項作業的長期維護與收錄，本儲存庫採用**模組化作業子資料夾架構**，根目錄作為 GitHub Pages 課程作業入口，各次作業獨立收錄於各自的資料夾中：

```text
115_1_TAICA_IVEAI/
├── index.html                               # 課程作業線上導覽總頁 (VS Code Dark+ IDE 風格入口)
├── AGENTS.md                                # 專案架構、設計系統規範與 AI Agent 開發守則
├── data.json                                # 課程專案、講義、筆記與影片中繼資料庫 (Manifest)
├── README.md                                # 全學期作業目錄與儲存庫說明
├── scripts/                                 # 自動化建置腳本
│   └── build_manifest.py                    # 掃描資料夾並自動更新 data.json 守護腳本
├── .github/workflows/                       # GitHub Actions 自動化工作流
│   └── update-manifest.yml                  # 檔案推播自動觸發 manifest 重新建置
├── notes/                                   # 課程實作與學習筆記 (Markdown)
│   └── W08_AGENTS_md_設計筆記.md             # W08 建立自己的 AGENTS.md 筆記
├── PPT/                                     # 課程教材講義 (01 ~ 08 週投影片與助教課)
│   ├── 01如何不焦慮地學AI(學生點開顯示未發佈).pdf
│   ├── 02神經網路的概念.pdf
│   ├── 03AI為什麼每次都不一樣？.pdf
│   ├── 04LLM只是在猜下一個字？.pdf
│   ├── 05AI怎麼記得前面說過什麼？.pdf
│   ├── 06打造自己的對話機器人.pdf
│   ├── 07讓AI看懂你的世界.pdf
│   ├── 08教AI做事的方法.pdf
│   └── 第七週助教課.pdf
│
├── 建立一個自己的  AGENTS/                   # 【作業二】建立一個自己的 AGENTS.md 子頁面
│   ├── index.html                           # 作業二展示頁 (VS Code Dark+ 零透明度風格)
│   ├── project.meta.json                    # 作業二中繼描述檔 (自動被 build_manifest.py 讀取)
│   └── README.md                            # 作業二詳細規格與設計原理說明書
│
├── Local AI File Agent/                     # 【期末專案】本地 RAG 檔案管家與自動知識庫
│   ├── index.html                           # 期末專案互動演示網頁 (Live Simulator)
│   ├── README.md                            # 專案架構設計、RAG 向量檢索與 LLMWiki 規格書
│   ├── ARCHITECTURE.md                      # 系統底層架構、狀態機與容錯設計說明書
│   ├── PROGRESS.md                          # 11月底衝刺進度表、技術對照與問題排查手冊
│   ├── VERIFICATION_GUIDE.md                # 詳細使用手冊與每週驗收標準與驗證指令書
│   ├── run_on_colab.ipynb                   # 期末專案 Google Colab 一鍵雲端執行腳本
│   ├── main.py                              # 系統常駐進入點與 Watchdog 監聽守護行程
│   ├── config.yaml                          # 系統設定檔 (路徑、模型、分類清單)
│   ├── requirements.txt                     # Python 依賴套件清單
│   ├── agent/                               # LLM 呼叫、RAG 向量檢索與 Prompt 模組
│   └── utils/                               # 文本解析、安全移動與 Obsidian Wiki 模組
│
└── 用 Vibe Coding 做出一個互動網頁/            # 【作業一】專案完整目錄
    ├── index.html                           # 作業一 Web App 本體 (山岳馱獸包包 PackBeast Pro)
    ├── README.md                            # 作業一詳細規格書、提示詞紀錄與 Vibe Coding 歷程
    ├── ARCHITECTURE.md                      # 系統架構圖與 Mermaid 流程圖說明書
    └── run_on_colab.ipynb                   # 作業一專屬 Google Colab 一鍵啟動腳本
```

---

## 🌟 期末專案亮點摘要：《本地 RAG 檔案管家與自動知識庫 (Local AI File Agent)》

* **核心技術**：100% 本地端離線推論（Ollama Qwen 2.5 Coder + nomic-embed-text）、FAISS 向量資料庫、Python watchdog、Obsidian LLMWiki。
* **特色功能**：
  1. **背景自動監控與防呆觸發**：macOS `~/Downloads` FSEvents 即時監聽，智慧排除 `.crdownload` 等暫存檔。
  2. **文本語意深度萃取**：PyMuPDF 擷取關鍵摘要，有效控管 Prompt Token 預算。
  3. **FAISS 向量 RAG 檢索**：語意維度比對過往文獻，自動判斷最適歸檔路徑與命名。
  4. **Obsidian LLMWiki 第二大腦建置**：自動產出結構化 Markdown 筆記、雙向連結 `[[雙向連結]]` 與標籤，並動態更新 `index.md`。
  5. **100% 隱私安全**：完全於本機晶片運行，免聯網、無資料洩漏風險與 API 費用。

👉 更多詳細內容請見 [Local AI File Agent/README.md](./Local%20AI%20File%20Agent/README.md) 與 [線上即時體驗](https://philiplin0211.github.io/115_1_TAICA_IVEAI/Local%20AI%20File%20Agent/)。

---

## 🌟 作業一亮點摘要：《山岳馱獸包包 PackBeast Pro》

* **核心技術**：純前端單一靜態架構（Vanilla HTML5 / CSS3 / JavaScript），零建置工具依賴，GitHub Pages Ready。
* **特色功能**：
  1. **動態負重儀表板**：體重滑桿即時計算 Base Weight (BW)、行進總重 (TPW) 與負重比。
  2. **呆萌馱獸小精靈 (SVG Mascot)**：隨負重比例即時展現不同心情、對話與動態反饋。
  3. **1-to-1 Match Scoring 配對演算法**：智慧識別自備裝備與推薦清單，杜絕重複顯示問題。
  4. **個人裝備庫與 130+ 款規格資料庫**：即時自動補全、年資燈號計算與本機 JSON 備份。
  5. **原生 Web Audio API 音效引擎**：無任何外部音效檔依賴，即時振盪器合成輕巧音效。

👉 更多詳細內容請見 [用 Vibe Coding 做出一個互動網頁/README.md](./用%20Vibe%20Coding%20做出一個互動網頁/README.md)。

---

## 🌟 作業二亮點摘要：《建立一個自己的 AGENTS.md》

* **核心技術**：VS Code Dark+ 零透明度實色設計系統、純靜態資料驅動架構、Python 守護自動化（`build_manifest.py`）、GitHub Actions CI/CD。
* **特色功能**：
  1. **零透明度實色保證**：全站 CSS 嚴禁 `rgba()`、半透明與 `backdrop-filter: blur()`，100% 實色符合工程級 IDE 標準。
  2. **自動化資料流 (CI/CD Sync)**：講義（`PPT/`）、筆記（`notes/`）與新作業資料夾推播至 GitHub 後，自動掃描並產出最新 `data.json`。
  3. **動態 Markdown 即時渲染**：使用 `marked.js` 即時解析與展示上課筆記及開發規範。
  4. **顯示名稱動態管理**：可於網頁直接修改 `displayName` 並支援一鍵匯出 `data.json`，免動實體目錄結構。

👉 更多詳細內容請見 [建立一個自己的  AGENTS/README.md](./建立一個自己的%20%20AGENTS/README.md) 與 [線上即時體驗](https://philiplin0211.github.io/115_1_TAICA_IVEAI/建立一個自己的%20%20AGENTS/)。

---

## 📅 2026-11-15 更新日誌（Changelog）

本日完成全站架構現代化升級與作業二整合，主要更動與增減功能如下：

### 1. 課程入口網站首頁改版 (`index.html`)
- **UI/UX 風格升級**：
  - 由原本的流式卡片頁面改版為 **VS Code Dark+ 零透明度 IDE 佈局**。
  - 標準四層版面：**Title Bar (36px)**、**Activity Bar (48px)**、**Explorer Sidebar (280px)**、**Editor Group** 與 **Status Bar (24px)**。
- **新增功能 (Features Added)**：
  - **資料驅動動態渲染**：首頁不寫死內容，完整讀取 `data.json` 動態建立作業樹、講義樹、筆記樹與影片清單。
  - **本地 Fallback 容錯機制**：在 `file://` 協定環境下自動啟用內建資料，確保本機雙擊開啟也能 100% 正常運作。
  - **Markdown 即時渲染檢視器**：引入 `marked.js`，點擊 `notes/*.md` 或 `AGENTS.md` 直接在編輯區渲染成排版精美之筆記。
  - **動態新增資源面板**：點擊活動列「➕」可直接填寫表單新增線上影片連結或撰寫新筆記，立即同步於當前工作階段。
  - **專案顯示名稱管理**：點擊活動列「🏷️」可直接自訂各專案展示名稱（`displayName`），無須修改實體資料夾。
  - **一鍵匯出 `data.json`**：在 Title Bar 與設定面板提供「↓ 匯出 data.json」，可將網頁中所有最新設定與新增內容打包下載儲存。
  - **內嵌即時預覽 (Embedded Preview)**：於作業詳情頁內建 iframe，可直接於 IDE 編輯區內操作作業，亦支援點擊跳轉全螢幕。
  - **側邊欄總覽入口與雙向連動**：在檔案總管最上方新增 `Overview.md (首頁)` 入口，支援點選開啟與分頁選中高亮（Active State）。
- **移除項目 (Components Removed)**：
  - 移除 Title Bar 右側的「AI 研究生」標籤元件，使頂部視窗控制列視覺更為簡潔清爽。
  - 徹底移除全站所有 `rgba()`、半透明色度與毛玻璃效果。

### 2. 新增作業二專屬子頁面 (`建立一個自己的  AGENTS/`)
- **新增檔案**：
  - `index.html`：以相同的 VS Code Dark+ 實色規範打造的展示子頁，具備返回首頁麵包屑導航。
  - `project.meta.json`：包含作業名稱、發布徽章、技術標籤與連結中繼資訊。
  - `README.md`：作業二專屬詳細規格、色彩對照表與架構說明書。

### 3. 自動化機制與規範建置
- **新增最高指導規範**：建立專案根目錄 [AGENTS.md](./AGENTS.md)。
- **建立自動化建置腳本**：建立 [scripts/build_manifest.py](./scripts/build_manifest.py)，負責掃描作業、講義與筆記，並產生最新的 [data.json](./data.json)。
- **GitHub Actions 自動推播更新**：建立 [.github/workflows/update-manifest.yml](./.github/workflows/update-manifest.yml)。
- **建立實作筆記**：建立 [notes/W08_AGENTS_md_設計筆記.md](./notes/W08_AGENTS_md_設計筆記.md)。

---

> 國立臺灣科技大學 人工智慧所 M11552010 林宸平  
> 感謝授課教師與助教的指導！
