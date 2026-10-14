# 《山岳馱獸包包 PackBeast Pro》系統架構與運作流程圖說明書

本文件詳細闡述《山岳馱獸包包 PackBeast Pro》的軟體系統架構、元件分層、模組交互關係以及四大核心功能的運作流程圖（採用 Mermaid 語法繪製）。

---

## 🏗️ 一、系統總體分層架構圖 (System Architecture)

《山岳馱獸包包》採用**純前端單一靜態架構（Single Static SPA）**，無需任何伺服器端或構建工具即可在瀏覽器獨立運作，所有資料與運算皆在客戶端完成，兼具隱私優先、離線可用與零延遲反應特性。

```mermaid
graph TB
    subgraph Client_UI ["前端視圖展示層 (Presentation Tier)"]
        Nav["導航切換列 (Navigation Tabs)"]
        Header["頂部工具列 (音效開關 / 複製摘要 / 範本重設)"]
        
        subgraph Tab1 ["Tab 1: 打包負重檢核"]
            T1_Input["體重調整 (數字 / 滑桿)"]
            T1_Presets["4大行程推薦預設 (單攻/山屋/露營/越野跑)"]
            T1_Dash["動態負重儀表板 (BW / TPW / 負重比)"]
            T1_Mascot["馱獸動態狀態反饋卡"]
            T1_Guardian["守護小精靈 (保命裝備雙重掃描)"]
            T1_Checklist["5大分類裝備檢核清單 (勾選/編輯/刪除)"]
        end

        subgraph Tab2 ["Tab 2: 個人裝備資產庫"]
            T2_Stats["裝備庫資產統計 (總重 / 總件數 / 平均服役年資)"]
            T2_Toolbar["搜尋過濾列 / 規格庫查詢 / 登記新裝備"]
            T2_Grid["個人裝備卡片 (年資狀態燈 / 一鍵加入打包)"]
            T2_Backup["JSON 備份匯出與檔案還原"]
        end

        subgraph Tab3 ["Tab 3: 路線規格與 EPH 體能計算"]
            T3_RouteChips["台灣熱門路線庫晶片 (玉山/雪山/奇萊等 9 條)"]
            T3_Inputs["自訂路線參數 (里程 / 爬升 / 下降)"]
            T3_Pace["個人配速係數滑桿 (0.6x ~ 1.5x)"]
            T3_EPH["EPH 體能等效步程難度 Banner"]
            T3_Penalty["馱獸包包負重減速加權修正卡"]
            T3_ETA["完登預估時間 / 起登 ETA / 日落警戒"]
        end

        subgraph Global_Modals ["全域輔助彈窗與互動回饋"]
            M_AddGear["新增/編輯裝備 Modal"]
            M_SpecSearch["智慧規格搜尋助手 Modal"]
            M_Toast["Toast 即時通知反饋"]
            M_Audio["Web Audio API 合成音效引擎"]
        end
    end

    subgraph Logic_Tier ["核心業務邏輯與演算引擎層 (Business Logic & Engine Tier)"]
        E_Weight["負重計算引擎 (Base Weight & TPW Calculator)"]
        E_Safety["安全防護檢測引擎 (Safety Guardian Scanner)"]
        E_Spec["規格模糊比對與自動補全引擎 (Spec Matching Engine)"]
        E_Route["EPH 難度與負重減速演算引擎 (Pace & Penalty Engine)"]
        E_Sound["Web Audio 振盪器音效引擎 (Oscillator Synthesizer)"]
    end

    subgraph Data_Tier ["資料儲存與持久化層 (Data & Persistence Tier)"]
        S_State["全域響應式狀態 (Global App State)"]
        DB_Specs["內建 130+ 款主流裝備規格資料庫 (登山/越野跑/迪卡儂)"]
        DB_Routes["內建台灣經典百岳與中級山路線庫"]
        Local_Storage["瀏覽器 LocalStorage (Key: packbeast_pro_state_v2)"]
        JSON_File["本機 JSON 備份檔案"]
    end

    %% 連接關係
    Header --> S_State
    Nav --> Tab1 & Tab2 & Tab3
    Tab1 --> E_Weight & E_Safety
    Tab2 --> E_Spec
    Tab3 --> E_Route
    Global_Modals --> E_Sound

    E_Weight & E_Safety & E_Spec & E_Route <--> S_State
    E_Spec <--> DB_Specs
    E_Route <--> DB_Routes
    S_State <--> Local_Storage
    T2_Backup <--> JSON_File
```

---

## 🔄 二、核心功能運作流程圖 (Operational Workflows)

### 1. 打包負重檢核與動態儀表板運作流程 (Pack Check & Dynamic Dashboard)

此流程涵蓋登山者輸入體重、選擇行程型態範本、即時計算基礎重量（BW）與起登總重（TPW），並連動守護小精靈進行保命裝備掃描。

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
        UI->>Storage: saveToStorage() 保存最新狀態
    end
```

---

### 2. 裝備資產庫搜尋、規格庫智慧檢索與一鍵入庫流程 (Gear Locker & Spec Search)

本模組支援**離線毫秒級檢索**與**個人裝備壽命管理**，當使用者在裝備庫搜尋時，系統會同時比對個人既有裝備與 130+ 款官方規格庫。

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
    ClickAdd --> AutoFill[自動提取規格參數 (品牌/品名/克數/分類/當前啟用日期)]
    AutoFill --> SaveLocker[存入個人裝備庫 State.gearLocker]
    SaveLocker --> PlaySound[播放 Success 成功提示音效]
    PlaySound --> RefreshView[即時重新渲染裝備庫並持久化儲存]
    
    HasDBMatch -- 無 --> ShowExternalLink[顯示 🌐 Google 規格 / OutdoorGearLab 線上查詢按鈕]
    ShowExternalLink --> UserOnlineSearch[點擊開啟精準搜尋新分頁查閱克重]
```

