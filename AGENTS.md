# AGENTS.md — 115-1 生成式AI：文字與圖像生成的原理與實務 課程作業與知識整合中心開發規範

> 本文件為 AI Agent 維護與擴充本專案的最高指導原則。任何修改、重構或新增頁面／內容前，請先完整閱讀本文件與 `data.json`。

## 1. 專案目的與核心架構
本專案為國立臺灣科技大學（NTUST）人工智慧所 **115-1《生成式AI：文字與圖像生成的原理與實務》** 課程入口網站與學習知識庫（GitHub Pages 靜態託管）。

採用 **「資料驅動（`data.json`）＋ 純靜態自動化（`scripts/build_manifest.py` + GitHub Actions）」** 架構：
- 首頁（`index.html`）不寫死作業卡片、講義或筆記清單，而是讀取 `data.json` 動態渲染左側檔案樹與中央編輯區。
- 新增 PDF 講義至 `PPT/`、新增 `.md` 筆記至 `notes/` 或新增作業資料夾後，由自動化腳本或 GitHub Actions 更新 `data.json`，網頁即自動同步顯示。

## 2. 網頁整體視覺風格規範（VS Code Dark+ 零透明度標準）
- **嚴禁使用任何半透明或毛玻璃效果**：禁止使用 `rgba()`、`hsla()`、`opacity < 1`、`backdrop-filter: blur()` 或半透明漸層，所有背景、邊框、卡片與按鈕皆須為 **100% 實色（Solid Colors）**。
- **標準 CSS 變數**：
  - `--bg-editor: #1e1e1e`（主編輯區）
  - `--bg-sidebar: #252526`（左側檔案總管）
  - `--bg-activity: #333333`（最左側活動列）
  - `--bg-tabs: #2d2d2d`（分頁列與標題列）
  - `--bg-hover: #2a2d2e` / `--bg-active: #37373d`
  - `--bg-statusbar: #007acc`（底部狀態列）
  - `--border-solid: #3c3c3c`（實色邊框）
  - `--text-main: #cccccc` / `--text-bright: #ffffff` / `--text-muted: #858585`
  - `--accent-blue: #569cd6` / `--accent-teal: #4ec9b0` / `--accent-yellow: #dcdcaa` / `--accent-orange: #ce9178`
- **字體**：程式碼與檔案樹用 `JetBrains Mono`；中文內文用 `Noto Sans TC`；英文標題用 `Outfit`。

## 3. 頁面結構（IDE 版型規範）
1. **Title Bar**：顯示課程名稱、學生資訊（`M11552010 林宸平`）與「匯出 `data.json`」按鈕。
2. **Activity Bar（48px）**：切換「檔案總管」、「新增影片連結／Markdown 筆記」、「專案顯示名稱管理」。
3. **Explorer Sidebar（270px）**：可折疊資料夾樹，對應 `assignments/`、`PPT/`、`notes/`、`videos` 與 `AGENTS.md`。
4. **Editor Group**：頂部為分頁列與麵包屑路徑，中央依選取項目顯示作業詳情、PDF 講義與關聯影片、或即時渲染的 `notes/*.md` 筆記（使用 `marked.js`）。
5. **Status Bar（24px）**：實色 `#007acc`，顯示分支與作業／講義／筆記數量統計。

## 4. 檔案命名、放置與改名規則
- **新作業資料夾**：放置於根目錄（建議英文 kebab-case），內部必須包含 `index.html`，可選配 `project.meta.json`。
- **顯示名稱與實體路徑分離**：若想修改專案名稱而不改資料夾，只需調整 `data.json` 的 `displayName`（可在網頁直接修改後匯出 `data.json`）；若更改實體資料夾名稱，執行 `python3 scripts/build_manifest.py` 即可自動更新。
- **上課筆記（`notes/`）**：一律使用 `.md` 檔案，建議命名 `W{週次}_{主題}.md`，首行使用 `# 標題`。
- **課程講義（`PPT/`）**：直接放入 `.pdf` 檔案即可自動納入掃描。

## 5. AI 修改或新增內容的強制工作流
1. **先讀規範**：先讀取 `AGENTS.md` 與 `data.json`。
2. **嚴守實色**：禁止在任何新增或修改的 CSS 中使用半透明色彩。
3. **新增作業**：建立 `<作業資料夾>/index.html`（套用相同 VS Code Dark+ 實色變數與返回首頁麵包屑），再執行 `python3 scripts/build_manifest.py` 更新 `data.json` 並同步更新 `README.md`。
4. **保留自訂資料**：更新 `data.json` 時，必須保留既有的 `displayName` 與 `videos` 影片連結。