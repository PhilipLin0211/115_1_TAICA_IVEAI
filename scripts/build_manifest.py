#!/usr/bin/env python3
"""
自動掃描 115_1_TAICA_IVEAI 儲存庫內的作業資料夾、PPT/ 講義與 notes/ Markdown 筆記，
更新 data.json 並完整保留既有項目的自訂 displayName、videos 與描述欄位。
"""

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data.json"
PPT_DIR = ROOT_DIR / "PPT"
NOTES_DIR = ROOT_DIR / "notes"

IGNORED_DIRS = {".git", ".github", "PPT", "notes", "scripts", "node_modules"}


def load_existing_data() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "meta": {
            "course": "115-1 TAICA_IVEAI 智慧虛擬實境與人工智慧",
            "student": "林宸平 (M11552010)",
            "repoUrl": "https://github.com/PhilipLin0211/115_1_TAICA_IVEAI",
        },
        "assignments": [],
        "materials": [],
        "notes": [],
        "videos": [],
    }


def extract_md_title(md_path: Path) -> str:
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
    except OSError:
        pass
    return md_path.stem.replace("_", " ")


def scan_materials(existing_materials: list) -> list:
    existing_by_path = {m.get("path"): m for m in existing_materials}
    materials = []
    if not PPT_DIR.exists():
        return materials

    for pdf in sorted(PPT_DIR.glob("*.pdf")):
        rel_path = f"./PPT/{pdf.name}"
        size_mb = f"{pdf.stat().st_size / (1024 * 1024):.1f} MB"
        if rel_path in existing_by_path:
            item = dict(existing_by_path[rel_path])
            item["sizeMB"] = size_mb
        else:
            clean_title = re.sub(r"\(.*?\)", "", pdf.stem).strip()
            item = {
                "id": f"ppt-{len(materials) + 1:02d}",
                "title": clean_title,
                "path": rel_path,
                "sizeMB": size_mb,
            }
        materials.append(item)
    return materials


def scan_notes(existing_notes: list) -> list:
    existing_by_path = {n.get("path"): n for n in existing_notes}
    notes = []
    if not NOTES_DIR.exists():
        return notes

    for md in sorted(NOTES_DIR.glob("*.md")):
        rel_path = f"./notes/{md.name}"
        title = extract_md_title(md)
        if rel_path in existing_by_path:
            item = dict(existing_by_path[rel_path])
            item["title"] = title
        else:
            item = {
                "id": f"note-{md.stem.lower()}",
                "title": title,
                "path": rel_path,
            }
        notes.append(item)
    return notes


def scan_assignments(existing_assignments: list) -> list:
    assignments = []
    seen_folders = set()

    for item in existing_assignments:
        folder_path = item.get("folderPath", "")
        if folder_path and (ROOT_DIR / folder_path).is_dir():
            assignments.append(item)
            seen_folders.add(folder_path)

    for entry in sorted(ROOT_DIR.iterdir()):
        if not entry.is_dir() or entry.name in IGNORED_DIRS or entry.name.startswith("."):
            continue
        if entry.name in seen_folders:
            continue
        if not (entry / "index.html").exists():
            continue

        meta_file = entry / "project.meta.json"
        if meta_file.exists():
            with open(meta_file, "r", encoding="utf-8") as mf:
                new_item = json.load(mf)
            new_item.setdefault("folderPath", entry.name)
            new_item.setdefault("entryFile", "index.html")
        else:
            new_item = {
                "id": re.sub(r"[^a-zA-Z0-9]+", "-", entry.name).strip("-").lower() or f"hw-{len(assignments)+1}",
                "badge": "課程作業 • 已發布",
                "displayName": entry.name,
                "subtitle": "自動偵測新增的課程專案資料夾",
                "folderPath": entry.name,
                "entryFile": "index.html",
                "description": f"自動從資料夾 `{entry.name}` 偵測並載入的靜態網頁成果。",
                "tags": ["Auto-Detected", "HTML5"],
                "links": [
                    {
                        "label": "線上體驗 (Live Demo)",
                        "url": f"./{entry.name}/index.html",
                        "type": "primary",
                    }
                ],
            }
        assignments.append(new_item)

    return assignments


def main():
    data = load_existing_data()
    tz_tw = timezone(timedelta(hours=8))
    data.setdefault("meta", {})
    data["meta"]["lastUpdated"] = datetime.now(tz_tw).strftime("%Y-%m-%d %H:%M CST")
    data["assignments"] = scan_assignments(data.get("assignments", []))
    data["materials"] = scan_materials(data.get("materials", []))
    data["notes"] = scan_notes(data.get("notes", []))
    data.setdefault("videos", [])

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {DATA_FILE}: {len(data['assignments'])} assignments, {len(data['materials'])} materials, {len(data['notes'])} notes.")


if __name__ == "__main__":
    main()