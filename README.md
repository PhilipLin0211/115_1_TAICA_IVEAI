# 115-1 智慧虛擬實境與人工智慧 (TAICA_IVEAI) 課程作業集

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
| :--- | :--- | :--- | :--- | :---: |
| **作業一 (HW 1)** | **用 Vibe Coding 做出一個互動網頁** | **《山岳馱獸包包 PackBeast Pro》**<br>登山輕量化負重與打包檢核 Web App | 🌐 [線上即時操作 (Live Demo)](https://philiplin0211.github.io/115_1_TAICA_IVEAI/%E7%94%A8%20Vibe%20Coding%20%E5%81%9A%E5%87%BA%E4%B8%80%E5%80%8B%E4%BA%92%E5%8B%95%E7%B6%B2%E9%A0%81/)<br>📖 [作業規格與開發歷程](./用%20Vibe%20Coding%20做出一個互動網頁/README.md)<br>🏗️ [系統架構圖 (Architecture)](./用%20Vibe%20Coding%20做出一個互動網頁/ARCHITECTURE.md)<br>📓 [Colab 雲端執行](./用%20Vibe%20Coding%20做出一個互動網頁/run_on_colab.ipynb) | ✅ 已發布 |
| **作業二 (HW 2)** | *規劃準備中* | *Coming Soon* | *即將推出* | ⏳ 規劃中 |
| **作業三 (HW 3)** | *規劃準備中* | *Coming Soon* | *即將推出* | ⏳ 規劃中 |

---

## 🗂️ 儲存庫目錄結構 (Repository Structure)

為利於本學期多項作業的長期維護與收錄，本儲存庫採用**模組化作業子資料夾架構**，根目錄作為 GitHub Pages 課程作業入口，各次作業獨立收錄於各自的資料夾中：

```text
115_1_TAICA_IVEAI/
├── index.html                               # 課程作業線上導覽總頁 (GitHub Pages 入口)
├── README.md                                # 全學期作業目錄與儲存庫說明
├── PPT/                                     # 課程教材講義 (01 ~ 05 週投影片)
│   ├── 01如何不焦慮地學AI(學生點開顯示未發佈).pdf
│   ├── 02神經網路的概念.pdf
│   ├── 03AI為什麼每次都不一樣？.pdf
│   ├── 04LLM只是在猜下一個字？.pdf
│   └── 05AI怎麼記得前面說過什麼？.pdf
│
└── 用 Vibe Coding 做出一個互動網頁/            # 【作業一】專案完整目錄
    ├── index.html                           # 作業一 Web App 本體 (山岳馱獸包包 PackBeast Pro)
    ├── README.md                            # 作業一詳細規格書、提示詞紀錄與 Vibe Coding 歷程
    ├── ARCHITECTURE.md                      # 系統架構圖與 Mermaid 流程圖說明書
    └── run_on_colab.ipynb                   # 作業一專屬 Google Colab 一鍵啟動腳本
```

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

> 國立臺灣科技大學 人工智慧所 M11552010 林宸平  
> 感謝授課教師與助教的指導！
