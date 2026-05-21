#!/usr/bin/env python3
import os
import re
import sys
import json
import shutil
import urllib.request
import urllib.error
import time
from datetime import datetime

# Path Config
STAX_ASP_DOCS = "/home/ka/Repos/github.com/trongnghiango/STAX_ASP/docs"
VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DOCS_DIR = os.path.join(VAULT_ROOT, "00_raw_docs")
ATOMIC_NODES_DIR = os.path.join(VAULT_ROOT, "02_atomic_nodes")
NEURAL_MAP_DIR = os.path.join(VAULT_ROOT, "03_neural_map")

# API Settings
DEFAULT_BASE_URL = "https://api.anthropic.com"
DEFAULT_MODEL = "ag/gemini-3-flash"

def get_api_url():
    base_url = os.environ.get("ANTHROPIC_BASE_URL", DEFAULT_BASE_URL)
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    return f"{base_url}/v1/messages"

def get_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("Warning: ANTHROPIC_API_KEY environment variable is not set. AI atomic note generation will be skipped.", file=sys.stderr)
        print("You can still copy raw files, but auto-synthesizing Layer 3 and Layer 4 requires the API key.", file=sys.stderr)
    return key

def make_claude_request(prompt, api_key, model=DEFAULT_MODEL):
    """
    Makes a robust request to the Anthropic API (supporting stream proxy).
    """
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": model,
        "max_tokens": 4000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    req = urllib.request.Request(
        get_api_url(),
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            if "text/event-stream" in response.headers.get("content-type", ""):
                full_text = ""
                for line in res_body.split("\n"):
                    line = line.strip()
                    if line.startswith("data:"):
                        data_str = line[5:].strip()
                        if data_str == "[DONE]":
                            continue
                        try:
                            data_json = json.loads(data_str)
                            if data_json.get("type") == "content_block_delta" and "delta" in data_json:
                                full_text += data_json["delta"].get("text", "")
                            elif data_json.get("type") == "completion":
                                full_text += data_json.get("completion", "")
                        except Exception:
                            pass
                return full_text.strip()
            else:
                res_json = json.loads(res_body)
                return res_json["content"][0]["text"]
    except urllib.error.HTTPError as e:
        print(f"HTTP Error calling Claude: {e.code} - {e.reason}", file=sys.stderr)
        try:
            err_body = e.read().decode("utf-8")
            print(f"Error Details: {err_body}", file=sys.stderr)
        except Exception:
            pass
        return None
    except Exception as e:
        print(f"Connection error calling Claude: {e}", file=sys.stderr)
        return None

def copy_raw_docs():
    """
    Copies updated documents from STAX_ASP/docs/ to 00_raw_docs/ incrementally.
    """
    print(f"--- Bước 1: Đồng bộ hóa tài liệu thô từ {STAX_ASP_DOCS} ---")
    if not os.path.exists(STAX_ASP_DOCS):
        print(f"Error: STAX_ASP docs directory not found at {STAX_ASP_DOCS}.", file=sys.stderr)
        return False

    os.makedirs(RAW_DOCS_DIR, exist_ok=True)
    copied_count = 0

    for root, dirs, files in os.walk(STAX_ASP_DOCS):
        # Calculate relative path
        rel_path = os.path.relpath(root, STAX_ASP_DOCS)
        dest_dir = RAW_DOCS_DIR if rel_path == "." else os.path.join(RAW_DOCS_DIR, rel_path)

        # Skip git folders or system folders
        if ".git" in root.split(os.sep):
            continue

        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)

            # Copy if file doesn't exist or is newer
            if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                shutil.copy2(src_file, dest_file)
                copied_count += 1

    print(f"Đã sao chép/cập nhật {copied_count} tệp tin thô sang {RAW_DOCS_DIR}.")
    return True

