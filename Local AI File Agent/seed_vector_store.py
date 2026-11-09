#!/usr/bin/env python3
"""
Seed Vector Store Script for Local AI File Agent.
Pre-indexes course PPTs and classic research papers into FAISS vector database.
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.rag_engine import LocalRagEngine
from utils.file_parser import extract_text_from_file

# Sample seed data for instant offline bootstrapping
DEFAULT_SEEDS = [
    {
        "title": "01 如何不焦慮地學 AI",
        "category": "Course_Materials/IVEAI",
        "summary": "臺科大 TAICA_IVEAI 課程第一週講義。引導學生建立正確的 AI 學習心態，從實作中探索神經網路與生成式 AI 工具應用。"
    },
    {
        "title": "02 神經網路的概念",
        "category": "Course_Materials/IVEAI",
        "summary": "介紹感知器、多層感知機 (MLP)、權重反向傳播 (Backpropagation) 與梯度下降法 (Gradient Descent) 之底層數學原理。"
    },
    {
        "title": "03 AI 為什麼每次都不一樣？",
        "category": "Course_Materials/IVEAI",
        "summary": "探討生成式語言模型的隨機性來源，包含溫度參數 (Temperature)、Top-k、Top-p 採樣與機率分佈抽樣機制。"
    },
    {
        "title": "04 LLM 只是在猜下一個字？",
        "category": "Course_Materials/IVEAI",
        "summary": "剖析次字元預測 (Next-token prediction) 與自迴歸語言模型機制，介紹因果自注意力 (Causal Self-Attention)。"
    },
    {
        "title": "05 AI 怎麼記得前面說過什麼？",
        "category": "Course_Materials/IVEAI",
        "summary": "解析長文本上下文視窗 (Context Window)、注意力衰減與 KV Cache 機制，說明 Transformer 如何維持上下文對話連貫。"
    },
    {
        "title": "06 打造自己的對話機器人",
        "category": "Course_Materials/IVEAI",
        "summary": "深入 Prompt Engineering、System Prompt 設計、Role-playing 與工具調用 (Tool Calling / Function Calling) 實作。"
    },
    {
        "title": "07 讓 AI 看懂你的世界",
        "category": "Course_Materials/IVEAI",
        "summary": "多模態大模型 (Multimodal LLM / VLM) 原理，結合視覺編碼器 (CLIP / SigLIP) 讓語言模型理解圖像與空間場景。"
    },
    {
        "title": "08 教 AI 做事的方法",
        "category": "Course_Materials/IVEAI",
        "summary": "自主智慧代理 (Autonomous Agent) 設計架構：ReAct 框架、思維鏈 (Chain of Thought)、記憶庫與任務分解演算法。"
    },
    {
        "title": "Vaswani et al. (2017) Attention Is All You Need",
        "category": "AI_Research/NLP",
        "summary": "經典 Transformer 論文，完全基於自注意力機制 (Self-Attention) 取代循環與卷積神經網路，成為現代大語言模型之核心架構。"
    }
]


def seed_database(ppt_dir: Path = None, live_ollama: bool = False):
    print("=" * 65)
    print("🌱 Local AI File Agent - 向量資料庫預置 (Vector Store Seeding)")
    print("=" * 65)

    store_dir = Path(__file__).parent / "vector_store"
    store_dir.mkdir(parents=True, exist_ok=True)
    index_file = store_dir / "faiss_index.bin"
    meta_file = store_dir / "metadata.json"

    rag = LocalRagEngine(
        index_path=str(index_file),
        metadata_path=str(meta_file)
    )

    count = 0
    # 1. Index preset course items
    print(f"\n📚 正在注入 {len(DEFAULT_SEEDS)} 筆課程重點與文獻種子資料...")
    for item in DEFAULT_SEEDS:
        rag.add_document(
            title=item["title"],
            category=item["category"],
            summary=item["summary"]
        )
        count += 1
        print(f"  ✅ 已注入: {item['title']} [{item['category']}]")

    # 2. If PPT directory provided, scan and index real PDFs
    if ppt_dir and ppt_dir.exists():
        print(f"\n📂 掃描實體講義資料夾: {ppt_dir}")
        for pdf_file in ppt_dir.glob("*.pdf"):
            file_info = extract_text_from_file(pdf_file)
            summary_text = file_info.get("text", "")[:300].strip()
            if not summary_text or "Error" in summary_text:
                summary_text = f"臺科大 TAICA_IVEAI 課程講義：{pdf_file.stem}"

            rag.add_document(
                title=pdf_file.stem,
                category="Course_Materials/IVEAI",
                summary=summary_text
            )
            count += 1
            print(f"  📄 已建立索引: {pdf_file.name}")

    print("\n" + "=" * 65)
    print(f"🎉 向量資料庫注入完成！共建立 {count} 筆語意知識索引。")
    print(f"📍 索引位置: {index_file}")
    print(f"📍 元數據位置: {meta_file}")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Pre-seed FAISS vector store with course materials.")
    parser.add_argument("--ppt-dir", default="../PPT", help="Path to course PPT directory")
    parser.add_argument("--live", action="store_true", help="Connect to live Ollama server for real embeddings")
    args = parser.parse_args()

    ppt_path = Path(args.ppt_dir).resolve()
    seed_database(ppt_path if ppt_path.exists() else None, live_ollama=args.live)


if __name__ == "__main__":
    main()

