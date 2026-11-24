# Source 02: ReAct: Synergizing Reasoning and Acting in Language Models
- **作者**：Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- **來源網址**：https://arxiv.org/abs/2210.03629
- **發布年份**：2022（ICLR 2023）
- **核心摘要**：
  1. 指出過去的研究將「推理（Reasoning，如 Chain-of-Thought）」與「行動（Acting，如直接輸出操作指令）」分開處理：純推理容易產生事實幻覺（Hallucination），純行動則缺乏高層次目標規劃。
  2. 提出 **ReAct（Reasoning + Acting）** 範式，讓 LLM 交替產生「思考軌跡（Thought）」與「具體動作（Action）」，並接收環境回傳的「觀察結果（Observation）」，形成 **`Thought -> Action -> Observation`** 的閉環迴圈。
  3. 實驗證明在多跳問答（HotpotQA）與事實驗證（FEVER）任務上，ReAct 透過主動查詢外部知識庫大幅降低幻覺，且決策過程具備高度人類可解釋性。
