"""
LLM Caller module for Local AI File Agent.
Interacts with local Ollama service and robustly parses JSON responses.
"""

import json
import re
from typing import Dict, Any, List
import requests

from .prompt_template import SYSTEM_PROMPT, CLASSIFY_PROMPT_TEMPLATE


class OllamaAgentCaller:
    def __init__(self, host: str = "http://127.0.0.1:11434", model: str = "qwen2.5-coder:7b", timeout: int = 60):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def check_health(self) -> bool:
        """Check if local Ollama server is reachable."""
        try:
            res = requests.get(f"{self.host}/api/tags", timeout=3)
            return res.status_code == 200
        except Exception:
            return False

    def classify_and_reason(
        self,
        file_info: Dict[str, Any],
        rag_context: str,
        categories: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Sends the file information and RAG context to local Ollama and returns parsed decision.
        """
        cat_str = "\n".join([f"- {c['name']}: {c.get('description', '')}" for c in categories])
        prompt = CLASSIFY_PROMPT_TEMPLATE.format(
            file_name=file_info.get("file_name", ""),
            file_size=file_info.get("file_size", 0),
            extension=file_info.get("extension", ""),
            is_binary=file_info.get("is_binary", False),
            extracted_text=file_info.get("text", "")[:3000],
            rag_context=rag_context if rag_context else "(無歷史相似文獻參考，請根據內文直接判斷)",
            category_list=cat_str
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.2,  # Low temperature for deterministic JSON output
                "top_p": 0.8
            }
        }

        try:
            # Quick check if server is reachable first
            if not self.check_health():
                print("ℹ️ [Ollama Offline] Ollama server is not running on 127.0.0.1:11434. Using rule fallback.")
                return self._fallback_decision(file_info)

            response = requests.post(
                f"{self.host}/api/chat",
                json=payload,
                timeout=(3, self.timeout)
            )
            response.raise_for_status()
            res_json = response.json()
            raw_content = res_json.get("message", {}).get("content", "").strip()

            # Clean markdown code blocks if model wrapped JSON
            cleaned_json = self._extract_json(raw_content)
            parsed = json.loads(cleaned_json)
            return parsed

        except requests.exceptions.RequestException as e:
            print(f"⚠️ [Ollama Connection Warning] Could not reach Ollama: {e}. Using rule fallback.")
            return self._fallback_decision(file_info)
        except json.JSONDecodeError as e:
            print(f"⚠️ [JSON Parse Warning] Failed to parse LLM JSON: {e}. Raw content: {raw_content[:200]}")
            return self._fallback_decision(file_info)

    def _extract_json(self, text: str) -> str:
        """Strip markdown fences ```json ... ``` from model output."""
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return text.strip()

    def _fallback_decision(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Deterministic fallback when LLM is offline or output is invalid."""
        fname = file_info.get("file_name", "unnamed_file")
        ext = file_info.get("extension", "").lower()

        cat = "General/Inbox"
        tags = ["Inbox", "Unsorted"]
        if ext in [".pdf", ".djvu"]:
            cat = "AI_Research/NLP" if "attention" in fname.lower() or "llm" in fname.lower() else "General/Documents"
            tags = ["Document", "PDF"]
        elif ext in [".py", ".js", ".html", ".md"]:
            cat = "Dev_Notes/Frontend" if ext in [".js", ".html"] else "Dev_Notes/Backend"
            tags = ["Dev", "Code"]

        return {
            "category": cat,
            "sanitized_name": fname,
            "wiki_title": fname,
            "tags": tags,
            "double_links": ["[[未整理文件]]"],
            "summary": f"自動備份歸檔之檔案：{fname}，建議後續手動檢視重點。",
            "reasoning": "觸發本機規則備援機制（Ollama 離線或回應逾時）。",
            "action_recommendation": "確認 Ollama 服務是否運行後重新索引。"
        }

