# 作業二：建立一個自己的 AGENTS.md (HW 2)

> **課程**：115-1 生成式AI：文字與圖像生成的原理與實務 (TAICA_IVEAI)  
> **學生**：國立臺灣科技大學 人工智慧所 林宸平 (M11552010)  
> **線上體驗**：👉 [https://philiplin0211.github.io/115_1_TAICA_IVEAI/建立一個自己的%20%20AGENTS/](https://philiplin0211.github.io/115_1_TAICA_IVEAI/%E5%BB%BA%E7%AB%8B%E4%B8%80%E5%80%8B%E8%87%AA%E5%B7%B1%E7%9A%84%20%20AGENTS/)  
> **規範手冊**：👉 [根目錄 AGENTS.md](../AGENTS.md)

---

## 📌 作業核心目標

本作業旨在跳脫單純的「單頁快速編碼 (Vibe Coding)」，轉向**「規範驅動 (Spec-Driven)」**與**「自動化資料流 (Automated Manifest)」**的永續維護架構：

1. **建立專屬開發規範 (`AGENTS.md`)**：
   明確定義 AI 輔助開發的最高準則，包含設計系統標準、色彩變數、目錄架構、資料格式與擴充工作流。
2. **VS Code Dark+ 零透明度實色系統**：
   嚴格禁止使用 `rgba()`、`opacity < 1` 或 `backdrop-filter: blur()`，所有色彩採 100% 實色。
3. **資料驅動與自動化建置 (`scripts/build_manifest.py` + GitHub Actions)**：
   講義（`PPT/`）、筆記（`notes/`）與新作業資料夾無需手動改寫 HTML，只要推送檔案至 GitHub，CI/CD 會自動掃描產生 `data.json` 並更新入口網站。

---

## 📂 檔案目錄結構

```text
建立一個自己的  AGENTS/
├── index.html           # 作業二成果展示子頁面 (VS Code Dark+ 零透明度風格)
├── project.meta.json    # 作業中繼描述檔 (供 build_manifest.py 自動解析)
└── README.md            # 作業二詳細技術文件 (本文件)
```

---

## 🎨 設計系統規範 (VS Code Dark+ Solid)

| 變數名稱 | 實色色碼 (Hex) | 用途 |
| :--- | :--- | :--- |
| `--bg-editor` | `#1e1e1e` | 主內容區背景底色 |
| `--bg-sidebar` | `#252526` | 側邊欄與主要卡片背景 |
| `--bg-activity` | `#333333` | 活動列背景 |
| `--bg-tabs` | `#2d2d2d` | 頂部分頁列底色 |
| `--bg-statusbar` | `#007acc` | 底部狀態列底色 (VS Code 標誌藍) |
| `--border-solid` | `#3c3c3c` | 全站實色邊框 |
| `--text-bright` | `#ffffff` | 高亮標題文字 |
| `--text-main` | `#cccccc` | 內文標準文字 |
| `--text-muted` | `#858585` | 次要說明文字 |
| `--accent-blue` | `#569cd6` | 主要藍色連結與標題 |
| `--accent-teal` | `#4ec9b0` | 徽章與語意高亮色 |
| `--accent-orange` | `#ce9178` | 副標題與行內代碼色 |
| `--accent-yellow` | `#dcdcaa` | 流程圖與警告色 |

