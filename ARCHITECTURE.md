# 《山岳馱獸包包 PackBeast Pro》系統架構與運作流程圖說明書

本文件詳細闡述《山岳馱獸包包 PackBeast Pro》的軟體系統架構、元件分層、模組交互關係以及核心功能的運作流程圖（採用 Mermaid 語法繪製）。

---

## 🏗️ 一、系統總體分層架構圖 (System Architecture)

《山岳馱獸包包》採用**純前端單一靜態架構（Single Static SPA）**，無需任何後端伺服器或建置工具即可在瀏覽器獨立運作，所有運算與資料儲存皆在使用者客戶端完成，具備離線可用、極速響應與隱私安全特性。

```mermaid
graph TB
    subgraph Client_UI ["前端視圖展示層 (Presentation Tier)"]
        Nav["導航切換列 (Navigation Tabs)"]
        Header["頂部工具列 (音效開關 / 複製裝備摘要 / 範本重設)"]
        
        subgraph Tab1 ["Tab 1: 打包負重檢核 (Pack Check)"]
            T1_Input["體重參數調整 (數字輸入 / 滑桿連動)"]
            T1_Presets["4大行程推薦預設 (單攻/山屋/露營/越野跑)"]
            T1_Dash["動態負重儀表板 (Base Weight / TPW / 負重比)"]
            T1_Mascot["馱獸動態狀態反饋卡 (羽量神獸/穩健馱獸/膝蓋火葬場)"]
            T1_Guardian["守護小精靈 (頭燈/雨衣保命裝備雙重掃描)"]
            T1_Checklist["5大分類裝備檢核清單 (即時勾選/編輯/自訂新增)"]
        end

        subgraph Tab2 ["Tab 2: 個人裝備資產庫 (Gear Locker)"]
            T2_Stats["裝備庫資產統計 (總重 / 總件數 / 平均服役年資)"]
            T2_Toolbar["即時搜尋過濾列 / 規格庫查詢 / 登記新裝備"]
            T2_Grid["個人裝備卡片 (服役年資燈號 / 一鍵加入打包)"]
            T2_Backup["JSON 備份匯出與本機檔案還原"]
        end

        subgraph Global_Modals ["全域輔助彈窗與互動反饋"]
            M_AddGear["登記/編輯裝備 Modal (支援即時自動補全)"]
            M_SpecSearch["智慧規格搜尋助手 Modal (內建規格庫 + 外部評測捷徑)"]
            M_Toast["Toast 即時通知反饋系統"]
            M_Audio["Web Audio API 合成音效引擎 (無外部音檔依賴)"]
        end
    end

    subgraph Logic_Tier ["核心業務邏輯與演算引擎層 (Business Logic & Engine Tier)"]
        E_Weight["負重計算引擎 (Base Weight & TPW Calculator)"]
        E_Safety["安全防護檢測引擎 (Safety Guardian Scanner)"]
        E_Spec["規格模糊比對與自動補全引擎 (Spec Matching Engine)"]
        E_Sound["Web Audio 振盪器音效引擎 (Oscillator Synthesizer)"]
    end

    subgraph Data_Tier ["資料儲存與持久化層 (Data & Persistence Tier)"]
        S_State["全域響應式狀態 (Global App State: gearList, gearLocker, bodyWeight)"]
        DB_Specs["內建 130+ 款主流裝備規格資料庫 (經典登山/越野跑/迪卡儂)"]
        Local_Storage["瀏覽器 LocalStorage (Key: packbeast_pro_state_v2)"]
        JSON_File["本機 JSON 備份檔案"]
    end

    %% 連接關係
    Header --> S_State
    Nav --> Tab1 & Tab2
    Tab1 --> E_Weight & E_Safety
    Tab2 --> E_Spec
    Global_Modals --> E_Sound

    E_Weight & E_Safety & E_Spec <--> S_State
    E_Spec <--> DB_Specs
    S_State <--> Local_Storage
    T2_Backup <--> JSON_File
```

---

## 🔄 二、核心功能運作流程圖 (Operational Workflows)

### 1. 打包負重檢核與動態儀表板運作流程 (Pack Check & Dynamic Dashboard)

此流程涵蓋登山者設定體重、選取行程型態預設範本、即時計算基礎重量（Base Weight）與起登總重（Total Packed Weight），並連動守護小精靈進行保命裝備即時掃描。

