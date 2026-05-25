#!/usr/bin/env python3
"""
sync_feedback_rules.py — Đồng bộ quy tắc từ memory/feedback vào CLAUDE.md

Chức năng:
  1. Quét tất cả tệp tin markdown trong memory/ có type: feedback.
  2. Nếu feedback chưa được đồng bộ (synced_to_claudemd: false hoặc thiếu trường này),
     trích xuất nội dung quy tắc và định tuyến chúng đến đúng phần trong CLAUDE.md.
  3. Đánh dấu synced_to_claudemd: true sau khi chèn thành công.
  4. Hỗ trợ chế độ --dry-run để xem trước thay đổi.

Chạy: python3 scripts/sync_feedback_rules.py
      python3 scripts/sync_feedback_rules.py --dry-run
"""

import os
import re
import sys
import yaml
from datetime import datetime

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(VAULT_ROOT, "memory")
CLAUDE_MD_PATH = os.path.join(VAULT_ROOT, "CLAUDE.md")


def read_file(path):
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"  ⚠️  Không thể đọc {path}: {e}", file=sys.stderr)
        return ""


def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  ❌ Lỗi ghi {path}: {e}", file=sys.stderr)
        return False


def parse_frontmatter(content):
    """Parse YAML frontmatter trả về (dict, rest_of_content)."""
    fm_match = re.match(r"^---\n(.*?)\n---\n?", content, re.DOTALL)
    if not fm_match:
        return {}, content

    fm_text = fm_match.group(1)
    remaining = content[fm_match.end():]
    try:
        data = yaml.safe_load(fm_text)
        if isinstance(data, dict):
            return data, remaining
    except yaml.YAMLError:
        pass
    return {}, remaining


def get_feedback_notes():
    """Quét memory/ và trả về danh sách feedback notes chưa được đồng bộ vào CLAUDE.md."""
    if not os.path.isdir(MEMORY_DIR):
        print(f"⚠️  Không tìm thấy thư mục {MEMORY_DIR}")
        return []

    notes = []
    for f in os.listdir(MEMORY_DIR):
        if not f.endswith(".md") or f == "MEMORY.md":
            continue

        fpath = os.path.join(MEMORY_DIR, f)
        content = read_file(fpath)
        if not content:
            continue

        fm, body = parse_frontmatter(content)
        meta = fm.get("metadata", {})
        note_type = meta.get("type", "") if isinstance(meta, dict) else ""

        if note_type != "feedback":
            continue

        synced = fm.get("synced_to_claudemd", False)
        if synced:
            continue

        notes.append({
            "file": f,
            "path": fpath,
            "fm": fm,
            "body": body.strip(),
            "name": fm.get("name", f.replace(".md", "")),
            "description": fm.get("description", ""),
        })

    return notes


def route_target_section(body, description):
    """Xác định section mục tiêu trong CLAUDE.md dựa trên nội dung quy tắc."""
    text = (body + " " + description).lower()

    # Domain / Entity / DB rules -> Core Guardrails
    domain_keywords = [
        "domain", "entity", "value object", "invariant", "nestjs", "drizzle",
        "repository", "schema", "database", "domain event", "application",
        "infrastructure", "dto", "mapper", "pgschema", "pgtable",
    ]
    if any(k in text for k in domain_keywords):
        return "Core Guardrails (The Technical Constitution)"

    # Naming / convention rules -> BA & Ubiquitous Language
    naming_keywords = [
        "casing", "naming", "ubiquitous", "role", "prefix", "suffix",
        "organizationid", "userid", "employeeid", "contactid", "actorid",
        "bounded context", "tier", "symbol", "token", "di token",
    ]
    if any(k in text for k in naming_keywords):
        return "BA & Ubiquitous Language Protocol"

    # Rules about how to interact in chat -> AI Chat & Coding Protocols
    chat_keywords = [
        "chat", "protocol", "coding", "code", "edit", "snippet", "targeted",
        "refactor", "progress", "summarize", "summarization", "distill",
    ]
    if any(k in text for k in chat_keywords):
        return "AI Chat & Coding Protocols (HƯỚNG DẪN XỬ LÝ TRONG CHAT)"

    # Default to Core Guardrails
    return "Core Guardrails (The Technical Constitution)"


def format_rule_text(note):
    """Format nội dung quy tắc dưới dạng markdown danh sách."""
    name = note.get("name", "feedback-rule").replace("-", " ").title()
    desc = note.get("description", "")
    body = note.get("body", "")

    lines = []
    lines.append(f"*   **{desc}**")
    # Extract actionable items (numbered list items from body)
    for line in body.split("\n"):
        stripped = line.strip()

        # Skip empty lines, Why? and How to apply? sections
        if not stripped or stripped.startswith("**Why") or stripped.startswith("**How to"):
            continue

        # Include numbered list items or bold key points
        if stripped.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "- ")):
            lines.append(f"    *   {stripped}")
        # Include standalone bold phrases
        elif stripped.startswith("**") and stripped.endswith("**"):
            lines.append(f"    *   {stripped}")

    lines.append(f"    *   *Nguồn: memory/{note['file']}*\n")
    return "\n".join(lines)


