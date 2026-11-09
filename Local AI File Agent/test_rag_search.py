#!/usr/bin/env python3
"""
Interactive RAG Semantic Search Verification Tool for Local AI File Agent.
Demonstrates Week 2 Deliverable: Sub-50ms Cosine Similarity Retrieval over Course Knowledge Base.
"""

import sys
import time
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.rag_engine import LocalRagEngine


def run_rag_search(query: str, top_k: int = 3):
    print("=" * 65)
    print("🔍 Local AI File Agent - RAG 語意相似度檢索驗證 (Week 2)")
    print("=" * 65)
    print(f"💬 檢索查詢: \"{query}\"")
    print(f"🎯 目標返回 Top-{top_k} 最相關歷史文獻與分類參考\n")

    store_dir = Path(__file__).parent / "vector_store"
    index_file = store_dir / "faiss_index.bin"
    meta_file = store_dir / "metadata.json"

    t0 = time.perf_counter()
    rag = LocalRagEngine(
        index_path=str(index_file),
        metadata_path=str(meta_file)
    )

    result_text = rag.search_similar(query, top_k=top_k)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    print("📊 檢索結果摘要：")
    print(result_text)
    print("-" * 65)
    print(f"⚡ 檢索總耗時 (Latency): {elapsed_ms:.2f} ms (目標 < 50 ms)")
    if elapsed_ms < 50:
        print("✅ 效能指標達成：毫秒級極速響應！")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Test RAG semantic retrieval on local knowledge base.")
    parser.add_argument(
        "--query",
        default="哪份教材有說明多模態視覺模型或讓 AI 看懂圖片？",
        help="Query sentence or keywords to search"
    )
    parser.add_argument("--top-k", type=int, default=3, help="Number of results to return")
    args = parser.parse_args()

    run_rag_search(args.query, top_k=args.top_k)


if __name__ == "__main__":
    main()

