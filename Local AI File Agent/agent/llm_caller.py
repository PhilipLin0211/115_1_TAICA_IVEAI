"""
LLM Caller module for Local AI File Agent.
Interacts with local Ollama service and robustly parses JSON responses.
Works with 'requests' or falls back to built-in 'urllib.request' (zero external dependency).
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List

try:
    import requests
except ImportError:
    requests = None

import urllib.request
import urllib.error

from .prompt_template import SYSTEM_PROMPT, CLASSIFY_PROMPT_TEMPLATE


class OllamaAgentCaller:
    def __init__(self, host: str = "http://127.0.0.1:11434", model: str = "qwen2.5-coder:7b", timeout: int = 60):
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def check_health(self) -> bool:
        """Check if local Ollama server is reachable."""
        if requests is not None:
            try:
                res = requests.get(f"{self.host}/api/tags", timeout=2)
                return res.status_code == 200
            except Exception:
                return False
        else:
            try:
                req = urllib.request.Request(f"{self.host}/api/tags")
                with urllib.request.urlopen(req, timeout=2) as res:
                    return res.status == 200
            except Exception:
                return False

    def classify_and_reason(
        self,
        file_info: Dict[str, Any],
        rag_context: str,
        categories: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Sends the file information and RAG context to local Ollama with Coarse-to-Fine routing.
        """
        ext = file_info.get("extension", "").lower()
        family = file_info.get("file_type_family", "")
        file_name = file_info.get("file_name", "")

        # -------------------------------------------------------------
        # Stage 1: Coarse Deterministic Routing (Bypasses LLM for Non-Docs)
        # -------------------------------------------------------------
        if family == "installer" or ext in [".dmg", ".pkg", ".exe", ".iso", ".app"]:
            clean_title = Path(file_name).stem.replace("_", " ").replace("-", " ").title()
            return {
                "action": "MOVE",
                "category": "Software/Installers",
                "sanitized_name": file_name,
                "wiki_title": f"安裝套件: {clean_title}",
                "tags": ["Installer", "Software", "Tools"],
                "double_links": ["[[Software]]", "[[Installers]]"],
                "summary": f"軟體應用程式安裝映像檔 ({ext})，經第一階段副檔名規則直接分流歸檔至軟體庫。",
                "reasoning": "第一階段副檔名確定性硬過濾，直接分流至軟體庫保存。",
                "action_recommendation": "確認安裝完畢後可隨時移至長期封存或清理。"
            }

        if family == "media" or ext in [".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav", ".flac"]:
            clean_title = Path(file_name).stem.replace("_", " ").title()
            return {
                "action": "MOVE",
                "category": "Media",
                "sanitized_name": file_name,
                "wiki_title": f"多媒體影音: {clean_title}",
                "tags": ["Media", "AudioVisual", "Assets"],
                "double_links": ["[[Media]]", "[[Assets]]"],
                "summary": f"多媒體影音素材 ({ext})，由第一階段副檔名規則自動分流至多媒體資料夾。",
                "reasoning": "多媒體二進制格式，無需耗費 LLM 內文推論，直接走專屬媒體路由。",
                "action_recommendation": "可直接於播放器開啟或導入編輯專案。"
            }

        # -------------------------------------------------------------
        # Stage 2: Candidate Category Pruning for High-Accuracy Reasoning
        # -------------------------------------------------------------
        text_sample = file_info.get("text", "")[:3000].lower()
        filtered_categories = self._prune_categories(categories, family, ext, file_name, text_sample)

        cat_str = "\n".join([f"- {c['name']}: {c.get('description', '')}" for c in filtered_categories])
        prompt = CLASSIFY_PROMPT_TEMPLATE.format(
            file_name=file_name,
            file_size=file_info.get("file_size", 0),
            extension=ext,
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
                "temperature": 0.2,
                "top_p": 0.8
            }
        }

        try:
            if not self.check_health():
                print("ℹ️ [Ollama Offline] Ollama server is not running on 127.0.0.1:11434. Using rule fallback.")
                return self._fallback_decision(file_info)

            raw_content = ""
            if requests is not None:
                response = requests.post(
                    f"{self.host}/api/chat",
                    json=payload,
                    timeout=(3, self.timeout)
                )
                response.raise_for_status()
                res_json = response.json()
                raw_content = res_json.get("message", {}).get("content", "").strip()
            else:
                req = urllib.request.Request(
                    f"{self.host}/api/chat",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    res_json = json.loads(resp.read().decode("utf-8"))
                    raw_content = res_json.get("message", {}).get("content", "").strip()

            cleaned_json = self._extract_json(raw_content)
            parsed = json.loads(cleaned_json)
            if "action" not in parsed:
                parsed["action"] = "MOVE"
            return parsed

        except Exception as e:
            print(f"⚠️ [Ollama Inference Warning] Fallback activated: {e}")
            return self._fallback_decision(file_info)

    def _extract_json(self, text: str) -> str:
        """Strip markdown fences ```json ... ``` from model output."""
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return text.strip()

    def _prune_categories(
        self,
        categories: List[Dict[str, str]],
        family: str,
        ext: str,
        file_name: str,
        text_sample: str
    ) -> List[Dict[str, str]]:
        """
        Prunes candidate categories based on coarse clues to increase LLM classification accuracy.
        """
        if not categories:
            return [{"name": "General/Inbox", "description": "一般未分類檔案"}]

        # Check for financial receipt clues
        finance_keywords = ["invoice", "receipt", "finance", "purchase", "發票", "收據", "報帳", "gui", "統一編號", "採購單"]
        is_finance = any(k in file_name.lower() or k in text_sample for k in finance_keywords)
        if is_finance:
            finance_cats = [c for c in categories if "finance" in c["name"].lower() or "receipt" in c["name"].lower()]
            if finance_cats:
                return finance_cats

        # Check for code/backend/frontend clues
        if family == "code":
            code_cats = [c for c in categories if "dev" in c["name"].lower() or "code" in c["name"].lower() or "general" in c["name"].lower()]
            if code_cats:
                return code_cats

        # Documents / Academic Papers: remove installer & media
        if family == "document":
            doc_cats = [c for c in categories if not any(x in c["name"].lower() for x in ["installer", "software", "media"])]
            if doc_cats:
                return doc_cats

        return categories

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
            "action": "MOVE",
            "category": cat,
            "sanitized_name": fname,
            "wiki_title": fname,
            "tags": tags,
            "double_links": ["[[未整理文件]]"],
            "summary": f"自動備份歸檔之檔案：{fname}，建議後續手動檢視重點。",
            "reasoning": "觸發本機規則備援機制（Ollama 離線或回應逾時）。",
            "action_recommendation": "確認 Ollama 服務是否運行後重新索引。"
        }
