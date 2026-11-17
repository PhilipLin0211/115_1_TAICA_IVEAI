"""
HDBSCAN & Density-Based Adaptive Topic Discovery Module for Local AI File Agent.
Analyzes vector distributions from vector_store/metadata.json, discovers emerging 
document clusters, and proposes new hierarchical category folders dynamically.
Requires no pre-trained deep learning weights (.pt/.pkl); operates purely on 
768-dim embeddings via unsupervised mathematical density clustering.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np

# Optional scikit-learn HDBSCAN with pure numpy cosine fallback
try:
    from sklearn.cluster import HDBSCAN
except ImportError:
    HDBSCAN = None


class TopicClusterAnalyzer:
    """
    Unsupervised cluster analyzer for adaptive directory evolution.
    """

    def __init__(self, metadata_path: str = None):
        if metadata_path is None:
            self.metadata_path = Path(__file__).parent.parent / "vector_store" / "metadata.json"
        else:
            self.metadata_path = Path(metadata_path)

    def load_vectors(self) -> Tuple[List[Dict[str, Any]], np.ndarray]:
        """Load document metadata and 768-dim embedding matrix."""
        if not self.metadata_path.exists():
            return [], np.empty((0, 768), dtype="float32")

        try:
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return [], np.empty((0, 768), dtype="float32")

        valid_items = []
        vectors = []
        for item in data:
            vec = item.get("embedding")
            if vec and isinstance(vec, list) and len(vec) == 768:
                valid_items.append(item)
                vectors.append(vec)

        if not vectors:
            return [], np.empty((0, 768), dtype="float32")

        arr = np.array(vectors, dtype="float32")
        # Ensure L2 normalization for exact cosine metric
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        arr = arr / norms
        return valid_items, arr

    def fit_clusters(self, min_cluster_size: int = 2) -> Dict[str, Any]:
        """
        Runs HDBSCAN (or pure numpy cosine density fallback) on knowledge embeddings.
        Returns cluster assignments and density summary.
        """
        items, matrix = self.load_vectors()
        n_samples = len(items)

        if n_samples < min_cluster_size:
            return {
                "status": "INSUFFICIENT_DATA",
                "message": f"目前向量庫僅有 {n_samples} 筆文件，需累積至少 {min_cluster_size} 筆方可啟動 HDBSCAN 分群。",
                "clusters": {},
                "noise_count": n_samples
            }

        labels = []
        algorithm_used = "sklearn.HDBSCAN"

        if True:
            try:
                from sklearn.cluster import HDBSCAN
                # Euclidean on normalized vectors strictly equates to Cosine distance: d^2 = 2(1 - cos)
                clusterer = HDBSCAN(
                    min_cluster_size=min_cluster_size,
                    min_samples=1,
                    metric="euclidean",
                    copy=True
                )
                labels = clusterer.fit_predict(matrix).tolist()
            except Exception as e:
                labels = self._fallback_numpy_cosine_clustering(matrix, min_cluster_size=min_cluster_size)
                algorithm_used = f"Numpy_Cosine_DBSCAN (fallback from {e})"
        else:
            labels = self._fallback_numpy_cosine_clustering(matrix, min_cluster_size=min_cluster_size)
            algorithm_used = "Numpy_Cosine_Density_Clustering"

        # Group items by cluster label
        clusters: Dict[int, List[Dict[str, Any]]] = {}
        for idx, lbl in enumerate(labels):
            item = items[idx]
            clusters.setdefault(lbl, []).append({
                "title": item.get("title", "Untitled"),
                "category": item.get("category", "General/Inbox"),
                "summary": item.get("summary", "")[:120]
            })

        noise_items = clusters.get(-1, [])
        valid_clusters = {k: v for k, v in clusters.items() if k != -1}

        return {
            "status": "SUCCESS",
            "algorithm": algorithm_used,
            "total_documents": n_samples,
            "clusters_count": len(valid_clusters),
            "noise_count": len(noise_items),
            "clusters": valid_clusters,
            "outliers_or_noise": noise_items
        }

    def _fallback_numpy_cosine_clustering(self, matrix: np.ndarray, min_cluster_size: int = 2, threshold: float = 0.65) -> List[int]:
        """
        Pure NumPy Cosine Distance Connected-Components Clustering.
        Zero dependency on scikit-learn.
        """
        n = matrix.shape[0]
        # Cosine similarity matrix
        sim_matrix = np.dot(matrix, matrix.T)
        adj = (sim_matrix >= threshold).astype(int)

        visited = [False] * n
        labels = [-1] * n
        curr_cluster = 0

        for i in range(n):
            if not visited[i]:
                # BFS/DFS connected components
                component = []
                queue = [i]
                visited[i] = True
                while queue:
                    node = queue.pop(0)
                    component.append(node)
                    neighbors = np.where(adj[node] == 1)[0]
                    for nb in neighbors:
                        if not visited[nb]:
                            visited[nb] = True
                            queue.append(nb)

                if len(component) >= min_cluster_size:
                    for node in component:
                        labels[node] = curr_cluster
                    curr_cluster += 1
                else:
                    for node in component:
                        labels[node] = -1

        return labels

    def discover_emerging_topics(self, min_cluster_size: int = 2) -> List[Dict[str, Any]]:
        """
        Identifies tightly clustered document groups and generates recommended new category names.
        """
        res = self.fit_clusters(min_cluster_size=min_cluster_size)
        if res.get("status") != "SUCCESS":
            return []

        suggestions = []
        for cluster_id, items in res.get("clusters", {}).items():
            # Check existing categories distribution in this cluster
            categories_present = set(it["category"] for it in items)
            titles = [it["title"] for it in items]

            # Detect common keywords or themes across titles
            combined_text = " ".join([f"{it['title']} {it['summary']}" for it in items]).lower()
            
            suggested_name = self._synthesize_category_name(titles, combined_text)
            suggestions.append({
                "cluster_id": cluster_id,
                "document_count": len(items),
                "member_titles": titles,
                "current_categories": list(categories_present),
                "suggested_new_category": suggested_name,
                "recommendation_reason": f"這 {len(items)} 份文獻在語意空間中聚集為高密度群集，目前分散於 {list(categories_present)}，建議開闢統一專屬目錄。"
            })

        return suggestions

    def _synthesize_category_name(self, titles: List[str], text: str) -> str:
        """Heuristic topic synthesizer for offline mode (or prompts LLM when online)."""
        keywords_map = [
            (["multimodal", "vlm", "vision", "clip", "siglip", "看懂"], "AI_Research/Multimodal_Vision"),
            (["transformer", "attention", "llm", "nlp", "bert"], "AI_Research/Transformers_NLP"),
            (["3d", "nerf", "gaussian", "splatting"], "AI_Research/3D_Generation"),
            (["robot", "agent", "planning", "tool"], "AI_Research/Autonomous_Agents"),
            (["taica", "iveai", "作業", "講義", "臺科大"], "Course_Materials/IVEAI"),
            (["invoice", "receipt", "發票", "收據"], "Finance/Receipts"),
            (["docker", "fastapi", "backend", "database"], "Dev_Notes/Backend"),
            (["frontend", "react", "vue", "css", "ui"], "Dev_Notes/Frontend")
        ]

        for keys, cat in keywords_map:
            if any(k in text for k in keys):
                return cat

        # Default fallback
        first_title_clean = "".join(c for c in titles[0] if c.isalnum() or c in " _-")[:20].strip()
        return f"AI_Research/{first_title_clean.replace(' ', '_')}"