def find_new_feature_sessions():
    """
    Scans RAW_DOCS_DIR/STAX/history/ and RAW_DOCS_DIR/context/ to find session folders
    that do not have a corresponding Atomic Note in ATOMIC_NODES_DIR.
    """
    print("\n--- Bước 2: Phát hiện các phiên làm việc (Features) mới ---")
    history_dir = os.path.join(RAW_DOCS_DIR, "STAX", "history")
    context_dir = os.path.join(RAW_DOCS_DIR, "context")

    sessions = []

    # Helper to check if a session is already processed by scanning existing atomic notes
    existing_notes = []
    if os.path.exists(ATOMIC_NODES_DIR):
        existing_notes = [f for f in os.listdir(ATOMIC_NODES_DIR) if f.endswith(".md")]

    def is_session_processed(slug):
        # Look for matching slug in existing atomic note contents
        for note in existing_notes:
            note_path = os.path.join(ATOMIC_NODES_DIR, note)
            try:
                with open(note_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if slug in content or note.startswith(f"dom-{slug}") or note.startswith(f"hb-{slug}"):
                        return True
            except Exception:
                pass
        return False

    # Scan history
    if os.path.exists(history_dir):
        for entry in os.listdir(history_dir):
            entry_path = os.path.join(history_dir, entry)
            if os.path.isdir(entry_path) and "_" in entry:
                slug = entry.split("_", 1)[1]
                if not is_session_processed(slug):
                    sessions.append({
                        "name": entry,
                        "slug": slug,
                        "path": entry_path,
                        "type": "history"
                    })

    # Scan active context
    if os.path.exists(context_dir):
        for entry in os.listdir(context_dir):
            entry_path = os.path.join(context_dir, entry)
            if os.path.isdir(entry_path) and "_" in entry:
                slug = entry.split("_", 1)[1]
                if not is_session_processed(slug):
                    sessions.append({
                        "name": entry,
                        "slug": slug,
                        "path": entry_path,
                        "type": "context"
                    })

    print(f"Phát hiện thấy {len(sessions)} phiên làm việc mới chưa được số hóa:")
    for s in sessions:
        print(f" - [{s['type'].upper()}] {s['name']}")
    return sessions

def extract_walkthrough_data(session):
    """
    Finds and reads the walkthrough or implementation plan file from the session directory.
    """
    files = os.listdir(session["path"])
    content = ""

    # Try walkthrough first, then tasks, then implementation plan
    target_files = ["03_be_walkthrough.md", "03_fe_walkthrough.md", "03_walkthrough.md",
                    "01_be_implementation_plan.md", "01_fe_implementation_plan.md",
                    "01_implementation_plan.md", "00_be_analysis.md", "00_fe_analysis.md"]

    selected_file = None
    for tf in target_files:
        if tf in files:
            selected_file = tf
            break

    if not selected_file and files:
        # Fallback to the largest markdown file
        md_files = [f for f in files if f.endswith(".md")]
        if md_files:
            selected_file = max(md_files, key=lambda f: os.path.getsize(os.path.join(session["path"], f)))

    if selected_file:
        file_path = os.path.join(session["path"], selected_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f" -> Đọc dữ liệu từ file: {selected_file} ({len(content)} kí tự)")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)

    return content

def generate_atomic_note(session, raw_content, api_key):
    """
    Calls Claude to synthesize the raw walkthrough into a perfect Layer 3 Atomic Note.
    """
    print(f"\n--- Bước 3: Đang tự động trích xuất Nốt nguyên tử cho {session['name']} ---")

    prompt = f"""Bạn là một Chuyên gia phân tích và thiết kế hệ thống AI của dự án STAX.
Hãy chuyển đổi tài liệu thiết kế/walkthrough thô của phiên làm việc nghiệp vụ dưới đây thành một **Layer 3 Atomic Note (Nốt nguyên tử)** cực kỳ tinh gọn, tối ưu hóa cho AI Agent.

Tên phiên làm việc: {session['name']}
Phân loại: {session['type']}

Nội dung tài liệu thô:
```markdown
{raw_content[:8000]}
```

### YÊU CẦU BẮT BUỘC:
1. **Dưới 50 dòng:** Tóm tắt thật cô đọng, chỉ giữ lại chi tiết kỹ thuật cốt lõi: cấu trúc Schema DB mới, API contracts mới, hoặc design pattern nghiệp vụ mới. Không đưa boilerplate, lời chào hay giải thích dài dòng.
2. **Ngôn ngữ:** Tiếng Việt chuyên nghiệp.
3. **YAML Frontmatter bắt buộc ở đầu file dạng:**
```yaml
---
id: [Tiền tố viết tắt của chuyên đề, e.g. "dom-{session['slug']}" hoặc "hb-{session['slug']}" hoặc "arch-{session['slug']}"]
title: [Tiêu đề tiếng Việt cực ngắn gọn, phản ánh rõ tính năng]
layer: 3-atomic
parent: "[[01_core_architecture]]" hoặc "[[03_technical_handbooks]]" hoặc "[[04_domain_knowledge]]" (chọn 1 cái phù hợp nhất làm cha)
depends_on:
  - "[[nốt-layer-3-khác-nếu-có]]"
summary: "[1 câu tóm tắt cực kỳ ngắn gọn và chứa từ khóa chính để AI đọc nhanh]"
tags: [danh, sách, từ, khóa, liên, quan]
---
```
4. **Liên kết chéo:** Hãy liên kết đến các nốt Layer 3 phổ biến khác nếu có liên quan (ví dụ: `[[arch-als-tenant-isolation]]`, `[[hb-drizzle-base-repo]]`, `[[hb-delta-logging]]`, `[[dom-accounting-finote]]`) bằng cú pháp Obsidian `[[tên-nốt]]`.

Chỉ trả về nội dung tệp tin Markdown hoàn chỉnh, bắt đầu bằng --- và kết thúc bằng nội dung. Không kèm lời mở đầu hay giải thích của bạn ngoài Markdown.
"""

    note_content = make_claude_request(prompt, api_key)
    if not note_content:
        return None

    # Ensure it starts with frontmatter
    if not note_content.strip().startswith("---"):
        # Fix missing frontmatter in case Claude forgot
        print("Warning: Frontmatter not detected at start, recovering...")

    # Extract ID from generated content to name the file
    id_match = re.search(r"^id:\s*(.+)$", note_content, re.MULTILINE)
    note_id = f"dom-{session['slug']}"
    if id_match:
        note_id = id_match.group(1).strip().replace('"', '').replace("'", "")

    filename = f"{note_id}.md"
    dest_path = os.path.join(ATOMIC_NODES_DIR, filename)

    try:
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(note_content)
        print(f"✅ Đã tạo thành công Nốt nguyên tử Layer 3: {dest_path}")
        return note_id, note_content
    except Exception as e:
        print(f"Error writing atomic note: {e}", file=sys.stderr)
        return None

