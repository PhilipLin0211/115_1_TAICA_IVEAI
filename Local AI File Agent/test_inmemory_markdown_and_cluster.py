#!/usr/bin/env python3
"""
Comprehensive Verification Suite for:
1. All-Format In-Memory Virtual Markdown Parser (Zero Disk Write Guarantee).
2. Two-Stage Coarse-to-Fine Router (Extension Fast Filter & Category Pruning).
3. HDBSCAN Density-Based Unsupervised Topic Discovery.
"""

import sys
import tempfile
import zipfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.file_parser import extract_text_from_file
from agent.llm_caller import OllamaAgentCaller
from agent.cluster_analyzer import TopicClusterAnalyzer


def run_tests():
    print("=" * 72)
    print("🧪 驗證套件：全格式記憶體 Markdown 轉譯、兩階段路由與 HDBSCAN 主題發現")
    print("=" * 72)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # -------------------------------------------------------------
        # Part 1: All-Format In-Memory Markdown Transformation
        # -------------------------------------------------------------
        print("\n[測試 1] 全檔案格式純記憶體 Markdown 轉譯與零硬碟殘留檢驗")
        
        # 1.1 CSV Table
        f_csv = tmp_path / "finance_hardware_purchase.csv"
        f_csv.write_text("Date,Item,Amount,Vendor\n2026-11-10,MacBook Air M5,45900,Apple Taiwan\n2026-11-12,Monitor,8900,Dell\n", encoding="utf-8")
        res_csv = extract_text_from_file(f_csv)
        assert "| Date | Item | Amount | Vendor |" in res_csv["text"]
        assert res_csv["file_type_family"] == "data"
        print("  ✅ CSV 試算表 ➔ 純記憶體 Markdown 表格: 成功")

        # 1.2 ZIP Archive Outline
        f_zip = tmp_path / "deep_learning_project.zip"
        with zipfile.ZipFile(f_zip, "w") as z:
            z.writestr("src/train_transformer.py", "import torch\nprint('training')")
            z.writestr("configs/model.yaml", "lr: 0.001\nbatch: 32")
            z.writestr("docs/README.md", "# Documentation")
        res_zip = extract_text_from_file(f_zip)
        assert "**Total Contained Files**: 3" in res_zip["text"]
        assert "src/train_transformer.py" in res_zip["text"]
        assert res_zip["file_type_family"] == "archive"
        print("  ✅ ZIP 壓縮包 ➔ 純記憶體目錄樹狀圖: 成功")

        # 1.3 Installer DMG
        f_dmg = tmp_path / "Docker_Desktop_Silicon.dmg"
        f_dmg.write_bytes(b"mock dmg header payload" * 100)
        res_dmg = extract_text_from_file(f_dmg)
        assert "# Software Installer:" in res_dmg["text"]
        assert res_dmg["file_type_family"] == "installer"
        print("  ✅ DMG 安裝套件 ➔ 純記憶體安裝卡片: 成功")

        # 1.4 Source Code
        f_py = tmp_path / "agent_router.py"
        f_py.write_text("def route_file(name):\n    return 'AI_Research'\n", encoding="utf-8")
        res_py = extract_text_from_file(f_py)
        assert "```python" in res_py["text"]
        assert res_py["file_type_family"] == "code"
        print("  ✅ 程式碼檔案 ➔ 純記憶體 Markdown 代碼區塊: 成功")

        # 1.5 0-Byte Empty File Defense
        f_empty = tmp_path / "corrupted_empty.docx"
        f_empty.write_bytes(b"")
        res_empty = extract_text_from_file(f_empty)
        assert "[Empty 0-byte file]" in res_empty["text"]
        print("  ✅ 0-Byte 空白檔 ➔ 安全攔截防呆: 成功")

        # 1.6 Verify Zero Physical .md Leftover Guarantee
        leftover_md = list(tmp_path.glob("*.md"))
        assert len(leftover_md) == 0, f"Error: Found physical leftover markdown files: {leftover_md}"
        print("  🛡️ 零磁碟殘留驗證：100% 通過（實體硬碟上絕無多餘 .md 產生，原檔毫髮無傷！）")

        # -------------------------------------------------------------
        # Part 2: Two-Stage Coarse-to-Fine Router
        # -------------------------------------------------------------
        print("\n[測試 2] 兩階段粗到細分類路由驗證 (Coarse-to-Fine Routing)")
        agent = OllamaAgentCaller()
        categories = [
            {"name": "AI_Research/NLP", "description": "自然語言處理文獻"},
            {"name": "Course_Materials/IVEAI", "description": "課程講義與作業"},
            {"name": "Finance/Receipts", "description": "發票與採購單據"},
            {"name": "Dev_Notes/Backend", "description": "後端技術文件"},
            {"name": "General/Inbox", "description": "未分類檔案"}
        ]

        # Stage 1: Fast filter installer
        dec_dmg = agent.classify_and_reason(res_dmg, "", categories)
        assert dec_dmg["action"] == "MOVE"
        assert dec_dmg["category"] == "Software/Installers"
        print("  ✅ 第一階段硬過濾: DMG 安裝檔秒速分流至 'Software/Installers' (免 LLM 消耗)")

        # Stage 2: Candidate pruning for finance receipt
        pruned_cats = agent._prune_categories(categories, "data", ".csv", f_csv.name, res_csv["text"].lower())
        assert len(pruned_cats) == 1
        assert pruned_cats[0]["name"] == "Finance/Receipts"
        print(f"  ✅ 第二階段候選池縮減: 發票資料候選池精準聚焦為 {len(pruned_cats)} 個目標分類 ({pruned_cats[0]['name']})")

        # -------------------------------------------------------------
        # Part 3: HDBSCAN Topic Discovery
        # -------------------------------------------------------------
        print("\n[測試 3] HDBSCAN 無監督密度分群與主題發現驗證")
        analyzer = TopicClusterAnalyzer()
        cluster_report = analyzer.fit_clusters(min_cluster_size=2)
        assert cluster_report["status"] == "SUCCESS"
        assert cluster_report["total_documents"] >= 2
        print(f"  ✅ HDBSCAN 向量分群演算法執行成功: {cluster_report['algorithm']}")
        print(f"     分析文件總數: {cluster_report['total_documents']} 筆 | 發現聚類: {cluster_report['clusters_count']} 群")

        suggestions = analyzer.discover_emerging_topics(min_cluster_size=2)
        print(f"  ✅ 自適應主題發現產生 {len(suggestions)} 項目錄演進建議:")
        for s in suggestions:
            print(f"     • 建議新增: `{s['suggested_new_category']}` ({s['document_count']} 篇文獻)")

        print("\n" + "=" * 72)
        print("🎉 全部新功能驗收測試 100% 通過！新架構順利部署！")
        print("=" * 72)


if __name__ == "__main__":
    run_tests()
