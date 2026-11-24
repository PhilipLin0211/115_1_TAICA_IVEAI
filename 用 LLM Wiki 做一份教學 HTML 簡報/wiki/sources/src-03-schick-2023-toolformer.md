# Source 03: Toolformer: Language Models Can Teach Themselves to Use Tools
- **作者**：Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, Thomas Scialom
- **來源網址**：https://arxiv.org/abs/2302.04761
- **發布年份**：2023（NeurIPS 2023）
- **核心摘要**：
  1. 探討如何讓語言模型在**不依賴大量人工標註資料**的前提下，自主學會「何時該呼叫哪個工具、該傳入什麼參數，以及如何把工具回傳值融入後續回答」。
  2. 提出自我監督學習（Self-Supervised）流程：讓模型在一般文本中嘗試插入 API 呼叫標籤（如計算機、問答系統、搜尋引擎、翻譯器、日曆），並只保留「確實能降低預測下一個字困惑度（Perplexity / Loss）」的有效呼叫範例來微調模型。
  3. 證明僅 6.7B 參數的 GPT-J 經過 Toolformer 訓練後，在數學運算與時效性問答上能擊敗體積大上數十倍的 GPT-3（175B）。