def update_routing_table_and_index(note_id, note_content):
    """
    Auto-patches 02_atomic_nodes/INDEX.md and 03_neural_map/AI_ROUTING_TABLE.md
    to register the new Atomic Note.
    """
    print(f"\n--- Bước 4: Tự động cập nhật Bản đồ Định tuyến và Chỉ mục ---")

    # 1. Parse metadata from the new note content
    title = note_id
    summary = ""
    tags = []
    parent = ""

    title_match = re.search(r"^title:\s*(.+)$", note_content, re.MULTILINE)
    summary_match = re.search(r"^summary:\s*(.+)$", note_content, re.MULTILINE)
    tags_match = re.search(r"^tags:\s*\[(.+)\]$", note_content, re.MULTILINE)
    parent_match = re.search(r"^parent:\s*(.+)$", note_content, re.MULTILINE)

    if title_match:
        title = title_match.group(1).strip().replace('"', '').replace("'", "")
    if summary_match:
        summary = summary_match.group(1).strip().replace('"', '').replace("'", "")
    if tags_match:
        tags = [t.strip().replace('"', '').replace("'", "") for t in tags_match.group(1).split(",")]
    if parent_match:
        parent = parent_match.group(1).strip().replace('"', '').replace("'", "")

    # Clean brackets from parent e.g. "[[04_domain_knowledge]]" -> "04_domain_knowledge"
    parent_clean = parent.replace("[", "").replace("]", "")

    # 2. Patch 02_atomic_nodes/INDEX.md
    index_path = os.path.join(ATOMIC_NODES_DIR, "INDEX.md")
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_content = f.read()

            # Check if already in index
            if f"[[{note_id}]]" not in index_content:
                # Find appropriate table based on parent
                table_headers = {
                    "01_core_architecture": "## 🏗️ 1. Nhóm Kiến trúc & Hạ tầng",
                    "02_standards_governance": "## 🏰 2. Nhóm Tiêu chuẩn & Quy tắc",
                    "03_technical_handbooks": "## 📚 3. Nhóm Sổ tay Thực thi",
                    "04_domain_knowledge": "## 📦 4. Nhóm Nghiệp vụ & Từ điển"
                }

                target_header = table_headers.get(parent_clean, "## 📦 4. Nhóm Nghiệp vụ & Từ điển")

                new_row = f"| [[{note_id}]] | {summary} | *Tự động* | `#{' ` #'.join(tags)}` |\n"

                # Insert row after table header and its markdown table structure
                header_index = index_content.find(target_header)
                if header_index != -1:
                    # Find end of table headers (locate the delimiter line |---|---|...)
                    delim_index = index_content.find("| :--- | :--- | :--- | :--- |", header_index)
                    if delim_index != -1:
                        insert_pos = index_content.find("\n", delim_index) + 1
                        patched_index = index_content[:insert_pos] + new_row + index_content[insert_pos:]

                        with open(index_path, 'w', encoding='utf-8') as f:
                            f.write(patched_index)
                        print(f" -> Đã cập nhật 02_atomic_nodes/INDEX.md thành công.")
        except Exception as e:
            print(f"Error patching INDEX.md: {e}", file=sys.stderr)

    # 3. Patch 03_neural_map/AI_ROUTING_TABLE.md
    routing_path = os.path.join(NEURAL_MAP_DIR, "AI_ROUTING_TABLE.md")
    if os.path.exists(routing_path):
        try:
            with open(routing_path, 'r', encoding='utf-8') as f:
                routing_content = f.read()

            if f"[[{note_id}]]" not in routing_content:
                # Find appropriate section
                sections = {
                    "01_core_architecture": "### 1. Thiết kế Module mới, Tổ chức Folder & Import",
                    "02_standards_governance": "### 1. Thiết kế Module mới, Tổ chức Folder & Import",
                    "03_technical_handbooks": "### 3. Xác thực, Phân quyền & Request Flow",
                    "04_domain_knowledge": "### 5. Xử lý logic Nghiệp vụ Core (HRM / CRM / Accounting)"
                }

                # Handle database specific routing
                if any(x in tags for x in ["database", "drizzle", "transactions", "als"]):
                    target_sec = "### 2. Làm việc với Cơ sở dữ liệu & Giao dịch (Database & Transactions)"
                elif any(x in tags for x in ["logging", "delta-logging", "audit-log"]):
                    target_sec = "### 4. Logging & Kiểm toán nghiệp vụ (Audit Logging)"
                else:
                    target_sec = sections.get(parent_clean, "### 5. Xử lý logic Nghiệp vụ Core (HRM / CRM / Accounting)")

                new_route = f"    *   `[[{note_id}]]` — Đường dẫn: [02_atomic_nodes/{note_id}.md](../02_atomic_nodes/{note_id}.md)\n"

                # Locate section and insert before the next header or end of section list
                sec_index = routing_content.find(target_sec)
                if sec_index != -1:
                    # Find insert position (after the current list)
                    list_start = routing_content.find("*   **Nốt cần đọc:**", sec_index)
                    if list_start != -1:
                        insert_pos = routing_content.find("\n\n", list_start)
                        if insert_pos == -1:
                            insert_pos = len(routing_content)
                        # Add a newline
                        patched_routing = routing_content[:insert_pos] + "\n" + new_route + routing_content[insert_pos:]

                        with open(routing_path, 'w', encoding='utf-8') as f:
                            f.write(patched_routing)
                        print(f" -> Đã cập nhật 03_neural_map/AI_ROUTING_TABLE.md thành công.")
        except Exception as e:
            print(f"Error patching AI_ROUTING_TABLE.md: {e}", file=sys.stderr)

