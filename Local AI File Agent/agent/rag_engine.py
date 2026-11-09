"""
RAG Engine module for Local AI File Agent.
Handles Ollama embedding generation and FAISS vector index retrieval.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import requests

try:
    import faiss
    import numpy as np
except ImportError:
    faiss = None
    np = None


class LocalRagEngine:
    def __init__(
        self,
        host: str = "http://127.0.0.1:11434",
        embed_model: str = "nomic-embed-text",
        index_path: str = "./vector_store/faiss_index.bin",
        metadata_path: str = "./vector_store/metadata.json",
        dimension: int = 768
    ):
        self.host = host.rstrip("/")
        self.embed_model = embed_model
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.dimension = dimension
        self.index = None
        self.metadata = []
        self._load_or_init()

    def _load_or_init(self):
        """Load existing FAISS index or create an empty one."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        if faiss is not None:
            if self.index_path.exists() and self.metadata_path.exists():
                try:
                    self.index = faiss.read_index(str(self.index_path))
                    with open(self.metadata_path, "r", encoding="utf-8") as f:
                        self.metadata = json.load(f)
                    return
                except Exception as e:
                    print(f"⚠️ [FAISS Load Warning] Could not load index: {e}, initializing fresh index.")

            # Create new L2 / Cosine Index
            self.index = faiss.IndexFlatIP(self.dimension)  # Inner Product for normalized cosine
            self.metadata = []

    def get_embedding(self, text: str) -> List[float]:
        """Fetch embedding vector from Ollama (supports modern /api/embed and legacy /api/embeddings)."""
        if not text.strip():
            return [0.0] * self.dimension

        # 1. Try modern Ollama /api/embed endpoint first
        try:
            embed_url = f"{self.host}/api/embed"
            payload = {"model": self.embed_model, "input": text[:2000]}
            res = requests.post(embed_url, json=payload, timeout=(2, 10))
            if res.status_code == 200:
                data = res.json()
                embeddings = data.get("embeddings", [])
                if embeddings and len(embeddings) > 0:
                    vec = embeddings[0]
                    return self._normalize_vec(vec)
        except Exception:
            pass

        # 2. Fallback to legacy /api/embeddings endpoint
        try:
            legacy_url = f"{self.host}/api/embeddings"
            payload = {"model": self.embed_model, "prompt": text[:2000]}
            res = requests.post(legacy_url, json=payload, timeout=(2, 10))
            if res.status_code == 200:
                vec = res.json().get("embedding", [])
                if vec:
                    return self._normalize_vec(vec)
        except Exception as e:
            pass

        return [0.0] * self.dimension

    def _normalize_vec(self, vec: List[float]) -> List[float]:
        """L2-normalize vector for Cosine similarity calculation."""
        if np is not None and vec:
            arr = np.array(vec, dtype="float32")
            norm = np.linalg.norm(arr)
            if norm > 0:
                arr = arr / norm
            return arr.tolist()
        return vec

    def search_similar(self, query_text: str, top_k: int = 3) -> str:
        """Search top-k most similar past documents in FAISS index."""
        if faiss is None or self.index is None or self.index.ntotal == 0:
            return "(知識庫目前為冷啟動狀態，暫無過往相似記錄)"

        q_vec = self.get_embedding(query_text)
        if not q_vec or all(v == 0.0 for v in q_vec):
            return "(向量生成失敗或為空文本)"

        arr = np.array([q_vec], dtype="float32")
        scores, indices = self.index.search(arr, min(top_k, self.index.ntotal))

        context_lines = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                item = self.metadata[idx]
                score = scores[0][i]
                context_lines.append(
                    f"- 文獻: {item.get('title')} | 分類: {item.get('category')} | 相似度: {score:.3f}\n  摘要: {item.get('summary', '')[:120]}"
                )

        return "\n".join(context_lines) if context_lines else "(無足夠相似文獻)"

    def add_document(self, title: str, category: str, summary: str):
        """Add newly categorized file into FAISS index and persist."""
        embed_text = f"Title: {title}\nCategory: {category}\nSummary: {summary}"
        vec = self.get_embedding(embed_text)

        if faiss is not None and self.index is not None and vec and np is not None:
            arr = np.array([vec], dtype="float32")
            self.index.add(arr)

        self.metadata.append({
            "title": title,
            "category": category,
            "summary": summary
        })
        self._save()

    def _save(self):
        """Persist index and metadata to disk."""
        if faiss is not None and self.index is not None:
            try:
                faiss.write_index(self.index, str(self.index_path))
            except Exception as e:
                print(f"⚠️ [FAISS Save Warning] {e}")

        try:
            with open(self.metadata_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ [Metadata Save Warning] {e}")

