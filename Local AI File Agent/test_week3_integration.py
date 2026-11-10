#!/usr/bin/env python3
"""
Week 3 Integration & End-to-End Reasoning Test for Local AI File Agent.
Validates the complete closed loop:
1. File Ingestion & Parsing
2. RAG Context Retrieval (Top-K against Course Knowledge Base)
3. Qwen 2.5 Coder JSON Decision (MOVE-Only Guard)
4. Safe File Movement & Collision Renaming
5. Obsidian LLMWiki Note Generation (YAML Frontmatter, [[Double-Links]], #tags)
6. Automatic Maintenance of index.md and log.md
7. Security Audit Trail & Directory Snapshot
8. Incremental Vector Store Online Update & Real-Time Query Verification
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.file_parser import extract_text_from_file
from utils.file_mover import safe_move_file, validate_agent_permission
from utils.wiki_builder import create_obsidian_note
from utils.audit_logger import AuditLogger
from agent.llm_caller import OllamaAgentCaller
from agent.rag_engine import LocalRagEngine


def run_week3_integration_test():
    print("=" * 70)
    print("🧠 Local AI File Agent - Week 3 全端到端決策與第二大腦整合測試")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        downloads_mock = tmp_path / "Downloads"
        vault_mock = tmp_path / "Obsidian_Vault"
        vector_mock = tmp_path / "vector_store"
        downloads_mock.mkdir()
        vault_mock.mkdir()
        vector_mock.mkdir()

        # Step 1: Create a realistic incoming file
        sample_filename = "2024_Multimodal_Vision_Language_Models_Survey.txt"
        sample_file = downloads_mock / sample_filename
        sample_content = (
            "A Comprehensive Survey on Vision-Language Models (VLMs) and Multimodal AI Systems\n"
            "Authors: Lin et al., NTUST AI Lab, 2024.\n\n"
            "Abstract: This survey presents a thorough analysis of modern Vision-Language Models (VLMs), "
            "focusing on visual encoders like CLIP and SigLIP, cross-attention alignment mechanisms, "
            "and spatial image comprehension. We evaluate zero-shot reasoning and document understanding.\n\n"
            "Conclusion: Multimodal foundation models bridge perceptual vision and cognitive reasoning, "
            "paving the way for autonomous embodied AI agents in complex environments."
        )
        sample_file.write_text(sample_content, encoding="utf-8")
        print(f"\n[步驟 1] 模擬使用者下載新檔案: {sample_filename}")
        print(f"  • 檔案大小: {sample_file.stat().st_size} bytes")

        # Step 2: Content Parsing & Token Guard
        print("\n[步驟 2] 萃取內文與元數據 (Token 防爆截斷)...")
        file_info = extract_text_from_file(sample_file)
        assert len(file_info["text"]) > 0
        print(f"  • 成功解析文字長度: {len(file_info['text'])} 字元")
        print(f"  • 摘要預覽: {file_info['text'][:100]}...")

        # Step 3: RAG Retrieval from Vector Store
        print("\n[步驟 3] 執行 RAG 本地語意相似度檢索 (查詢相關課程教材)...")
        rag = LocalRagEngine(
            index_path=str(vector_mock / "faiss_index.bin"),
            metadata_path=str(vector_mock / "metadata.json")
        )
        # Pre-seed course slide 07 into the test vector store
        rag.add_document(
            title="07 讓 AI 看懂你的世界",
            category="Course_Materials/IVEAI",
            summary="多模態大模型 (Multimodal LLM / VLM) 原理，結合視覺編碼器 (CLIP / SigLIP) 讓語言模型理解圖像與空間場景。"
        )
        rag_context = rag.search_similar(file_info["text"], top_k=2)
        print(f"  • RAG 檢索命中的相似歷史紀錄:\n{rag_context}")

        # Step 4: Qwen 2.5 Coder Classification & Decision
        print("\n[步驟 4] 呼叫決策引擎 (Qwen 2.5 Coder / Few-Shot JSON 規範)...")
        categories = [
            {"name": "AI_Research/Vision", "description": "電腦視覺、Diffusion、NeRF、圖像生成與辨識論文"},
            {"name": "AI_Research/NLP", "description": "自然語言處理、大型語言模型、Transformer、Attention 文獻"},
            {"name": "Course_Materials/IVEAI", "description": "臺科大 TAICA_IVEAI 課程講義與作業"}
        ]
        agent_caller = OllamaAgentCaller()
        decision = agent_caller.classify_and_reason(file_info, rag_context, categories)
        print(f"  • 決定分類路徑: {decision.get('category')}")
        print(f"  • 正規化新檔名: {decision.get('sanitized_name')}")
        print(f"  • 筆記標題: {decision.get('wiki_title')}")
        print(f"  • 標籤 Tags: {decision.get('tags')}")
        print(f"  • 雙向連結: {decision.get('double_links')}")

        # Step 5: Safe File Movement with MOVE-ONLY check
        print("\n[步驟 5] 執行 MOVE-ONLY 權限核驗與防碰撞安全搬移...")
        action_requested = decision.get("action", "MOVE")
        validate_agent_permission(action_requested)
        dest_dir = vault_mock / decision.get("category", "General/Inbox")

        ok, final_path = safe_move_file(
            source=sample_file,
            destination_dir=dest_dir,
            target_filename=decision.get("sanitized_name"),
            dry_run=False,
            requested_action=action_requested
        )
        assert ok is True
        assert Path(final_path).exists()
        print(f"  ✅ 檔案安全搬移成功: {final_path}")

        # Step 6: Obsidian LLMWiki Note Generation
        print("\n[步驟 6] 自動產生 Obsidian 導讀筆記與更新總索引...")
        note_path = create_obsidian_note(
            vault_dir=vault_mock,
            relative_category=decision.get("category", "General/Inbox"),
            file_info=file_info,
            decision=decision,
            dry_run=False
        )
        assert note_path.exists()
        note_text = note_path.read_text(encoding="utf-8")
        assert "---" in note_text  # YAML frontmatter check
        assert decision.get("wiki_title") in note_text
        print(f"  ✅ Obsidian 筆記已建立: {note_path.name}")

        index_file = vault_mock / "index.md"
        assert index_file.exists()
        assert decision.get("wiki_title") in index_file.read_text(encoding="utf-8")
        print(f"  ✅ 總索引目錄 index.md 已成功更新雙向連結！")

        # Step 7: Security Audit Logging & Directory Snapshot
        print("\n[步驟 7] 紀錄審計日誌與目標目錄快照...")
        logger = AuditLogger(log_dir=tmp_path / "history", vault_dir=vault_mock)
        audit_entry = logger.record_action(
            action=action_requested,
            source_path=sample_file,
            destination_path=Path(final_path),
            file_info=file_info,
            decision=decision,
            watch_dir=downloads_mock,
            dry_run=False
        )
        assert audit_entry["permission_guard"]["verified"] is True
        target_files = audit_entry["folder_directory_snapshots"]["target_directory"]["total_files"]
        print(f"  ✅ 動作審計紀錄完成: ID {audit_entry['id']}")
        print(f"  📸 目標目錄現有檔案快照數: {target_files} 筆")

        # Step 8: Incremental RAG Vector Index Update & Immediate Verification
        print("\n[步驟 8] 即時增量更新向量資料庫並驗證再次檢索...")
        rag.add_document(
            title=decision.get("wiki_title"),
            category=decision.get("category"),
            summary=decision.get("summary")
        )
        # Search again for the newly added document
        re_search = rag.search_similar("請問有關於 SigLIP 與 Vision-Language Model 的文獻嗎？", top_k=1)
        print(f"  🔍 新增後的即時檢索結果:\n{re_search}")
        assert decision.get("wiki_title") in re_search
        print("  ✅ 知識庫即時自我增長閉環驗證通過！")

        print("\n" + "=" * 70)
        print("🎉 WEEK 3 全端到端決策、知識庫閉環與安全防禦測試全數通過 (8/8)！")
        print("=" * 70)


if __name__ == "__main__":
    run_week3_integration_test()