def insert_into_claude_md(rule_text, section_name):
    """Chèn rule_text vào đúng section trong CLAUDE.md."""
    claude_content = read_file(CLAUDE_MD_PATH)
    if not claude_content:
        print(f"  ❌ Không thể đọc {CLAUDE_MD_PATH}")
        return False

    # Map section names to actual CLAUDE.md headers
    section_headers = {
        "Core Guardrails (The Technical Constitution)": "### 2. Core Guardrails (The Technical Constitution)",
        "BA & Ubiquitous Language Protocol": "## 📋 BA & Ubiquitous Language Protocol",
        "AI Chat & Coding Protocols (HƯỚNG DẪN XỬ LÝ TRONG CHAT)": "## AI Chat & Coding Protocols (HƯỚNG DẪN XỬ LÝ TRONG CHAT)",
    }

    header = section_headers.get(section_name)
    if not header:
        print(f"  ⚠️  Không tìm thấy section '{section_name}' trong CLAUDE.md, mặc định vào cuối file.")
        claude_content += f"\n{rule_text}\n"
        return write_file(CLAUDE_MD_PATH, claude_content)

    # Find the header and insert after the last item in that section
    if header not in claude_content:
        # Fallback: find the nearest parent header
        print(f"  ⚠️  Header '{header}' không tìm thấy, thêm vào cuối file.")
        claude_content += f"\n{rule_text}\n"
        return write_file(CLAUDE_MD_PATH, claude_content)

    # Insert rule_text before the NEXT header of same or higher level
    # Determine header level (## or ###)
    h_level = header.count("#")
    # Pattern to match any header of same or higher level
    next_header_pattern = re.compile(rf"^#{{1,{h_level}}}\s", re.MULTILINE)

    header_start = claude_content.index(header)
    search_start = header_start + len(header)

    next_match = next_header_pattern.search(claude_content, search_start)
    insert_pos = next_match.start() if next_match else len(claude_content)

    # Add a newline before insertion if not at end
    prefix = "\n" if insert_pos < len(claude_content) else "\n\n"
    new_content = claude_content[:insert_pos] + prefix + rule_text + claude_content[insert_pos:]

    return write_file(CLAUDE_MD_PATH, new_content)


def mark_synced(note_path, frontmatter, body):
    """Đánh dấu file feedback là đã được đồng bộ. Cập nhật frontmatter với synced_to_claudemd: true."""
    frontmatter["synced_to_claudemd"] = True
    frontmatter["synced_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Reconstruct file: frontmatter + body
    new_fm = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False).strip()
    new_content = f"---\n{new_fm}\n---\n\n{body}\n"
    return write_file(note_path, new_content)


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("  🔄 ĐỒNG BỘ FEEDBACK VÀO CLAUDE.md (SYNC FEEDBACK RULES)")
    if dry_run:
        print("  📝 CHẾ ĐỘ THỬ NGHIỆM (DRY RUN) — không ghi thay đổi")
    print("=" * 60)

    notes = get_feedback_notes()
    if not notes:
        print("\n✅ Không có feedback mới cần đồng bộ.")
        return

    print(f"\n📋 Phát hiện {len(notes)} feedback chưa được đồng bộ:")
    for note in notes:
        print(f"   - {note['file']}: {note['description'][:80]}")

    if dry_run:
        print("\n📝 === NỘI DUNG SẼ ĐƯỢC ĐỒNG BỘ (DRY RUN) ===")
        for note in notes:
            section = route_target_section(note["body"], note["description"])
            print(f"\n--- {note['file']} -> [{section}] ---")
            print(format_rule_text(note)[:500])
        print("\n✅ Dry run hoàn tất. Không có thay đổi nào được ghi.")
        return

    success_count = 0
    for note in notes:
        print(f"\n{'-' * 50}")
        print(f"📄 Đang xử lý: {note['file']}")

        section = route_target_section(note["body"], note["description"])
        print(f"   🎯 Định tuyến đến section: {section}")

        rule_text = format_rule_text(note)
        if not rule_text.strip():
            print(f"   ⚠️  Không có quy tắc nào để trích xuất, bỏ qua.")
            continue

        inserted = insert_into_claude_md(rule_text, section)
        if not inserted:
            print(f"   ❌ Không thể chèn quy tắc vào CLAUDE.md")
            continue

        marked = mark_synced(note["path"], note["fm"], note["body"])
        if not marked:
            print(f"   ⚠️  Đã chèn vào CLAUDE.md nhưng không thể đánh dấu synced trong {note['file']}")
            continue

        print(f"   ✅ Đã đồng bộ {note['file']} vào CLAUDE.md thành công!")
        success_count += 1

    print(f"\n{'=' * 60}")
    print(f"  🎉 Đã đồng bộ {success_count}/{len(notes)} feedback vào CLAUDE.md thành công!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