---

### 3. 登山路線規格、EPH 體能指標與負重減速加權演算流程 (Route, EPH & Pack Penalty)

本功能整合路線地形指標與**打包總重（TPW）**，透過動態聯動演算法，真實模擬登山重裝對步速的減速影響。

```mermaid
flowchart LR
    subgraph Inputs ["輸入參數層"]
        R_Select["選取 9 條經典路線<br>或自訂里程/爬升/下降"]
        R_Pace["設定個人步速係數<br>(0.6x 神腿 ~ 1.5x 慢行)"]
        R_Start["設定預計起登時間<br>(預設 04:30)"]
        R_PackWeight["讀取 Tab 1 之起登總重 TPW<br>與個人體重負重佔比 %"]
    end

    subgraph Calculation ["核心演算邏輯"]
        Calc_EPH["計算 EPH 體能等效步程時<br>EPH = 里程 + (爬升/100) + (下降/300)"]
        Calc_Difficulty["評定體能難度等級<br>🟢 愜意郊山 (≤12)<br>🟡 中度百岳 (12-22)<br>🟠 高強度挑戰 (22-35)<br>🔴 極限縱走 (>35)"]
        
        Calc_Base["計算標準山徑步程時間 (Base Time)<br>自訂模式：(里程/3.8) + (爬升/400) + (下降/1200)"]
        Calc_Personal["計算個人無負重預估時間<br>Personal Hours = Base Time * Pace Ratio"]
        
        Calc_Penalty["馱獸包包獨創：背包負重減速加權<br>• 負重 ≤ 15%: 懲罰率 1.00x (無延遲)<br>• 負重 15~20%: 懲罰率 1.0 + (超額% * 0.018)<br>• 負重 > 20%: 懲罰率 1.10 + (超額% * 0.025)"]
        
        Calc_Final["計算負重修正後之最終完登時間<br>Final Hours = Personal Hours * 懲罰率"]
        Calc_ETA["推算抵達時間 (ETA) 與日落撤退警戒<br>起登時間 + 最終步程時間"]
    end

    subgraph Outputs ["即時視覺呈現與群組分享"]
        Out_Banner["EPH 難度勳章與數值卡"]
        Out_Time["完登預估時間 (小時 / 分鐘)"]
        Out_PenaltyCard["負重減速加權卡與膝蓋耗損提醒"]
        Out_ETA["ETA 抵達標籤 (若超過 17:30 觸發摸黑警戒)"]
        Out_Share["📋 一鍵複製配速計畫至 LINE 群組"]
    end

    Inputs --> Calculation
    Calc_EPH --> Calc_Difficulty
    Calc_Base & R_Pace --> Calc_Personal
    R_PackWeight --> Calc_Penalty
    Calc_Personal & Calc_Penalty --> Calc_Final
    Calc_Final & R_Start --> Calc_ETA
    
    Calculation --> Outputs
```

---

### 4. 資料持久化、匯出備份與無痛轉移機制 (State Persistence & Backup)

保證使用者在離線、重新整理網頁或更換裝置時，裝備與計算狀態絕不遺失。

```mermaid
flowchart TD
    subgraph Browser_Runtime ["瀏覽器運行時 (Runtime)"]
        AppStart([網頁載入 DOMContentLoaded]) --> CheckStorage{LocalStorage 是否有存檔?}
        CheckStorage -- 存在有效資料 --> ParseJSON[解析 packbeast_pro_state_v2 JSON]
        ParseJSON --> HydrateState[還原裝備清單、個人裝備櫃與配速設定]
        CheckStorage -- 首次訪問 / 空白 --> InitDefault[載入預設 65kg、兩天一夜範本]
        
        HydrateState & InitDefault --> RenderApp[全面渲染 Tab 1, Tab 2, Tab 3 畫面]
        
        UserAction[使用者進行任何互動<br>增刪裝備 / 勾選 / 修改路線 / 調整體重] --> UpdateState[更新記憶體內之 state 物件]
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

### 1. 裝備項目物件（Gear Item Schema）
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

### 2. 路線參數物件（Route Parameter Schema）
```typescript
interface RouteItem {
  id: string;             // 路線代碼 (如 "yushan_main", "custom")
  name: string;           // 路線名稱 (如 "玉山主峰線 (塔塔加往返)")
  distKm: number;         // 總單程或往返里程 (公里 km)
  ascentM: number;        // 累計爬升高度 (公尺 m)
  descentM: number;       // 累計下降高度 (公尺 m)
  standardHours: number;  // 路線標準地圖步程基準時間 (小時 hr)
  desc: string;           // 路線地形特徵與安全提示說明
}
```

---

## 💡 四、架構特點與工程優勢總結

1. **零外部框架依賴（Zero Dependencies）**：純原生 HTML5、CSS3 與現代 ES6+ JavaScript，整套系統打包於單一檔案，無 npm 套件龐大體積與供應鏈漏洞風險。
2. **高響應式與流暢體驗（60 FPS Animation）**：採用 CSS 變數系統、彈性格線（Flexbox/Grid）與硬體加速過渡效果，支援手機、平板至桌上型螢幕無縫適配。
3. **離線優先設計（Offline-First & Local-First）**：內建 130+ 款裝備與 9 條路線資料，在無行動網路的山區仍可完整運行所有檢核、搜尋與計算功能。
4. **模組化演算法解耦（Decoupled Calculation Engines）**：負重引擎、守護掃描器、規格檢索器與配速引擎各自獨立，便於未來擴充 GPS GPX 軌跡匯入或天氣預報 API 串接。
