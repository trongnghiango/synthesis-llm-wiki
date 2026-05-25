#!/usr/bin/env python3
"""
audit_vault.py — Bộ Kiểm toán Toàn diện Obsidian Vault STAX Wiki.

Kiểm tra:
1. Liên kết hỏng (Broken Links) — cả [[Wiki Links]] và [Markdown](links).
2. Tính di động (Portability) — cấm đường dẫn tuyệt đối hoặc ../ trong vault.
3. Tính nhất quán phân cấp (Hierarchical Graph Audit) — Frontmatter parent/depends_on/source_note.

Chạy: python3 scripts/audit_vault.py
"""

import os
import re
import sys
import yaml
from collections import defaultdict

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories to scan for audits (except Templates)
SCAN_DIRS = [
    "0-Inbox", "1-Journal", "2-Processed", "3-Distilled",
    "02_atomic_nodes", "03_neural_map",
]

# Directories to SKIP — templates, git, hidden, binary
SKIP_DIRS = {"Templates", ".git", ".obsidian", "__pycache__", ".claude"}

# Whitelisted external domains (these are valid external links)
EXTERNAL_DOMAIN_ALLOWLIST = {
    "https://", "http://", "ftp://",
    "mailto:", "#", "tel:",
}

INCLUDE_EXTENSIONS = {".md", ".csv", ".json", ".yaml", ".yml", ".txt", ".env"}


def get_all_vault_files():
    """Walk all SCAN_DIRS and collect markdown files, returning (rel_path, abs_path) tuples."""
    files = []
    for d in SCAN_DIRS:
        abs_dir = os.path.join(VAULT_ROOT, d)
        if not os.path.isdir(abs_dir):
            continue
        for root, dirs, filenames in os.walk(abs_dir):
            # Skip hidden/system dirs
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS]
            for f in filenames:
                ext = os.path.splitext(f)[1].lower()
                if ext in INCLUDE_EXTENSIONS:
                    abs_path = os.path.join(root, f)
                    rel_path = os.path.relpath(abs_path, VAULT_ROOT)
                    files.append((rel_path, abs_path))
    return files


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"  ⚠️  Could not read {path}: {e}", file=sys.stderr)
        return ""


def build_file_map(all_files):
    """Build mapping: lowercase basename with/without extension -> set of rel_paths."""
    fm = defaultdict(set)
    for rel_path, _ in all_files:
        basename = os.path.basename(rel_path)
        fm[basename.lower()].add(rel_path)

        name_no_ext = os.path.splitext(basename)[0]
        fm[name_no_ext.lower()].add(rel_path)

        # Also map by full rel_path
        fm[rel_path.lower()].add(rel_path)

        # Map just the name part (without directory prefix)
        # e.g. "dom-accounting-finote" from "02_atomic_nodes/dom-accounting-finote.md"
        parts = rel_path.replace("\\", "/").split("/")
        for part in parts:
            if part.endswith(".md"):
                fm[part.lower()].add(rel_path)
                fm[part.lower().replace(".md", "")].add(rel_path)

    return fm


def find_obsidian_wiki_links(content):
    """
    Find all Obsidian [[wiki links]] including aliases and anchors.
    Returns list of (full_match, target_page, alias_or_anchor).
    """
    # [[page]] or [[page|alias]] or [[page#anchor]] or [[page#anchor|alias]]
    pattern = r"\[\[([^\]]+?)(?:\|([^\]]*?))?\]\]"
    matches = []
    for m in re.finditer(pattern, content):
        target = m.group(1).strip()
        alias = m.group(2).strip() if m.group(2) else ""
        # Strip any #anchor from target for resolution
        clean_target = target.split("#")[0].strip() if "#" in target else target.strip()
        matches.append((m.group(0), clean_target, target))
    return matches


def find_markdown_links(content):
    """
    Find all standard Markdown links [label](path).
    Returns list of (full_match, url).
    """
    pattern = r"\[([^\]]*)\]\(([^)]+)\)"
    matches = []
    for m in re.finditer(pattern, content):
        url = m.group(2).strip()
        matches.append((m.group(0), url))
    return matches


def is_external_link(url):
    """Check if a link is external (web, mailto, anchor, etc.)."""
    for prefix in EXTERNAL_DOMAIN_ALLOWLIST:
        if url.startswith(prefix):
            return True
    return False


def is_svg_icon(url):
    """Detect if URL is a local SVG icon name (no extension, no slash)."""
    return "/" not in url and "." not in url and not url.startswith("#")


def check_link_portability(link_text, file_rel_path):
    """Check if a markdown link violates portability rules."""
    violations = []
    # Absolute path starting with /
    if link_text.startswith("/"):
        violations.append(f"đường dẫn tuyệt đối ('{link_text}')")
    # Relative path going up (../)
    if "../" in link_text:
        violations.append(f"đường dẫn '../' ('{link_text}')")
    return violations


