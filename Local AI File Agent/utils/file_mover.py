"""
File mover module with strict permission boundaries and collision-avoidance safety.
Enforces the Principle of Least Privilege: The Agent ONLY has 'MOVE' permission.
Any DELETE, OVERWRITE, or EXECUTE operations are strictly prohibited.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Tuple

# Strict Permission Definition
ALLOWED_PERMISSIONS = {"MOVE"}
FORBIDDEN_OPERATIONS = {"DELETE", "OVERWRITE", "MODIFY", "EXECUTE", "TRUNCATE"}


class PermissionDeniedError(PermissionError):
    """Raised when an unauthorized file system operation is attempted."""
    pass


def validate_agent_permission(requested_action: str):
    """
    Validates that the requested action strictly adheres to the MOVE-only policy.
    """
    act = (requested_action or "").upper().strip()
    if act not in ALLOWED_PERMISSIONS:
        raise PermissionDeniedError(
            f"🚫 [Permission Denied] Agent is strictly restricted to MOVE-only permission! "
            f"Requested action '{requested_action}' is unauthorized."
        )


def safe_move_file(
    source: Path,
    destination_dir: Path,
    target_filename: str = None,
    dry_run: bool = False,
    requested_action: str = "MOVE"
) -> Tuple[bool, Path]:
    """
    Safely move source to destination_dir with permission validation and collision avoidance.
    Enforces MOVE-ONLY permission.
    """
    # 1. Permission Gatekeeper
    validate_agent_permission(requested_action)

    src_path = Path(source).resolve()
    dest_dir = Path(destination_dir).expanduser().resolve()

    if not src_path.exists():
        print(f"❌ [File Mover Error] Source file does not exist: {src_path}")
        return False, src_path

    # Security: Ensure we are not moving system-critical files
    if src_path.is_symlink() or src_path.name.startswith("."):
        print(f"⚠️ [Security Warning] Bypassing hidden or symlink file: {src_path.name}")
        return False, src_path

    # Determine desired filename
    final_name = target_filename if target_filename else src_path.name

    # Ensure valid extension matches source
    if Path(final_name).suffix == "" and src_path.suffix:
        final_name += src_path.suffix

    dest_path = dest_dir / final_name

    # 2. Collision avoidance (NEVER overwrite existing files!)
    if dest_path.exists():
        stem = Path(final_name).stem
        ext = Path(final_name).suffix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_name = f"{stem}_{timestamp}{ext}"
        dest_path = dest_dir / final_name

    if dry_run:
        print(f"🔍 [DRY-RUN MOVE] Permission Verified: MOVE | '{src_path.name}' -> '{dest_path}'")
        return True, dest_path

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        # Execute pure atomic move
        shutil.move(str(src_path), str(dest_path))
        print(f"✅ [File Moved] Permission Authorized (MOVE-ONLY): {dest_path}")
        return True, dest_path
    except Exception as e:
        print(f"❌ [File Mover Exception] Failed to move {src_path} -> {dest_path}: {e}")
        return False, src_path
