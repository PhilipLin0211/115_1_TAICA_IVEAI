# 《山岳馱獸包包 PackBeast Pro》

> **國立臺灣科技大學 (NTUST) 人工智慧所**  
> **課程名稱**：智慧虛擬實境與人工智慧 (115_1_TAICA_IVEAI)  
> **作業名稱**：用 Vibe Coding 做出一個互動網頁 (作業一)  
> **學號**：M11552010  
> **姓名**：林宸平  
> **專案名稱**：山岳馱獸包包 (PackBeast Pro) —— 登山輕量化負重與打包檢核 Web App

[![Live Demo](https://img.shields.io/badge/作業一線上體驗-GitHub%20Pages-success?style=for-the-badge&logo=github)](https://philiplin0211.github.io/115_1_TAICA_IVEAI/%E7%94%A8%20Vibe%20Coding%20%E5%81%9A%E5%87%BA%E4%B8%80%E5%80%8B%E4%BA%92%E5%8B%95%E7%B6%B2%E9%A0%81/)
[![Course Portal](https://img.shields.io/badge/課程作業總覽首頁-Portal-purple?style=for-the-badge&logo=githubpages)](https://philiplin0211.github.io/115_1_TAICA_IVEAI/)
[![GitHub Repo](https://img.shields.io/badge/原始碼-GitHub%20Repo-blue?style=for-the-badge&logo=github)](https://github.com/PhilipLin0211/115_1_TAICA_IVEAI)
[![Open In Colab](https://img.shields.io/badge/雲端執行-Google%20Colab-orange?style=for-the-badge&logo=googlecolab)](https://colab.research.google.com/github/PhilipLin0211/115_1_TAICA_IVEAI/blob/main/%E7%94%A8%20Vibe%20Coding%20%E5%81%9A%E5%87%BA%E4%B8%80%E5%80%8B%E4%BA%92%E5%8B%95%E7%B6%B2%E9%A0%81/run_on_colab.ipynb)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 快速核心連結 (Live Links)

* 🌐 **作業一 GitHub Pages 線上直接操作網址（核心評分項目）**：  
  👉 **[https://philiplin0211.github.io/115_1_TAICA_IVEAI/用%20Vibe%20Coding%20做出一個互動網頁/](https://philiplin0211.github.io/115_1_TAICA_IVEAI/%E7%94%A8%20Vibe%20Coding%20%E5%81%9A%E5%87%BA%E4%B8%80%E5%80%8B%E4%BA%92%E5%8B%95%E7%B6%B2%E9%A0%81/)**
* 🏠 **學期作業導航總目錄首頁**：  
  👉 **[https://philiplin0211.github.io/115_1_TAICA_IVEAI/](https://philiplin0211.github.io/115_1_TAICA_IVEAI/)**
* 🏗️ **系統架構圖與 Mermaid 流程圖說明書**：  
  👉 **[ARCHITECTURE.md](./ARCHITECTURE.md)**
* 📓 **Colab 一鍵雲端運行 Notebook**：  
  👉 **[run_on_colab.ipynb](./run_on_colab.ipynb)**
* 💻 **GitHub 原始碼儲存庫（Repository）**：  
  👉 **[https://github.com/PhilipLin0211/115_1_TAICA_IVEAI](https://github.com/PhilipLin0211/115_1_TAICA_IVEAI)**

---

## 🏔️ 一、專案簡介與核心理念

**《山岳馱獸包包 PackBeast Pro》** 是一套專為台灣百岳、中級山與越野跑山友量身打造的全方位行前裝備與體能管理 Web App。

在登山行前準備中，山友常面臨兩難痛點：
1. **過度打包（Over-packing）**：因擔憂失溫或物資不足攜帶過多冗餘物品，重裝壓垮雙膝與體力。
2. **盲目偷輕（Stupid Light）**：追求克數數字卻漏帶關鍵保命裝備（如頭燈、防水風雨衣褲），造成失溫山難風險。
3. **裝備管理混亂**：散落在不同行程、不同衣櫃的裝備無法統一追蹤重量、服役年限與磨損狀態。

本專案融合**精準公克數負重檢核**、**個人裝備履歷庫**、**130+ 款裝備規格智慧搜尋庫**、**動態馱獸小精靈情緒反饋**與**保命裝備防呆機制**，協助登山者在極致輕量化與生命安全間取得完美平衡。

---

## 🌟 二、完整網頁規格書與功能說明

### 🎒 模組一：五大系統裝備檢核與動態負重儀表板 (Pack Check)
1. **登山者個人參數與安全線推算**：
   * 支援體重數字輸入與拉桿即時微調（預設 65 kg）。
   * 🟢 **舒適安全區**（$\le 15\%$ 體重）：羽量輕裝，步履輕盈。
   * 🟡 **警戒臨界區**（$15\% \sim 20\%$ 體重）：需特別注意體能配速與關節負擔。
   * 🔴 **超重危險區**（$> 20\%$ 體重）：負重過載，極易引發膝部損傷與體能衰竭。
2. **四大行程型態推薦預設（Trip Preset）**：
   * ⚡ **單日單攻**：輕量單攻背包、水袋、避難毯、能量膠，追求極速安全。
   * 🏕️ **兩天一夜山屋**：含保暖中層、輕量睡袋、爐頭套鍋與高山瓦斯。
   * 🎒 **多日重裝露營**：含雙人自立帳、充氣睡墊、雙頭燈安全備份與三日乾燥糧。
   * 🏃 **越野跑 / 跑山**：水袋背心、雙軟水壺、賽事強制急救求生毯與高音哨。
3. **雙重重量指標與多層色彩進度條**：
   * 🎒 **基礎重量（Base Weight, BW）**：排除水與消耗性糧食後的純裝備重量。
   * ⚖️ **行進總重（Total Pack Weight, TPW）**：含行動水、瓦斯與食物的起登總負重。
   * 五大系統（睡眠收納、保暖防護、炊事水糧、安全導航、個人配件）色彩佔比長條圖。
4. **呆萌馱獸小精靈動態回饋（Packy Mascot）**：
   * 依據負重體重比即時變換 SVG 向量馱獸表情、動作與專屬對話：
     * $< 12\%$ 體重：羽量神獸，微風漂浮，心情極佳。
     * $12\% \sim 18\%$ 體重：穩健馱獸，踏實前進。
     * $> 20\%$ 體重：膝蓋火葬場，滿頭大汗劇烈震動求饒。
5. **高山保命安全防呆警示（Safety Guardian）**：
   * 自動即時掃描清單是否遺漏「防水風雨衣」或「照明頭燈」。若未帶齊，底部彈出警示條並提供 `⚡ 立即補上一鍵勾選`。
6. **五大系統清單即時互動**：
   * 支援個別項目勾選/取消勾選、克數即時聯動。
   * 支援自備裝備（已入庫）與推薦裝備（未在庫需準備）清晰狀態標籤。
   * 支援快速自訂新增裝備（名稱、重量、類別、消耗品勾選）。

---

### 🗄️ 模組二：個人裝備資產庫管理 (Gear Locker)
1. **完整裝備履歷記錄**：
   * 品牌（Brand）、品名（Model）、分類、精確重量（g）。
   * 購置日期與服役年資自動計算（如：`服役 1 年 4 個月`），提供新品/黃金戰力/超齡檢修燈號。
   * 消耗品與保命裝備專屬標記。
2. **裝備庫與打包清單高度聯動**：
   * 支援「一鍵帶入打包」與「移出打包」。
   * 支援打包頁面「從裝備庫挑選」批次勾選載入。
   * 支援本機 JSON 檔案備份匯出與匯入，換裝置資料不丟失。

---

### 🔍 模組三：130+ 裝備規格智慧搜尋與推薦 (Smart Spec Database)
1. **內建規格資料庫**：
   * 收錄 130+ 款常見經典登山裝備（Arc'teryx, Montbell, Osprey, Gregory, Soto, MSR, Sea to Summit, Black Diamond, Petzl）、越野跑裝備（Salomon, Ultimate Direction）與迪卡儂（Forclaz / Quechua）熱門款式。
2. **即時自動補全（Auto-Complete）**：
   * 輸入關鍵字即時下拉推薦相符品牌與官方重量，一鍵帶入。
3. **規格自動上網查詢助手**：
   * 忘記重量時點擊助手，自動模糊比對或一鍵跳轉 Google 官方規格與 OutdoorGearLab 評測。

---

## 🤖 三、AI 協同開發（Vibe Coding）過程與提示詞紀錄

本專案全程採用 **人機協同 Vibe Coding** 模式開發，由人類擔任「產品架構師與高山領域專家（Product Owner & Domain Expert）」，AI 擔任「技術工程師（AI Pair Programmer）」，歷經多輪迭代演進：

### 1. 核心起始 Prompt（建立應用雛型）
```text
我想用純前端單一靜態檔案（Vanilla HTML/CSS/JS）打造一款名為「山岳馱獸包包 PackBeast」的登山輕量化負重與打包檢核 Web App。
需求包含：
1. 現代深色/溫暖大地山系質感 UI，支援體重滑桿輸入（預設 65kg）。
2. 提供基礎重量（BW）與行進總重（TPW）即時計算，計算負重比（<15% 安全、15-20% 警戒、>20% 超重）。
3. 五大系統檢核清單（睡眠收納、保暖防護、炊事水糧、安全導航、個人配件），可即時勾選與刪增。
4. 呆萌馱獸 Mascot 動態 SVG 表情回饋（根據負重比變化表情對話）。
5. 保命安全防呆警示：若未勾選頭燈或雨衣，彈出安全防護警示。
6. 單日單攻、兩天一夜山屋、多日重裝露營等熱門行程推薦。
```

### 2. 迭代優化歷程（Bug 修正與進階功能擴充）

| 迭代階段 | 人類提出的需求 / 發現的 Bug | AI 實作解決方案與技術細節 |
| :--- | :--- | :--- |
| **Iteration 1** | 表情符號（Emoji）在各裝置渲染不一致，希望升級為現代化向量圖示。 | 引入 Flaticon Uicons 向量圖示庫，全面替換系統中所有 Emoji，統一大地色系視覺語言。 |
| **Iteration 2** | 行程推薦裝備應能自動比對使用者的「個人裝備庫」，已有者自動使用使用者裝備，缺少的再以推薦品項提醒。 | 設計 `state.gearLocker` 與行程範本的自動比對邏輯，已在庫品項自動標記為自備並勾選帶入。 |
| **Iteration 3** | 首頁技術性標語（如「純前端單一靜態架構」）過於工程導向，影響使用者體驗。 | 精簡標頭文案，聚焦於登山核心價值：「登山輕量化負重 • 個人裝備資產庫 • 規格智慧搜尋」。 |
| **Iteration 4** | 裝備標籤過於雜亂，保命與消耗品標籤容易造成視覺疲勞。 | 重構標籤系統，將標籤改為各系統專屬子分類（如「防水風雨衣」、「照明頭燈」、「攻頂爐具」），大幅提升辨識度。 |
| **Iteration 5** | 官方推薦裝備預設被自動勾選，且未勾選時會被劃線變淺，使用者加入自備裝備後提示未消失。 | 1. 推薦裝備保留 checklist 功能，預設調整為未勾選。<br>2. 改善未勾選視覺效果，避免文字劃線。<br>3. 當使用者加入自備裝備時，自動替換並移除原本的推薦款。 |
| **Iteration 6** | **重大 Bug**：行程推薦在「多日重裝露營」時，安全系統出現了兩個一模一樣的重複頭燈（Petzl Actik Core）。 | 1. **建立 1-to-1 裝備分配機制**：單一在庫裝備僅能被配對一次，不可重複分配。<br>2. **研發 Match Scoring 評分演算法**：完全相符（100分）、品名相符（90分）、關鍵字吻合（80分）、同子分類（50分），確保主力頭燈精確配對，備用頭燈保持推薦提醒。<br>3. **全域去重防護**：全域過濾重複 ID 與重複型號，徹底解決重複顯示問題。 |

---

## 🛠️ 四、技術架構特點

* **純前端單一檔案架構 (Zero-Build Single File)**：全應用整合於單一 index.html，無需 Webpack/Vite 打包，無需 Node.js 環境。
* **原生 Web Audio API 音效合成引擎**：不依賴任何外部音效 MP3 檔案，以瀏覽器原生振盪器（Oscillator）即時合成輕巧清脆的點擊與成功回饋音效。
* **隱私優先本地持久化**：所有個人裝備庫與負重設定皆儲存於瀏覽器 `localStorage`，完全離線可用，不上傳任何個人資訊。
* **GitHub Pages Ready**：可直接推送到 GitHub 靜態發布。

---

## 📄 本次作業檔案結構

```text
用 Vibe Coding 做出一個互動網頁/
├── index.html            # 作業一核心網頁（完整單一靜態 SPA 應用）
├── README.md             # 作業一規格說明書、Vibe Coding 歷程與提示詞紀錄
├── ARCHITECTURE.md       # 系統架構圖、Mermaid 流程圖與資料流規格
└── run_on_colab.ipynb    # Google Colab 一鍵啟動與雲端執行腳本
```

---

> 國立臺灣科技大學 人工智慧所 M11552010 林宸平  
> 感謝授課教師與助教的指導！
