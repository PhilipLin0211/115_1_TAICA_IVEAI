# 02. 任務規劃（Planning）與 ReAct 推理迴圈

## 一句話白話定義
**ReAct（Reasoning + Acting）** 就是教 AI 養成「先在心裡想清楚下一步（Thought）、再動手查資料或操作（Action）、看完結果再決定怎麼辦（Observation）」的嚴謹工作習慣。

## 核心直覺與運作機制
- **子目標拆解（Task Decomposition）**：面對「幫我規劃一趟東京五日遊並訂好機票」這類大目標，Agent 會透過思維鏈（Chain of Thought）把大任務切成「查航班 $\rightarrow$ 比價 $\rightarrow$ 排景點 $\rightarrow$ 檢查預算」等小步驟 `[[src-01]]`。
- **ReAct 交替迴圈**：在每一步中，模型先輸出一段人類看得懂的內心獨白（`Thought`），接著觸發外部動作（`Action`），並讀取環境回傳的真實數據（`Observation`），如此反覆迭代直到得出最終答案 `[[src-02]]`。
- **自我反思（Self-Reflection）**：當某一步執行失敗（例如查無航班或程式報錯）時，Agent 能檢視錯誤訊息並修正計畫，避免在死胡同裡無限鬼打牆 `[[src-01]]`。

## 解決了什麼痛點？（與前代模型對比）
- **純推理（Chain-of-Thought）的痛點**：模型雖然會一步步思考，但因為沒有連接外部世界，遇到不知道的事實就會開始「一本正經地胡說八道（Hallucination）」`[[src-02]]`。
- **純行動（Act-only）的痛點**：沒有先經過思考就盲目呼叫工具，容易在複雜多步驟任務中迷失方向 `[[src-02]]`。
- **ReAct 的突破**：讓「推理引導行動、行動帶回真實事實修正推理」，大幅降低事實幻覺並提高決策透明度 `[[src-02]]`。

## 延伸閱讀與 Wiki 關聯
- 前置概念：[[01-what-is-an-ai-agent]]
- 行動之後如何記住結果？請見 [[03-memory-architecture]]。
