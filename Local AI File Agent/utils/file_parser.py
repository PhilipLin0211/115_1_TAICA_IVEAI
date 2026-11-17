"""
Unified In-Memory Virtual Markdown Parser for Local AI File Agent.
Transforms all file types (PDF, Word, Code, CSV, Archives, Media, Binaries) 
into structured Markdown text streams purely in RAM.
Zero disk writes, zero leftover .md files, original files remain 100% untouched.
"""

import os
import io
import csv
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, Any, List

# Optional dependencies with graceful fallbacks
try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

try:
    import pymupdf4llm
except ImportError:
    pymupdf4llm = None

try:
    import docx
except ImportError:
    docx = None


class UnifiedInMemoryMarkdownConverter:
    """
    In-memory document-to-Markdown engine.
    Ensures LLM receives clean, structured headings, lists, and tables.
    """

    @classmethod
    def convert(cls, file_path: Path, max_chars: int = 4000) -> Dict[str, Any]:
        path = Path(file_path)
        ext = path.suffix.lower()
        file_size = path.stat().st_size if path.exists() else 0

        result = {
            "file_name": path.name,
            "file_size": file_size,
            "extension": ext,
            "text": "",
            "in_memory_markdown": "",
            "file_type_family": cls._detect_family(ext),
            "is_binary": False,
            "pages": 1
        }

        if not path.exists():
            result["text"] = f"# Error: File Not Found\n- Path: `{path}`"
            result["in_memory_markdown"] = result["text"]
            return result

        if file_size == 0:
            result["text"] = f"[Empty 0-byte file]"
            result["in_memory_markdown"] = f"# 0-Byte File\n- Filename: `{path.name}`\n- Status: Empty file (0 bytes)."
            return result

        family = result["file_type_family"]

        # 1. PDF Documents
        if ext == ".pdf":
            md_content, pages = cls._parse_pdf(path, max_chars)
            result["pages"] = pages
            result["text"] = md_content
            result["in_memory_markdown"] = md_content

        # 2. Microsoft Word (.docx)
        elif ext == ".docx":
            md_content = cls._parse_docx(path, max_chars)
            result["text"] = md_content
            result["in_memory_markdown"] = md_content

        # 3. Spreadsheets & Tabular Data (.csv, .tsv)
        elif ext in [".csv", ".tsv"]:
            md_content = cls._parse_tabular(path, ext, max_chars)
            result["text"] = md_content
            result["in_memory_markdown"] = md_content

        # 4. Archives (.zip, .tar, .gz)
        elif ext in [".zip", ".tar", ".gz", ".tgz"]:
            md_content = cls._parse_archive(path, ext)
            result["text"] = md_content
            result["in_memory_markdown"] = md_content
            result["is_binary"] = True

        # 5. Source Code & Markup & Configurations
        elif family == "code" or ext in [".txt", ".md", ".json", ".yaml", ".yml", ".html", ".css", ".xml", ".sh", ".sql"]:
            md_content = cls._parse_code_or_text(path, ext, max_chars)
            result["text"] = md_content
            result["in_memory_markdown"] = md_content

        # 6. Software Installers & Packages (.dmg, .pkg, .exe, .iso, .app)
        elif family == "installer":
            md_content = cls._format_installer_card(path, ext, file_size)
            result["text"] = md_content
            result["in_memory_markdown"] = md_content
            result["is_binary"] = True

        # 7. Media & Video / Audio (.mp4, .mov, .mp3, .wav, .png, .jpg)
        elif family == "media":
            md_content = cls._format_media_card(path, ext, file_size)
            result["text"] = md_content
            result["in_memory_markdown"] = md_content
            result["is_binary"] = True

        # 8. Generic Binary fallback
        else:
            result["is_binary"] = True
            md_content = (
                f"# Binary Asset: `{path.name}`\n\n"
                f"- **Extension**: `{ext}`\n"
                f"- **Size**: {file_size:,} bytes\n"
                f"- **Note**: Unparsed binary payload. Classification relies on filename and extension semantics."
            )
            result["text"] = md_content
            result["in_memory_markdown"] = md_content

        return result

    @classmethod
    def _detect_family(cls, ext: str) -> str:
        if ext in [".pdf", ".docx", ".doc", ".pptx", ".ppt", ".odt"]:
            return "document"
        if ext in [".dmg", ".pkg", ".exe", ".iso", ".msi", ".deb", ".rpm"]:
            return "installer"
        if ext in [".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav", ".flac", ".png", ".jpg", ".jpeg", ".gif", ".webp"]:
            return "media"
        if ext in [".zip", ".tar", ".gz", ".tgz", ".7z", ".rar"]:
            return "archive"
        if ext in [".csv", ".tsv", ".xlsx", ".xls"]:
            return "data"
        if ext in [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".rs", ".go", ".rb", ".php", ".sh", ".sql"]:
            return "code"
        return "general"

    @classmethod
    def _parse_pdf(cls, path: Path, max_chars: int) -> (str, int):
        pages_count = 1
        if fitz is not None:
            try:
                doc = fitz.open(path)
                pages_count = len(doc)
                
                # Try pymupdf4llm if installed for beautiful structural markdown
                if pymupdf4llm is not None:
                    try:
                        # Extract first 3 pages and last page if long
                        page_indices = list(range(min(3, pages_count)))
                        if pages_count > 4:
                            page_indices.append(pages_count - 1)
                        md_text = pymupdf4llm.to_markdown(doc, pages=page_indices)
                        if md_text and len(md_text.strip()) > 50:
                            return f"# PDF Document: `{path.name}` (Pages: {pages_count})\n\n{md_text[:max_chars]}", pages_count
                    except Exception:
                        pass

                # Fallback to structural block extraction via fitz
                blocks_text = []
                num_front = min(3, pages_count)
                for i in range(num_front):
                    blocks = doc[i].get_text("blocks")
                    for b in blocks:
                        text = b[4].strip()
                        if text:
                            # Heuristic: Short capitalized or bold text -> heading
                            if len(text) < 80 and not text.endswith("."):
                                blocks_text.append(f"\n### {text}\n")
                            else:
                                blocks_text.append(text)

                if pages_count > 4:
                    blocks_text.append("\n\n## --- [Last Page / Conclusion] ---\n")
                    last_blocks = doc[-1].get_text("blocks")
                    for b in last_blocks:
                        text = b[4].strip()
                        if text:
                            blocks_text.append(text)

                full_md = f"# PDF Document: `{path.name}` (Total Pages: {pages_count})\n\n" + "\n\n".join(blocks_text)
                return full_md[:max_chars], pages_count

            except Exception as e:
                return f"# PDF Document: `{path.name}`\n[Notice: Failed to parse PDF structure: {e}]", pages_count
        else:
            return f"# PDF Document: `{path.name}`\n[PyMuPDF not installed, using filename semantics only]", pages_count

    @classmethod
    def _parse_docx(cls, path: Path, max_chars: int) -> str:
        if docx is not None:
            try:
                doc = docx.Document(path)
                md_lines = [f"# Word Document: `{path.name}`\n"]

                # 1. Parse paragraphs with heading levels
                for p in doc.paragraphs:
                    text = p.text.strip()
                    if not text:
                        continue
                    style_name = p.style.name.lower() if p.style else ""
                    if "heading 1" in style_name:
                        md_lines.append(f"\n# {text}\n")
                    elif "heading 2" in style_name:
                        md_lines.append(f"\n## {text}\n")
                    elif "heading 3" in style_name:
                        md_lines.append(f"\n### {text}\n")
                    elif "bullet" in style_name or "list" in style_name:
                        md_lines.append(f"- {text}")
                    else:
                        md_lines.append(text)

                # 2. Parse first table if present
                if doc.tables:
                    md_lines.append("\n\n### Document Tables (Preview)\n")
                    table = doc.tables[0]
                    for r_idx, row in enumerate(table.rows[:6]):
                        row_vals = [c.text.strip().replace("\n", " ") for c in row.cells]
                        md_lines.append("| " + " | ".join(row_vals) + " |")
                        if r_idx == 0:
                            md_lines.append("| " + " | ".join(["---"] * len(row_vals)) + " |")

                return "\n".join(md_lines)[:max_chars]
            except Exception as e:
                return f"# Word Document: `{path.name}`\n[Notice: Failed to parse DOCX: {e}]"
        else:
            return f"# Word Document: `{path.name}`\n[python-docx not installed, relying on filename semantics]"

    @classmethod
    def _parse_tabular(cls, path: Path, ext: str, max_chars: int) -> str:
        try:
            delimiter = "\t" if ext == ".tsv" else ","
            md_lines = [f"# Tabular Data: `{path.name}`\n"]
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f, delimiter=delimiter)
                rows = []
                for idx, row in enumerate(reader):
                    if idx >= 10:
                        break
                    rows.append(row)

                if rows:
                    header = [c.strip() for c in rows[0]]
                    md_lines.append("| " + " | ".join(header) + " |")
                    md_lines.append("| " + " | ".join(["---"] * len(header)) + " |")
                    for row in rows[1:]:
                        md_lines.append("| " + " | ".join(c.strip() for c in row) + " |")

            return "\n".join(md_lines)[:max_chars]
        except Exception as e:
            return f"# Tabular Data: `{path.name}`\n[Notice: Tabular parse error: {e}]"

    @classmethod
    def _parse_archive(cls, path: Path, ext: str) -> str:
        md_lines = [f"# Archive Package: `{path.name}`\n"]
        try:
            if ext == ".zip":
                with zipfile.ZipFile(path, "r") as z:
                    file_list = z.namelist()
                    md_lines.append(f"- **Total Contained Files**: {len(file_list)}")
                    md_lines.append("- **Directory Tree Preview**:")
                    for f in file_list[:25]:
                        md_lines.append(f"  - `{f}`")
                    if len(file_list) > 25:
                        md_lines.append(f"  - `... and {len(file_list) - 25} more items`")
            elif ext in [".tar", ".gz", ".tgz"]:
                with tarfile.open(path, "r:*") as t:
                    names = t.getnames()
                    md_lines.append(f"- **Total Contained Files**: {len(names)}")
                    md_lines.append("- **Directory Tree Preview**:")
                    for n in names[:25]:
                        md_lines.append(f"  - `{n}`")
                    if len(names) > 25:
                        md_lines.append(f"  - `... and {len(names) - 25} more items`")
            return "\n".join(md_lines)
        except Exception as e:
            return f"# Archive Package: `{path.name}`\n[Encrypted or compressed archive: {e}]"

    @classmethod
    def _parse_code_or_text(cls, path: Path, ext: str, max_chars: int) -> str:
        lang_map = {
            ".py": "python", ".js": "javascript", ".ts": "typescript",
            ".html": "html", ".css": "css", ".json": "json", ".yaml": "yaml",
            ".yml": "yaml", ".sh": "bash", ".sql": "sql", ".md": "markdown"
        }
        lang = lang_map.get(ext, "")
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(max_chars)
            
            if ext == ".md":
                return f"# Markdown Document: `{path.name}`\n\n{content}"
            elif lang:
                return f"# Source Code File: `{path.name}`\n```{lang}\n{content}\n```"
            else:
                return f"# Plain Text Document: `{path.name}`\n\n{content}"
        except Exception as e:
            return f"# Text Document: `{path.name}`\n[Read error: {e}]"

    @classmethod
    def _format_installer_card(cls, path: Path, ext: str, size: int) -> str:
        size_mb = size / (1024 * 1024)
        return (
            f"# Software Installer: `{path.name}`\n\n"
            f"- **Package Type**: macOS / OS Application Installer ({ext})\n"
            f"- **File Size**: {size_mb:.1f} MB ({size:,} bytes)\n"
            f"- **Classification Policy**: Direct route to `Software/Installers`\n"
            f"- **Execution Safety**: Execution disabled (MOVE-ONLY boundary enforced)"
        )

    @classmethod
    def _format_media_card(cls, path: Path, ext: str, size: int) -> str:
        size_mb = size / (1024 * 1024)
        media_type = "Video File" if ext in [".mp4", ".mov", ".avi", ".mkv"] else "Audio/Image Asset"
        return (
            f"# Multimedia Asset: `{path.name}`\n\n"
            f"- **Asset Category**: {media_type} ({ext})\n"
            f"- **File Size**: {size_mb:.1f} MB ({size:,} bytes)\n"
            f"- **Classification Policy**: Direct route to `Media/`\n"
            f"- **Content Hint**: Binary audiovisual stream"
        )


def extract_text_from_file(file_path: Path, max_chars: int = 4000) -> Dict[str, Any]:
    """
    Unified public API. Converts any file to an in-memory virtual Markdown dictionary.
    Guarantees zero physical disk writes and complete preservation of the original file.
    """
    return UnifiedInMemoryMarkdownConverter.convert(file_path, max_chars=max_chars)