###############################################################################
# MODULE 1: LINK AUDITOR
###############################################################################
def audit_links(all_files, file_map):
    """Kiểm toán tất cả liên kết trong vault, báo cáo liên kết hỏng và vi phạm portability."""
    print("=" * 60)
    print("  🔗 KIỂM TOÁN LIÊN KẾT (LINK AUDITOR)")
    print("=" * 60)

    broken_obsidian = []
    broken_markdown = []
    portability_issues = []
    checked_count = 0
    total_links = 0

    # Collect all existing page names (without extensions) for resolving wiki links
    existing_pages = set()
    for rel_path, _ in all_files:
        # e.g. "02_atomic_nodes/dom-accounting-finote.md" -> "dom-accounting-finote"
        name = os.path.splitext(os.path.basename(rel_path))[0]
        existing_pages.add(name.lower())
        # Also add the full path without extension
        full_no_ext = os.path.splitext(rel_path)[0]
        existing_pages.add(full_no_ext.lower())

    for rel_path, abs_path in all_files:
        content = read_file(abs_path)
        if not content:
            continue

        checked_count += 1

        # --- Check Obsidian Wiki Links [[...]] ---
        for full_match, target_page, raw_target in find_obsidian_wiki_links(content):
            total_links += 1
            # Skip embeds of external files like [[README]]
            if not target_page:
                continue

            # Check if target exists in the file map
            target_lower = target_page.lower()
            found = target_lower in existing_pages

            if not found:
                broken_obsidian.append((rel_path, full_match, target_page))

        # --- Check Markdown Links [label](path) ---
        for full_match, url in find_markdown_links(content):
            total_links += 1

            # Skip external links, anchors, and SVG icon references
            if is_external_link(url) or is_svg_icon(url):
                continue

            # Check portability
            p_issues = check_link_portability(url, rel_path)
            for issue in p_issues:
                portability_issues.append((rel_path, url, issue))

            # Resolve the link to a known file
            # Normalize: strip leading ./ and remove anchor
            clean_url = url.split("#")[0].strip()
            if clean_url.startswith("./"):
                clean_url = clean_url[2:]

            # Try to find the file
            link_lower = clean_url.lower()
            found = False
            for known_rel_path in file_map:
                if link_lower == known_rel_path or \
                   link_lower == os.path.splitext(known_rel_path)[0].lower():
                    found = True
                    break
                # Also check just the basename
                base = os.path.basename(known_rel_path).lower()
                base_no_ext = os.path.splitext(base)[0]
                if link_lower == base or link_lower == base_no_ext:
                    found = True
                    break

            if not found:
                broken_markdown.append((rel_path, full_match, clean_url))

    # --- REPORT ---
    print(f"\n  📊 Đã kiểm tra {checked_count} file, {total_links} liên kết tổng cộng.")
    print()

    if portability_issues:
        print(f"  ❌ VI PHẠM PORTABILITY ({len(portability_issues)}):")
        for rel_path, link, issue in portability_issues:
            print(f"     - [{rel_path}]: {issue}")
    else:
        print("  ✅ Không vi phạm portability nào.")

    if broken_obsidian:
        print(f"\n  ❌ LIÊN KẾT OBSIDIAN HỎNG ({len(broken_obsidian)}):")
        for rel_path, match, target in broken_obsidian:
            print(f"     - [{rel_path}]: {match} → không tìm thấy '{target}'")
    else:
        print("  ✅ Không có liên kết Obsidian hỏng.")

    if broken_markdown:
        print(f"\n  ❌ LIÊN KẾT MARKDOWN HỎNG ({len(broken_markdown)}):")
        for rel_path, match, url in broken_markdown:
            print(f"     - [{rel_path}]: {match} → không tìm thấy '{url}'")
    else:
        print("  ✅ Không có liên kết Markdown hỏng.")

    summary = {
        "checked_files": checked_count,
        "total_links": total_links,
        "portability_issues": len(portability_issues),
        "broken_obsidian": len(broken_obsidian),
        "broken_markdown": len(broken_markdown),
    }
    return summary


###############################################################################
# MODULE 2: HIERARCHICAL GRAPH AUDIT
###############################################################################
def parse_frontmatter(content, file_rel_path):
    """Parse YAML frontmatter from markdown content."""
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        return {}

    fm_text = fm_match.group(1)
    try:
        data = yaml.safe_load(fm_text)
        if isinstance(data, dict):
            return data
        return {}
    except yaml.YAMLError as e:
        print(f"  ⚠️  Lỗi YAML frontmatter tại [{file_rel_path}]: {e}", file=sys.stderr)
        return {}


def clean_link(ref):
    """Clean a frontmatter reference — strip [[ ]] and whitespace."""
    if not ref:
        return ""
    cleaned = ref.strip().replace("[[", "").replace("]]", "").strip()
    return cleaned


