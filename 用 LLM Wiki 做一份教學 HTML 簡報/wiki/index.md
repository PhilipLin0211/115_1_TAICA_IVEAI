# AI Agents 技術文獻 LLM Wiki（總目錄）

本知識庫系統性收錄網路上關於 **LLM-powered AI Agents** 的經典研究與工程實務文獻，拆解 AI 如何從「只會聊天的對話機器人」進化為「能自主規劃、記憶、呼叫工具並完成任務的數位代理人」。

## 知識架構地圖（Agent Architecture Graph）
```text
                    ┌─── [02. Planning & ReAct 推理規劃]
                    │
[01. AI Agent 核心定義] ──┼─── [03. Memory 短期與長期記憶] ──▶ [05. Workflows vs. Agents 工程選型]
   (LLM 大腦中樞)    │
                    └─── [04. Tool Use 外部工具呼叫]
```

## 核心概念條目（Concepts）
1. [[01-what-is-an-ai-agent]] — 聊天機器人（Chatbot）與 AI Agent 的本質差異：`Agent = LLM + Planning + Memory + Tools`。
2. [[02-planning-and-react]] — 任務拆解與 ReAct（Thought $\rightarrow$ Action $\rightarrow$ Observation）邊想邊做的推理迴圈。
3. [[03-memory-architecture]] — 突破 Context Window 限制：感覺記憶、短期工作記憶與向量資料庫長期記憶。
4. [[04-tool-use-and-actions]] — 讓模型長出手腳：API 呼叫、搜尋引擎、程式碼直譯器與 Self-Supervised 工具學習。
5. [[05-workflows-vs-autonomous-agents]] — Anthropic 工程實務指南：何時該用固定流程（Workflows）？何時才需要自主 Agent？

## 已收錄網路文獻來源（Ingested Sources，共 5 篇）
- `src-01`: Weng, L. (2023). *LLM Powered Autonomous Agents*. Lil'Log Technical Blog. `https://lilianweng.github.io/posts/2023-06-23-agent/`
- `src-02`: Yao, S., et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models* (arXiv:2210.03629). `https://arxiv.org/abs/2210.03629`
- `src-03`: Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools* (arXiv:2302.04761). `https://arxiv.org/abs/2302.04761`
- `src-04`: Anthropic Engineering (2024). *Building Effective Agents*. Anthropic Research & Engineering Blog. `https://www.anthropic.com/engineering/building-effective-agents`
- `src-05`: Park, J. S., et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior* (arXiv:2304.03442). `https://arxiv.org/abs/2304.03442`
