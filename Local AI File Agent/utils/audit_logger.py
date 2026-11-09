"""
Audit Logger & Directory Snapshot Module for Local AI File Agent.
Records every action taken by the Agent along with complete folder directory snapshots.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class AuditLogger:
    def __init__(self, log_dir: Path = None, vault_dir: Path = None):
        if log_dir is None:
            self.log_dir = Path(__file__).parent.parent / "history"
        else:
            self.log_dir = Path(log_dir)

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.json_log_path = self.log_dir / "audit_log.json"
        self.vault_dir = Path(vault_dir).expanduser() if vault_dir else None

    def get_directory_snapshot(self, directory: Path, max_depth: int = 2) -> Dict[str, Any]:
        """
        Takes a snapshot of a directory's file structure and file sizes.
        """
        dir_path = Path(directory).expanduser()
        if not dir_path.exists():
            return {"path": str(dir_path), "exists": False, "files": []}

        file_list = []
        try:
            for item in sorted(dir_path.rglob("*")):
                if item.is_file() and not item.name.startswith("."):
                    rel_path = item.relative_to(dir_path)
                    # Limit depth to keep snapshot compact
                    if len(rel_path.parts) <= max_depth:
                        file_list.append({
                            "relative_path": str(rel_path),
                            "size_bytes": item.stat().st_size,
                            "modified": datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        })
        except Exception as e:
            return {"path": str(dir_path), "error": str(e), "files": []}

        return {
            "path": str(dir_path),
            "total_files": len(file_list),
            "files": file_list
        }

    def record_action(
        self,
        action: str,
        source_path: Path,
        destination_path: Path,
        file_info: Dict[str, Any],
        decision: Dict[str, Any],
        watch_dir: Path = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Records an action entry with permission verification, metadata, and folder snapshots.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_iso = datetime.now().isoformat()

        target_dir = Path(destination_path).parent if destination_path else None
        target_snapshot = self.get_directory_snapshot(target_dir) if target_dir else {}
        watch_snapshot = self.get_directory_snapshot(watch_dir) if watch_dir else {}

        log_entry = {
            "id": f"act_{int(datetime.now().timestamp())}",
            "timestamp": now_str,
            "timestamp_iso": timestamp_iso,
            "action_executed": action,
            "permission_guard": {
                "allowed_scope": "MOVE_ONLY",
                "verified": (action == "MOVE"),
                "status": "PASSED" if action == "MOVE" else "REJECTED"
            },
            "source": {
                "file_name": file_info.get("file_name", ""),
                "size_bytes": file_info.get("file_size", 0),
                "extension": file_info.get("extension", "")
            },
            "destination": {
                "category": decision.get("category", ""),
                "sanitized_name": decision.get("sanitized_name", ""),
                "final_path": str(destination_path) if destination_path else ""
            },
            "decision_metadata": {
                "wiki_title": decision.get("wiki_title", ""),
                "tags": decision.get("tags", []),
                "double_links": decision.get("double_links", []),
                "reasoning": decision.get("reasoning", "")
            },
            "dry_run": dry_run,
            "folder_directory_snapshots": {
                "target_directory": target_snapshot,
                "watch_directory": watch_snapshot
            }
        }

        # 1. Update structured JSON log
        self._append_json_log(log_entry)

        # 2. Update Obsidian log.md if vault is configured
        if self.vault_dir and not dry_run:
            self._append_vault_log(log_entry)

        print(f"📜 [Audit Log Recorded] Action ID: {log_entry['id']} | Target files count: {target_snapshot.get('total_files', 0)}")
        return log_entry

    def _append_json_log(self, entry: Dict[str, Any]):
        """Persist to history/audit_log.json"""
        history = []
        if self.json_log_path.exists():
            try:
                with open(self.json_log_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = []

        history.append(entry)
        try:
            with open(self.json_log_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ [Audit Log Save Error] {e}")

    def _append_vault_log(self, entry: Dict[str, Any]):
        """Append to Obsidian Vault's log.md with directory snapshot summary"""
        log_md_path = self.vault_dir / "log.md"
        src_name = entry["source"]["file_name"]
        cat = entry["destination"]["category"]
        sanitized = entry["destination"]["sanitized_name"]
        file_count = entry["folder_directory_snapshots"]["target_directory"].get("total_files", 0)

        row = (
            f"| {entry['timestamp']} | `{src_name}` | `{cat}/{sanitized}` | "
            f"✅ MOVE | 目錄現有 {file_count} 檔案 |\n"
        )

        if not log_md_path.exists():
            header = (
                "# 📜 Local File Agent 操作審計與目錄記錄 (Audit & Directory Log)\n\n"
                "> 系統遵循【嚴格僅移動權限 (MOVE-ONLY)】，任何其他操作均受硬性阻擋。\n\n"
                "| 時間 | 原始檔案 | 搬移至目錄 | 權限狀態 | 目錄快照摘要 |\n"
                "| :--- | :--- | :--- | :--- | :--- |\n"
            )
            with open(log_md_path, "w", encoding="utf-8") as f:
                f.write(header + row)
        else:
            with open(log_md_path, "a", encoding="utf-8") as f:
                f.write(row)