```mermaid
sequenceDiagram
    autonumber
    actor User as 登山者 / 使用者
    participant UI as 前端互動介面
    participant State as 全域狀態 (State)
    participant Engine as 負重與安全演算引擎
    participant Audio as Web Audio 音效
    participant Storage as LocalStorage

    User->>UI: 調整體重數值 或 點選行程預設 (單攻/山屋/露營/越野跑)
    UI->>State: 更新 bodyWeight / currentPreset 並載入裝備範本
    UI->>Engine: 觸發 recalculate()
    
    activate Engine
    Engine->>Engine: 計算 Base Weight (未勾選消耗品之總克數)
    Engine->>Engine: 計算 Total Packed Weight (已勾選所有裝備之總克數)
    Engine->>Engine: 計算 負重體重比 = (起登總重 / 體重) * 100%
    Engine->>Engine: 評估負重門檻 (舒適綠 ≤15% | 警戒黃 15-20% | 危險紅 >20%)
    Engine->>Engine: 掃描核心保命裝備 (頭燈 / 防水雨衣雨褲)
    deactivate Engine

    Engine-->>UI: 回傳 BW, TPW, 負重比率, 馱獸吉祥物狀態, 安全警告
    UI->>UI: 更新雙指標進度條、狀態勳章與吉祥物動畫 (羽量/穩健/膝蓋火葬場)
    
    alt 缺少核心保命裝備
        UI->>UI: 守護小精靈高亮紅色警戒橫幅
    else 裝備齊全
        UI->>UI: 顯示綠色安全通過認證標章
    end

    opt 使用者勾選 / 新增 / 刪除裝備
        User->>UI: 點選裝備 Checkbox 或 刪除裝備
        UI->>Audio: 播放 Pop / Click 音效
        UI->>State: 增刪裝備陣列元素
        UI->>Engine: 重新計算負重指標
        UI->>Storage: saveToStorage() 保存最新狀態至 LocalStorage
    end
```

---

### 2. 裝備資產庫搜尋、規格庫智慧檢索與一鍵入庫流程 (Gear Locker & Spec Search)

本模組支援**離線毫秒級雙向檢索**與**個人裝備壽命管理**，當使用者在裝備庫搜尋時，系統會同時檢索個人既有裝備與 130+ 款官方規格庫。

```mermaid
flowchart TD
    Start([使用者在裝備庫搜尋框輸入關鍵字]) --> CheckInput{輸入文字是否為空?}
    
    CheckInput -- 是 --> ShowAllLocker[展示個人裝備庫完整清單與資產統計]
    
    CheckInput -- 否 --> QueryLocal[1. 檢索個人裝備庫 (Brand / Model / Notes / Category)]
    QueryLocal --> QueryDB[2. 同步檢索內建 130+ 官方規格庫 (登山/越野跑/迪卡儂)]
    
    QueryLocal & QueryDB --> FilterDuplicates{排除個人裝備庫已擁有的型號}
    
    FilterDuplicates --> RenderUI[動態渲染搜尋結果面板]
    
    RenderUI --> HasLocalMatch{個人庫有相符?}
    HasLocalMatch -- 有 --> DisplayLocalCards[展示個人裝備卡片 (含服役年資狀態燈號)]
    HasLocalMatch -- 無 --> DisplayEmptyPrompt[顯示個人庫未收錄提示]
    
    RenderUI --> HasDBMatch{官方規格庫有相符?}
    HasDBMatch -- 有 --> DisplayDBRecommendations[下方渲染 🌟 官方資料庫推薦區塊<br>標示品牌、官方淨重與分類]
    DisplayDBRecommendations --> ClickAdd[使用者點擊 ➕ 登記存入裝備庫]
    ClickAdd --> AutoFill[自動提取規格參數 (品牌/品名/克數/分類/啟用日期)]
    AutoFill --> SaveLocker[存入個人裝備庫 State.gearLocker]
    SaveLocker --> PlaySound[播放 Success 成功提示音效]
    PlaySound --> RefreshView[即時重新渲染裝備庫並持久化儲存]
    
    HasDBMatch -- 無 --> ShowExternalLink[顯示 🌐 Google 規格 / OutdoorGearLab 線上查詢按鈕]
    ShowExternalLink --> UserOnlineSearch[點擊開啟精準搜尋新分頁查閱克重]
```

