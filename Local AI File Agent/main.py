#!/usr/bin/env python3
"""
Local AI File Agent - Main Entry Point.
Listens to ~/Downloads, runs RAG-based classification, and builds Obsidian LLMWiki.
"""

import sys
import os
import time
import argparse
from pathlib import Path
import yaml

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.file_parser import extract_text_from_file
from utils.file_mover import safe_move_file
from utils.wiki_builder import create_obsidian_note
from utils.audit_logger import AuditLogger
from agent.llm_caller import OllamaAgentCaller
from agent.rag_engine import LocalRagEngine


class DownloadFolderHandler(FileSystemEventHandler):
    def __init__(self, config: dict, dry_run: bool = False):
        super().__init__()
        self.config = config
        self.dry_run = dry_run
        self.ignored_exts = set(config.get("ignored_extensions", [".crdownload", ".tmp", ".part"]))
        self.vault_dir = Path(config.get("vault_directory", "~/Documents/Obsidian_Vault")).expanduser()
        self.watch_dir = Path(config.get("watch_directory", "~/Downloads")).expanduser()
        self.categories = config.get("categories", [])
        
        # Initialize modules
        self.logger = AuditLogger(vault_dir=self.vault_dir)

        ollama_cfg = config.get("ollama", {})
        self.agent = OllamaAgentCaller(
            host=ollama_cfg.get("host", "http://127.0.0.1:11434"),
            model=ollama_cfg.get("llm_model", "qwen2.5-coder:7b"),
            timeout=ollama_cfg.get("timeout_seconds", 60)
        )
        
        rag_cfg = config.get("vector_store", {})
        self.rag = LocalRagEngine(
            host=ollama_cfg.get("host", "http://127.0.0.1:11434"),
            embed_model=ollama_cfg.get("embed_model", "nomic-embed-text"),
            index_path=rag_cfg.get("index_path", "./vector_store/faiss_index.bin"),
            metadata_path=rag_cfg.get("metadata_path", "./vector_store/metadata.json")
        )

    def on_created(self, event):
        if event.is_directory:
            return
        self.process_file(Path(event.src_path))

    def on_moved(self, event):
        if event.is_directory:
            return
        # Download completing often triggers rename from .crdownload to real name
        self.process_file(Path(event.dest_path))

    def process_file(self, file_path: Path):
        ext = file_path.suffix.lower()
        if ext in self.ignored_exts or file_path.name.startswith("."):
            return

        print(f"\n⚡ [Watchdog Event] Detected new file: {file_path.name}")
        
        # Debounce / File Lock check
        if not self._wait_until_stable(file_path):
            print(f"⚠️ [Skip] File still writing or inaccessible: {file_path.name}")
            return

        print(f"📄 [Step 1] Parsing content & metadata...")
        file_info = extract_text_from_file(file_path)

        print(f"🔍 [Step 2] Querying FAISS vector index (RAG)...")
        rag_context = self.rag.search_similar(file_info.get("text", "")[:1000], top_k=3)

        print(f"🧠 [Step 3] LLM Reasoning via Qwen 2.5 Coder 7B...")
        decision = self.agent.classify_and_reason(file_info, rag_context, self.categories)
        print(f"🎯 [Decision] Category: {decision.get('category')} | Name: {decision.get('sanitized_name')}")

        dest_dir = self.vault_dir / decision.get("category", "General/Inbox")
        action_requested = decision.get("action", "MOVE")
        print(f"📂 [Step 4] Requesting action: {action_requested} -> {dest_dir} (Dry-run: {self.dry_run})...")
        
        ok, final_path = safe_move_file(
            source=file_path,
            destination_dir=dest_dir,
            target_filename=decision.get("sanitized_name"),
            dry_run=self.dry_run,
            requested_action=action_requested
        )

        if ok:
            print(f"📝 [Step 5] Building Obsidian LLMWiki note & updating index.md...")
            create_obsidian_note(
                vault_dir=self.vault_dir,
                relative_category=decision.get("category", "General/Inbox"),
                file_info=file_info,
                decision=decision,
                dry_run=self.dry_run
            )

            print(f"📸 [Step 6] Recording audit history & directory snapshot...")
            self.logger.record_action(
                action=action_requested,
                source_path=file_path,
                destination_path=final_path,
                file_info=file_info,
                decision=decision,
                watch_dir=self.watch_dir,
                dry_run=self.dry_run
            )

            # Update FAISS Vector Store with this new knowledge
            if not self.dry_run:
                self.rag.add_document(
                    title=decision.get("wiki_title", file_info.get("file_name")),
                    category=decision.get("category"),
                    summary=decision.get("summary", "")
                )
                print(f"✨ [Done] Vector store updated. Ready for next download.\n")

    def _wait_until_stable(self, path: Path, timeout: float = 10.0) -> bool:
        """Wait until file size stops changing (download finished)."""
        if not path.exists():
            return False
        start = time.time()
        last_size = -1
        while time.time() - start < timeout:
            try:
                curr_size = path.stat().st_size
                if curr_size == last_size and curr_size > 0:
                    return True
                last_size = curr_size
            except Exception:
                pass
            time.sleep(1.0)
        return False


def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Local AI File Agent - Auto Sorting & RAG Wiki")
    parser.add_argument("--dry-run", action="store_true", help="Run without physically moving files or writing notes")
    parser.add_argument("--config", default="config.yaml", help="Path to configuration yaml")
    parser.add_argument("--watch", help="Override watch directory (default from config)")
    parser.add_argument("--vault", help="Override Obsidian vault directory")
    args = parser.parse_args()

    cfg_file = Path(args.config)
    if not cfg_file.exists():
        cfg_file = Path(__file__).parent / "config.yaml"

    config = load_config(str(cfg_file))
    if args.watch:
        config["watch_directory"] = args.watch
    if args.vault:
        config["vault_directory"] = args.vault

    watch_dir = Path(config.get("watch_directory", "~/Downloads")).expanduser()
    if not watch_dir.exists():
        print(f"Creating watch directory: {watch_dir}")
        watch_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("🧠 Local AI File Agent (TAICA_IVEAI Final Project)")
    print(f"👀 Monitoring: {watch_dir}")
    print(f"📚 Obsidian Vault: {Path(config.get('vault_directory')).expanduser()}")
    print(f"🛡️ Dry-Run Mode: {'ENABLED (Simulated)' if args.dry_run else 'OFF (Real Actions)'}")
    print("=" * 60)

    handler = DownloadFolderHandler(config, dry_run=args.dry_run)
    observer = Observer()
    observer.schedule(handler, str(watch_dir), recursive=False)
    observer.start()

    print("🚀 Agent daemon active. Press Ctrl+C to terminate.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping Observer...")
        observer.stop()
    observer.join()
    print("👋 Agent successfully stopped.")


if __name__ == "__main__":
    main()