def main():
    print("==================================================")
    print("🔋 BẮT ĐẦU QUY TRÌNH ĐỒNG BỘ TRI THỨC TỰ ĐỘNG STAX")
    print("==================================================")

    # 1. Sync raw files
    if not copy_raw_docs():
        sys.exit(1)

    # 2. Get API key
    api_key = get_api_key()
    if not api_key:
        print("\n[Hoàn thành một nửa] Đã đồng bộ thành công các file thô. Bỏ qua trích xuất AI vì thiếu API Key.")
        sys.exit(0)

    # 3. Find new features
    new_sessions = find_new_feature_sessions()
    if not new_sessions:
        print("\n🎉 Không có tính năng mới nào cần số hóa. Tất cả đã đồng bộ hoàn hảo!")
        sys.exit(0)

    # 4. Ingest and synthesize each feature
    success_count = 0
    consecutive_failures = 0

    for session in new_sessions:
        # Prevent hitting rate limits with a small sleep
        time.sleep(2)

        raw_data = extract_walkthrough_data(session)
        if not raw_data:
            print(f"⚠️ Bỏ qua {session['name']} vì không tìm thấy file walkthrough/thiết kế.")
            continue

        result = generate_atomic_note(session, raw_data, api_key)
        if result:
            note_id, note_content = result
            update_routing_table_and_index(note_id, note_content)
            success_count += 1
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            print(f"❌ Không thể tạo nốt nguyên tử cho {session['name']}.")
            if consecutive_failures >= 3:
                print("\n⚠️ Đã xảy ra 3 lỗi liên tiếp (có thể do giới hạn số lượng yêu cầu API (Rate Limit) hoặc hết hạn mức Quota).")
                print("Tạm dừng quy trình trích xuất AI. Phần tài liệu thô đã được đồng bộ hoàn tất.")
                break

    print("\n==================================================")
    print(f"🎉 ĐỒNG BỘ HOÀN TẤT! Đã số hóa thành công {success_count} nốt nguyên tử.")
    print("==================================================")

if __name__ == "__main__":
    main()
