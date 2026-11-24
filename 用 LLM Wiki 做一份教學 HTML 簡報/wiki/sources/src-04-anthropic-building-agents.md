# Source 04: Building Effective Agents
- **作者**：Erik Schluntz, Barry Zhang（Anthropic Engineering Team）
- **來源網址**：https://www.anthropic.com/engineering/building-effective-agents
- **發布年份**：2024
- **核心摘要**：
  1. 提出工程界最重要的架構區分：**Workflows（工作流）** 是透過預先寫好的程式碼路徑編排 LLM 與工具；**Agents（自主代理人）** 則是由 LLM 動態自主決定執行步驟與工具選擇。
  2. 建議「**能用簡單方案就不要過度設計（Keep it simple）**」：多數企業場景只需單一 LLM 搭配檢索與工具，或使用五種標準 Workflow 模式（Prompt Chaining 提示鏈、Routing 路由分流、Parallelization 平行處理、Orchestrator-Workers 協調者模式、Evaluator-Optimizer 評估優化迴圈）即可穩定解決。
  3. 強調 **ACI（Agent-Computer Interface，代理人電腦介面）** 設計的重要性：工具的說明文件、參數命名與防呆錯誤訊息，應像設計給人類工程師的 UI 一樣清晰，才能避免 Agent 傳錯參數。
