# 05. 工作流（Workflows）vs. 自主代理人（Autonomous Agents）

## 一句話白話定義
**Workflow** 像是「照著標準作業程序（SOP）走的自動化流水線」，而 **Autonomous Agent** 則是「遇到突發狀況能自己臨機應變、決定路線的專案經理」。

## 核心直覺與運作機制
- Anthropic 在《Building Effective Agents》中明確劃分了兩種系統設計光譜 `[[src-04]]`：
  1. **Workflows（預設路徑工作流）**：由工程師事先寫好程式碼流程，LLM 只在特定節點負責分類、摘要或審核。常見五大模式包含：**Prompt Chaining（提示鏈）**、**Routing（路由分流）**、**Parallelization（平行處理）**、**Orchestrator-Workers（協調者派工）** 與 **Evaluator-Optimizer（評估優化迴圈）** `[[src-04]]`。
  2. **Autonomous Agents（自主代理人）**：不寫死執行步驟，而是給定目標與工具箱，讓 LLM 根據每次環境回饋動態決定下一步（直到滿足停止條件或達到最大步數）`[[src-04]]`。

## 解決了什麼痛點？（與前代模型對比）
- **痛點（過度工程與失控風險）**：許多開發者一窩蜂想做「全自動 Agent」，結果導致 Token 成本暴增、延遲過高，甚至在錯誤迴圈裡無限燒錢 `[[src-04]]`。
- **工程選型黃金法則**：
  - 當任務步驟明確、追求高穩定與低成本時 $\rightarrow$ 優先選用 **Workflows**（特別是「生成 $\rightarrow$ 檢查 Gate $\rightarrow$ 修正」的 Evaluator-Optimizer 迴圈）`[[src-04]]`。
  - 只有當任務路徑無法事先窮舉、需要高度彈性探索時 $\rightarrow$ 才啟用 **Autonomous Agent**，並務必設置沙盒隔離與最大步數限制 `[[src-04]]`。

## 延伸閱讀與 Wiki 關聯
- 回顧整體架構：[[01-what-is-an-ai-agent]] $\rightarrow$ [[02-planning-and-react]] $\rightarrow$ [[04-tool-use-and-actions]]
