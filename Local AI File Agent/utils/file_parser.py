"""
File parser module for Local AI File Agent.
Extracts text from PDF, DOCX, TXT, MD, and code files with safety truncation.
"""

import os
from pathlib import Path
from typing import Dict, Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import docx
except ImportError:
    docx = None


def extract_text_from_file(file_path: Path, max_chars: int = 4000) -> Dict[str, Any]:
    """
    Extract text content and basic metadata from a file.
    Safely truncates content to avoid token overflow in LLM prompts.
    """
    path = Path(file_path)
    ext = path.suffix.lower()
    file_size = path.stat().st_size if path.exists() else 0

    result = {
        "file_name": path.name,
        "file_size": file_size,
        "extension": ext,
        "text": "",
        "is_binary": False,
        "pages": 1
    }

    if not path.exists():
        result["text"] = f"[Error] File not found: {path}"
        return result

    if file_size == 0:
        result["text"] = "[Empty 0-byte file]"
        return result

    # 1. PDF extraction
    if ext == ".pdf":
        if fitz is not None:
            try:
                doc = fitz.open(path)
                result["pages"] = len(doc)
                extracted_pages = []

                # Extract first 3 pages (Title, Abstract, Intro)
                num_front = min(3, len(doc))
                for i in range(num_front):
                    extracted_pages.append(doc[i].get_text("text"))

                # Extract last page (Conclusion) if more than 4 pages
                if len(doc) > 4:
                    extracted_pages.append("\n--- [Last Page / Conclusion] ---\n")
                    extracted_pages.append(doc[-1].get_text("text"))

                raw_text = "\n".join(extracted_pages).strip()
                result["text"] = raw_text[:max_chars]
            except Exception as e:
                result["text"] = f"[Error parsing PDF: {e}]"
        else:
            result["text"] = "[PyMuPDF not installed, using filename only]"

    # 2. Word (.docx) extraction
    elif ext == ".docx":
        if docx is not None:
            try:
                doc = docx.Document(path)
                paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                raw_text = "\n".join(paragraphs)
                result["text"] = raw_text[:max_chars]
            except Exception as e:
                result["text"] = f"[Error parsing DOCX: {e}]"
        else:
            result["text"] = "[python-docx not installed, using filename only]"

    # 3. Plain text / Markdown / Source code
    elif ext in [".txt", ".md", ".json", ".py", ".html", ".js", ".css", ".yaml", ".yml", ".sh"]:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                raw_text = f.read(max_chars)
                result["text"] = raw_text
        except Exception as e:
            result["text"] = f"[Error reading text file: {e}]"

    # 4. Binary or media file
    else:
        result["is_binary"] = True
        result["text"] = f"[Binary/Media file: {ext}, size: {file_size} bytes. Relying on filename and metadata]"

    return result

