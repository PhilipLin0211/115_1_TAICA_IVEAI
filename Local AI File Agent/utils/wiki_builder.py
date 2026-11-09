"""
Obsidian Wiki Builder module.
Generates structured Markdown reading notes, double-links, and maintains index.md and log.md.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


def create_obsidian_note(
    vault_dir: Path,
    relative_category: str,
    file_info: Dict[str, Any],
    decision: Dict[str, Any],
    dry_run: bool = False
) -> Path:
    """
    Generate an Obsidian Markdown note for the organized file and update index.md.
    """
    vault = Path(vault_dir).expanduser()
    target_dir = vault / relative_category
    note_title = decision.get("wiki_title") or Path(decision.get("sanitized_name", "note")).stem
    clean_title = "".join(c for c in note_title if c not in r'\/:*?"<>|').strip()
    note_path = target_dir / f"{clean_title}.md"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Format tags
    tags = decision.get("tags", ["Untagged"])
    tag_str = " ".join(f"#{t.replace('#', '')}" for t in tags)

    # Format double links
    links = decision.get("double_links", [])
    link_str = " ".join(f"[[{l.strip('[]')}]]" for l in links)

    content = f"""---
title: "{clean_title}"
date: {today_str}
created: {now_str}
original_file: "{file_info.get('file_name', '')}"
category: "{relative_category}"
tags: [{', '.join(f'"{t.replace("#", "")}"' for t in tags)}]
---

# 📖 {clean_title}

> 📂 **歸檔位置**：`{relative_category}/{decision.get('sanitized_name', '')}`  
> 🏷️ **主題標籤**：{tag_str}  
> 🔗 **關聯概念**：{link_str if link_str else "無"}

---

## 📌 核心重點精要
{decision.get('summary', '尚無摘要內容。')}

## 💡 AI 思考與推薦行動
* **分類理由**：{decision.get('reasoning', '依據內容關鍵字與向量語意相似度分類。')}
* **推薦行動**：{decision.get('action_recommendation', '閱讀完畢後歸檔至長期封存庫。')}

---
*自動生成自 Local AI File Agent (TAICA_IVEAI Final Project)*
"""

    if dry_run:
        print(f"🔍 [DRY-RUN WIKI] Would generate note at: {note_path}")
        return note_path

    target_dir.mkdir(parents=True, exist_ok=True)
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Update index.md and log.md in Vault root
    _append_to_index(vault, clean_title, relative_category, tags)
    _append_to_log(vault, file_info.get('file_name', ''), relative_category, clean_title)

    print(f"📝 [Wiki Note Created] {note_path}")
    return note_path


def _append_to_index(vault: Path, title: str, category: str, tags: List[str]):
    """Append the new entry to index.md"""
    index_file = vault / "index.md"
    entry = f"- [[{title}]] `({category})` {' '.join('#' + t.replace('#', '') for t in tags)}\n"

    if not index_file.exists():
        header = "# 🧠 個人第二大腦知識總索引 (LLMWiki Index)\n\n> 本文件由 Local AI File Agent 自動維護。\n\n## 📚 已歸檔文獻與筆記列表\n"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(header + entry)
    else:
        with open(index_file, "a", encoding="utf-8") as f:
            f.write(entry)


def _append_to_log(vault: Path, original: str, category: str, note_title: str):
    """Append event to log.md"""
    log_file = vault / "log.md"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"| {now_str} | `{original}` | `{category}` | [[{note_title}]] |\n"

    if not log_file.exists():
        header = "# 📜 Local File Agent 操作審計日誌 (Audit Log)\n\n| 時間 | 原始檔案 | 分類目錄 | 生成筆記 |\n| :--- | :--- | :--- | :--- |\n"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(header + entry)
    else:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)