def audit_hierarchy(all_files):
    """Kiểm toán cấu trúc phân cấp parent/depends_on/source_note trong frontmatter."""
    print("\n" + "=" * 60)
    print("  🏗️  KIỂM TOÁN CẤU TRÚC PHÂN CẤP (HIERARCHICAL GRAPH AUDIT)")
    print("=" * 60)

    nodes = {}  # slug -> {file, frontmatter}

    # Build node index from all files
    for rel_path, abs_path in all_files:
        if not rel_path.endswith(".md"):
            continue
        content = read_file(abs_path)
        if not content:
            continue

        fm = parse_frontmatter(content, rel_path)
        if not fm:
            continue

        slug = os.path.splitext(os.path.basename(rel_path))[0]
        nodes[slug] = {
            "file": rel_path,
            "fm": fm,
            "content": content,
        }

    # Build a set of all known slugs for fast lookup
    known_slugs = set(nodes.keys())

    inconsistencies = []

    # Check parent references
    for slug, info in nodes.items():
        fm = info["fm"]
        parent_ref = fm.get("parent", "")
        depends_on_refs = fm.get("depends_on", [])
        source_note = fm.get("source_note", "")

        # 1. Validate parent
        if parent_ref:
            parent_clean = clean_link(parent_ref)
            if parent_clean and parent_clean not in known_slugs:
                inconsistencies.append(
                    f"[{info['file']}]: parent='{parent_clean}' không tồn tại trong vault"
                )

        # 2. Validate depends_on
        if isinstance(depends_on_refs, list):
            for dep in depends_on_refs:
                dep_clean = clean_link(dep)
                if dep_clean and dep_clean not in known_slugs:
                    inconsistencies.append(
                        f"[{info['file']}]: depends_on='{dep_clean}' không tồn tại trong vault"
                    )
        elif isinstance(depends_on_refs, str) and depends_on_refs.strip():
            dep_clean = clean_link(depends_on_refs)
            if dep_clean and dep_clean not in known_slugs:
                inconsistencies.append(
                    f"[{info['file']}]: depends_on='{dep_clean}' không tồn tại trong vault"
                )

        # 3. Validate source_note (for processed notes)
        if source_note:
            source_clean = clean_link(source_note)
            # source_note may point to a file path, not just a slug
            # Check if it exists as a known slug or as a rel_path known slug without dir prefix
            source_filename = os.path.splitext(os.path.basename(source_clean))[0]
            if not (source_clean in known_slugs or source_filename in known_slugs):
                # Could be pointing to an external source — check if it's a path that exists
                if not source_clean.startswith("http"):
                    inconsistencies.append(
                        f"[{info['file']}]: source_note='{source_clean}' không tồn tại trong vault"
                    )

    # --- REPORT ---
    if inconsistencies:
        print(f"\n  ❌ PHÁT HIỆN {len(inconsistencies)} VẤN ĐỀ PHÂN CẤP:")
        for issue in inconsistencies:
            print(f"     - {issue}")
    else:
        print("\n  ✅ Cấu trúc phân cấp tri thức (parent/depends_on/source_note) hoàn toàn nhất quán!")

    return inconsistencies


###############################################################################
# MAIN
###############################################################################
def main():
    print("=" * 60)
    print("  🔬 STAX WIKI VAULT AUDIT")
    print("  Phân tích toàn diện tính toàn vẹn của tri thức")
    print("=" * 60)
    print(f"  Root: {VAULT_ROOT}")
    print()

    # Phase 1: Collect files
    print("📂 Đang thu thập tệp tin vault...")
    all_files = get_all_vault_files()
    file_map = build_file_map(all_files)
    print(f"   Tổng cộng {len(all_files)} tệp tin trong phạm vi kiểm toán.\n")

    # Phase 2: Link Audit
    link_summary = audit_links(all_files, file_map)

    # Phase 3: Hierarchy Audit
    audit_hierarchy(all_files)

    # Final summary
    print("\n" + "=" * 60)
    print("  📋 TỔNG KẾT KIỂM TOÁN")
    print("=" * 60)
    total_issues = (
        link_summary["portability_issues"]
        + link_summary["broken_obsidian"]
        + link_summary["broken_markdown"]
    )
    if total_issues == 0:
        print("  ✅ VAULT LÀNH MẠNH: Không phát hiện vấn đề nào!")
        print("  🎉 Toàn bộ liên kết và cấu trúc phân cấp đều nhất quán.")
    else:
        print(f"  ⚠️  Phát hiện {total_issues} vấn đề cần xem xét:")
        print(f"      - Vi phạm portability: {link_summary['portability_issues']}")
        print(f"      - Liên kết Obsidian hỏng: {link_summary['broken_obsidian']}")
        print(f"      - Liên kết Markdown hỏng: {link_summary['broken_markdown']}")
    print()


if __name__ == "__main__":
    main()
