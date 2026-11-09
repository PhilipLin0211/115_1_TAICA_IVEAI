"""
File mover module with collision-avoidance and dry-run safety.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Tuple


def safe_move_file(source: Path, destination_dir: Path, target_filename: str = None, dry_run: bool = False) -> Tuple[bool, Path]:
    """
    Safely move source to destination_dir with collision avoidance.
    If destination file exists, appends timestamp.
    """
    src_path = Path(source)
    dest_dir = Path(destination_dir).expanduser()

    if not src_path.exists():
        print(f"❌ [File Mover Error] Source file does not exist: {src_path}")
        return False, src_path

    # Determine desired filename
    final_name = target_filename if target_filename else src_path.name

    # Ensure valid extension
    if Path(final_name).suffix == "" and src_path.suffix:
        final_name += src_path.suffix

    dest_path = dest_dir / final_name

    # Collision avoidance
    if dest_path.exists():
        stem = Path(final_name).stem
        ext = Path(final_name).suffix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_name = f"{stem}_{timestamp}{ext}"
        dest_path = dest_dir / final_name

    if dry_run:
        print(f"🔍 [DRY-RUN MOVE] Would move: '{src_path.name}' -> '{dest_path}'")
        return True, dest_path

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dest_path))
        print(f"✅ [File Moved] Successfully moved to: {dest_path}")
        return True, dest_path
    except Exception as e:
        print(f"❌ [File Mover Exception] Failed to move {src_path} -> {dest_path}: {e}")
        return False, src_path

