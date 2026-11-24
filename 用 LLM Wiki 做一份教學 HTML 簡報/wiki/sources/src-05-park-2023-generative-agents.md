# Source 05: Generative Agents: Interactive Simulacra of Human Behavior
- **作者**：Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein
- **來源網址**：https://arxiv.org/abs/2304.03442
- **發布年份**：2023（UIST 2023，史丹佛 Smallville 虛擬小鎮研究）
- **核心摘要**：
  1. 在名為 Smallville 的沙盒虛擬小鎮中部署 25 位由 LLM 驅動的生成式代理人，展現可信的日常作息、社交傳播與自發性協作（如自主籌辦情人節派對）。
  2. 設計完整的 **Memory Stream（記憶流）與檢索評分架構**：代理人持續記錄所有觀察事件，檢索時綜合評估三個維度——**Recency（新近度）**、**Importance（重要性）** 與 **Relevance（語意相關度）**。
  3. 提出 **Reflection（反思機制）**：當累積事件的重要性總分超過門檻時，Agent 會定期暫停並將零碎記憶歸納為高層次的抽象洞見（例如「我最近常和某人討論音樂」），實現真正的長期人格一致性。
