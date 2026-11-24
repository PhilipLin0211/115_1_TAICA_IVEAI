# Source 01: LLM Powered Autonomous Agents
- **作者**：Lilian Weng（前 OpenAI 安全系統負責人）
- **來源網址**：https://lilianweng.github.io/posts/2023-06-23-agent/
- **發布年份**：2023
- **核心摘要**：
  1. 提出業界最經典的 AI Agent 系統架構公式：**`Agent = LLM（大腦） + Planning（規劃） + Memory（記憶） + Tool Use（工具使用）`**。
  2. **Planning（規劃）**：包含「子目標拆解（Subgoal Decomposition，如 Chain of Thought / Tree of Thoughts）」與「自我反思（Self-Reflection，如 Reflexion 機制，從失敗經驗修正下一步行動）」。
  3. **Memory（記憶）**：將人類記憶映射至 AI 系統——短期記憶（Short-term Memory）對應模型當下的 Context Window（上下文視窗）；長期記憶（Long-term Memory）則透過外部向量資料庫（Vector DB）與最大內積搜尋（MIPS）實現無限容量檢索。
  4. **Tool Use（工具使用）**：指出純文字模型受限於預訓練截止時間與數學計算弱點，必須學會呼叫外部 API（如日曆、計算機、網路搜尋、程式碼執行器）來突破能力邊界。