---

### 3. 資料持久化、匯出備份與無痛轉移機制 (State Persistence & Backup)

確保使用者在離線、重新整理網頁或更換不同裝置時，個人裝備資產與打包狀態安全無虞。

```mermaid
flowchart TD
    subgraph Browser_Runtime ["瀏覽器運行時 (Runtime)"]
        AppStart([網頁載入 DOMContentLoaded]) --> CheckStorage{LocalStorage 是否有存檔?}
        CheckStorage -- 存在有效資料 --> ParseJSON[解析 packbeast_pro_state_v2 JSON]
        ParseJSON --> HydrateState[還原裝備清單、個人裝備資產庫與體重設定]
        CheckStorage -- 首次訪問 / 空白 --> InitDefault[載入預設 65kg、兩天一夜範本]
        
        HydrateState & InitDefault --> RenderApp[全面渲染 Tab 1 與 Tab 2 畫面]
        
        UserAction[使用者進行任何互動<br>增刪裝備 / 勾選 / 登記新裝備 / 調整體重] --> UpdateState[更新記憶體內之 state 物件]
        UpdateState --> SaveStorage[(寫入 window.localStorage)]
    end

    subgraph Backup_Transfer ["備份匯出與無痛轉移"]
        ExportBtn[點擊 💾 匯出 JSON 備份] --> GenBlob[生成 DataURI / Blob JSON 資料]
        GenBlob --> DownloadFile[觸發瀏覽器下載 packbeast_gear_locker_日期.json]
        
        ImportBtn[點擊 📂 匯入 JSON 備份] --> FilePicker[喚起本機檔案選取器]
        FilePicker --> ReadFile[FileReader 異步讀取檔案內容]
        ReadFile --> ValidateJSON{校驗 JSON 結構是否相符?}
        ValidateJSON -- 格式正確 --> MergeLocker[合併或覆蓋至個人裝備庫]
        MergeLocker --> SaveStorage
        MergeLocker --> ShowSuccess[彈出 Toast 提示「匯入成功」]
        ValidateJSON -- 格式損毀 --> ShowError[提示「JSON 格式不符」並拒絕寫入]
    end
```

---

## 📊 三、核心資料結構規範 (Data Schema Reference)

### 裝備項目物件（Gear Item Schema）
```typescript
interface GearItem {
  id: string;             // 唯一識別代碼 (如 "dh_1", "locker_1697...")
  brand: string;          // 品牌名稱 (如 "Montbell", "Arc'teryx", "Forclaz")
  name: string;           // 裝備品名與型號 (如 "Versalite Jacket 超輕風雨衣")
  cat: 'sleep' | 'warm' | 'cook' | 'safe' | 'gear'; // 裝備所屬五大系統
  grams: number;          // 裝備實秤重量（公克 g）
  checked?: boolean;      // 打包檢核勾選狀態 (true = 已裝入背包)
  isConsumable: boolean;  // 是否為消耗品 (水、糧食、瓦斯，不計入 Base Weight)
  vital: boolean;         // 是否為保命裝備 (頭燈、雨衣雨褲)
  vitalType?: 'headlamp' | 'rain' | null; // 保命裝備特定類型
  startDate?: string;     // 啟用日期 (YYYY-MM-DD，用於裝備庫計算服役年資)
  notes?: string;         // 個人使用心得或保養備註
}
```

---

## 💡 四、架構特點與工程優勢總結

1. **聚焦核心體驗**：全面專注於「輕量化負重控制」與「個人裝備生命週期管理」兩大核心價值，介面直覺乾淨，無冗餘干擾。
2. **零外部框架依賴（Zero Dependencies）**：純原生 HTML5、CSS3 與現代 JavaScript（ES6+），單一靜態檔案架構，可直接部署於 GitHub Pages。
3. **離線優先設計（Offline-First & Local-First）**：內建 130+ 款主流裝備規格資料庫，在無行動網路的山區仍可完整運行所有檢核、搜尋與裝備管理功能。
4. **流暢動態回饋（60 FPS Animation）**：CSS 變數系統、彈性感應格線與硬體加速過渡動畫，在手機、平板與桌機上均能享有極致體驗。
