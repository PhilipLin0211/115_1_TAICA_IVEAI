# LLM Wiki × 教學 HTML 簡報：AI Agents 是什麼？

> **115-1 TAICA《生成式 AI：文字與圖像生成的原理與實務》作業**  
> **繳交者**：台科大 人工智慧跨域科技研究所 碩一 M11552010 林宸平

## 專案簡介
本專案針對「**AI Agents（自主型語言模型代理人）**」領域，從網路蒐集 5 篇具代表性的官方工程指南、技術部落格與經典論文，透過「先制定 `AGENTS.md` 討論規格、再增量 Ingest 建構知識庫」的方式建立結構化 LLM Wiki，並以該 Wiki 為唯一知識來源，產製零基礎友善的互動式 HTML 教學簡報。

## 目錄結構
```text
.
├── AGENTS.md                  # AI 協作憲法與 Ingest / 簡報生成檢查規則
├── README.md                  # 專案說明與部署指南
├── index.html                 # 教學 HTML 簡報入口頁（與 slides/index.html 同步）
├── wiki/
│   ├── index.md               # LLM Wiki 總目錄與概念演進圖
│   ├── sources/               # 5 篇網路蒐集文獻摘要卡
│   │   ├── src-01-lilian-weng-agents.md
│   │   ├── src-02-yao-2022-react.md
│   │   ├── src-03-schick-2023-toolformer.md
│   │   ├── src-04-anthropic-building-agents.md
│   │   └── src-05-park-2023-generative-agents.md
│   └── concepts/              # 結構化 Wiki 概念條目
│       ├── 01-what-is-an-ai-agent.md
│       ├── 02-planning-and-react.md
│       ├── 03-memory-architecture.md
│       ├── 04-tool-use-and-actions.md
│       └── 05-workflows-vs-autonomous-agents.md
└── slides/
    └── index.html             # 可直接瀏覽之互動式教學 HTML 簡報（10 頁）
```

## 如何預覽與部署至 GitHub Pages
1. **本地預覽**：直接雙擊開啟 `index.html` 或 `slides/index.html`，可使用鍵盤 `←` / `→` 或點擊畫面下方按鈕切換投影片。
2. **GitHub Pages 部署**：
   - 將本資料夾推送至公開 GitHub Repository（例如 `llm-wiki-ai-agents`）。
   - 前往 `Settings -> Pages -> Build and deployment`，選擇 `Deploy from a branch` -> `main` / `/ (root)`。
   - 即可透過 `https://<你的帳號>.github.io/llm-wiki-ai-agents/` 線上瀏覽教學簡報。
