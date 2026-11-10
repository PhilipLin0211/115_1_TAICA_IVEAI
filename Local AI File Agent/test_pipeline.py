#!/usr/bin/env python3
"""
Quick Pipeline Verification Script for Local AI File Agent.
Simulates handling a sample file in --dry-run mode without requiring active Watchdog daemon.
"""

import sys
from pathlib import Path
import tempfile

from utils.file_parser import extract_text_from_file
from utils.file_mover import safe_move_file, PermissionDeniedError
from utils.wiki_builder import create_obsidian_note
from utils.audit_logger import AuditLogger
from agent.llm_caller import OllamaAgentCaller
from agent.rag_engine import LocalRagEngine


def run_pipeline_test():
    print("=" * 65)
    print("🧪 Running Local AI File Agent Pipeline Verification Test")
    print("=" * 65)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        downloads_mock = tmp_path / "Downloads"
        vault_mock = tmp_path / "Obsidian_Vault"
        downloads_mock.mkdir()
        vault_mock.mkdir()

        # Create a mock paper file
        sample_file = downloads_mock / "attention_is_all_you_need.txt"
        sample_file.write_text(
            "Attention Is All You Need\n"
            "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit...\n\n"
            "Abstract: The dominant sequence transduction models are based on complex "
            "recurrent or convolutional neural networks. We propose a new simple network "
            "architecture, the Transformer, based solely on attention mechanisms, dispensing "
            "with recurrence and convolutions entirely.\n\n"
            "Conclusion: The Transformer is the first sequence transduction model based entirely on self-attention."
        )

        print(f"\n[Test 1] Extracting file content: {sample_file.name}")
        info = extract_text_from_file(sample_file)
        print(f"  • Extracted length: {len(info['text'])} characters")
        print(f"  • Preview: {info['text'][:120]}...\n")

        print("[Test 2] Initializing RAG Engine & LLM Caller")
        rag = LocalRagEngine(index_path=str(tmp_path / "faiss.bin"), metadata_path=str(tmp_path / "meta.json"))
        caller = OllamaAgentCaller()

        categories = [
            {"name": "AI_Research/NLP", "description": "自然語言處理與 Transformer"},
            {"name": "Course_Materials/IVEAI", "description": "TAICA_IVEAI 課程教材"},
            {"name": "Finance/Receipts", "description": "發票與財務收據"}
        ]

        print("[Test 3] Simulating classification & reasoning...")
        decision = caller.classify_and_reason(info, rag_context="", categories=categories)
        print(f"  • Category chosen: {decision.get('category')}")
        print(f"  • Normalized name: {decision.get('sanitized_name')}")
        print(f"  • Wiki note title: {decision.get('wiki_title')}")
        print(f"  • Double links: {decision.get('double_links')}")

        print("\n[Test 4] Testing Safe File Movement (Dry-Run)")
        target_dir = vault_mock / decision.get("category", "General/Inbox")
        ok, dest_path = safe_move_file(sample_file, target_dir, decision.get("sanitized_name"), dry_run=True)
        assert ok, "Dry-run move failed!"

        print("\n[Test 5] Testing Obsidian LLMWiki Note Generation (Dry-Run)")
        note_path = create_obsidian_note(
            vault_dir=vault_mock,
            relative_category=decision.get("category", "General/Inbox"),
            file_info=info,
            decision=decision,
            dry_run=True
        )

        print("\n[Test 6] Testing Security Permission Boundary (MOVE-ONLY)")
        # Test 6a: Authorized MOVE should pass
        ok, _ = safe_move_file(sample_file, target_dir, dry_run=True, requested_action="MOVE")
        assert ok, "Valid MOVE action was blocked!"
        print("  ✅ Authorized action 'MOVE' permitted.")

        # Test 6b: Unauthorized DELETE should raise PermissionDeniedError
        try:
            safe_move_file(sample_file, target_dir, dry_run=True, requested_action="DELETE")
            assert False, "Security violation: DELETE operation was not blocked!"
        except PermissionDeniedError as e:
            print(f"  🛡️ Unauthorized action 'DELETE' successfully BLOCKED! ({e})")

        print("\n[Test 7] Testing Audit Logger & Folder Directory Snapshot")
        logger = AuditLogger(log_dir=tmp_path / "history", vault_dir=vault_mock)
        audit_entry = logger.record_action(
            action="MOVE",
            source_path=sample_file,
            destination_path=dest_path,
            file_info=info,
            decision=decision,
            watch_dir=downloads_mock,
            dry_run=True
        )
        assert audit_entry["permission_guard"]["verified"] is True
        print(f"  ✅ Audit log entry saved: ID {audit_entry['id']}")
        print(f"  📸 Target directory snapshot files count: {audit_entry['folder_directory_snapshots']['target_directory'].get('total_files')}")

        print("\n[Test 8] Testing Lifecycle Event Logging (Attach & Detach Snapshot)")
        attach_event = logger.record_lifecycle_event("ATTACH", downloads_mock, "測試掛載監聽")
        detach_event = logger.record_lifecycle_event("DETACH", downloads_mock, "測試卸載停用")
        assert attach_event["event_type"] == "ATTACH"
        assert detach_event["event_type"] == "DETACH"
        print("  ✅ Lifecycle event logging verified: ATTACH and DETACH successfully recorded.")

        print("\n" + "=" * 65)
        print("🎉 ALL PIPELINE & SECURITY BOUNDARY CHECKS PASSED (8/8)!")
        print("=" * 65)


if __name__ == "__main__":
    run_pipeline_test()

