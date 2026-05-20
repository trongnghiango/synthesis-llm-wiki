#!/usr/bin/env python3
import os
import re
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# Directory Paths (Relative to vault root)
CLIPPINGS_DIR = "Clippings"
PROCESSED_DIR = "2-Processed"

# API Settings
DEFAULT_BASE_URL = "https://api.anthropic.com"
DEFAULT_MODEL = "ag/gemini-3-flash"

def get_api_url():
    base_url = os.environ.get("ANTHROPIC_BASE_URL", DEFAULT_BASE_URL)
    # Ensure no trailing slash
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    return f"{base_url}/v1/messages"

def get_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("Error: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it in your environment (e.g. export ANTHROPIC_API_KEY='your-key')", file=sys.stderr)
        sys.exit(1)
    return key

def parse_frontmatter(content):
    """
    Parses YAML frontmatter from markdown file.
    Returns (frontmatter_dict, body_text, original_frontmatter_raw_string)
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content, ""

    fm_raw = match.group(1)
    body = match.group(2)

    fm_dict = {}
    for line in fm_raw.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")

            # Handle list parsing if applicable (e.g. tags: [a, b])
            if val.startswith("[") and val.endswith("]"):
                items = [i.strip().strip('"').strip("'") for i in val[1:-1].split(",") if i.strip()]
                fm_dict[key] = items
            else:
                fm_dict[key] = val

    return fm_dict, body, fm_raw

def serialize_frontmatter(fm_dict):
    """
    Serializes a dictionary back to YAML frontmatter format.
    """
    lines = ["---"]
    for k, v in fm_dict.items():
        if isinstance(v, list):
            items_str = ", ".join(f'"{i}"' for i in v)
            lines.append(f"{k}: [{items_str}]")
        else:
            if isinstance(v, str) and (":" in v or '"' in v or "'" in v):
                safe_v = v.replace('"', '\\"')
                lines.append(f'{k}: "{safe_v}"')
            else:
                lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)

def make_claude_request(prompt, api_key, model):
    """
    Makes a request to the Anthropic API.
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
            res_json = json.loads(res_body)
            return res_json["content"][0]["text"]
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        try:
            error_details = e.read().decode("utf-8")
            print(f"Details: {error_details}", file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Error making API request: {e}", file=sys.stderr)
        sys.exit(1)

def process_clipping(filepath, filename, api_key, model):
    print(f"\nProcessing Clipping: {filename}...")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fm_dict, body, fm_raw = parse_frontmatter(content)

    title = fm_dict.get("title")
    if not title:
        title = filename[:-3].replace("-", " ").title()

    # Formulate a Vietnamese-centric prompt to synthesize highly complex content into clean, professional Vietnamese notes.
    prompt = f"""Bạn là một chuyên gia quản lý tri thức cao cấp (Senior Knowledge Curator) và chuyên gia Phân tích nghiệp vụ (BA)/Kiến trúc sư hệ thống.
Nhiệm vụ của bạn là đọc bài viết kỹ thuật/tin tức công nghệ thô (thường bằng tiếng Anh) dưới đây, sau đó chắt lọc, tổng hợp và chuyển ngữ nó thành một ghi chú bằng TIẾNG VIỆT cực kỳ dễ hiểu, cô đọng nhưng giữ nguyên các thuật ngữ kỹ thuật chuyên ngành quan trọng.

Hãy phân tích kỹ lưỡng nội dung và xuất thông tin theo định dạng JSON với cấu trúc chính xác sau:
{{
  "short_summary": "Tóm tắt cực kỳ ngắn gọn từ 1 đến 2 câu phản ánh giá trị cốt lõi của bài viết.",
  "vietnamese_title": "Tiêu đề Tiếng Việt được dịch nghĩa một cách chuyên nghiệp và cuốn hút.",
  "ai_summary": "Bản tổng hợp chi tiết bằng tiếng Việt theo định dạng markdown (dùng bullet points), chia nhỏ thành các mục ý nghĩa chính (Key Insights, Giá trị nghiệp vụ, Tác động công nghệ hoặc Kiến trúc nếu có).",
  "keywords": ["từ-khóa-1", "từ-khóa-2", "từ-khóa-3"]
}}

Yêu cầu xuất ra định dạng JSON chuẩn xác và KHÔNG có bất kỳ ký tự giải thích hay định dạng markdown code block nào xung quanh JSON.

Nội dung bài viết thô:
Tiêu đề gốc: {title}
Nội dung bài viết:
{body}
"""

    response_text = make_claude_request(prompt, api_key, model)

    clean_json_str = response_text.strip()
    if clean_json_str.startswith("```json"):
        clean_json_str = clean_json_str[7:]
    if clean_json_str.startswith("```"):
        clean_json_str = clean_json_str[3:]
    if clean_json_str.endswith("```"):
        clean_json_str = clean_json_str[:-3]
    clean_json_str = clean_json_str.strip()

    try:
        synthesis = json.loads(clean_json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        print(f"Raw response was:\n{response_text}")
        return False

    short_summary = synthesis.get("short_summary", "")
    vietnamese_title = synthesis.get("vietnamese_title", f"Processed: {title}")
    ai_summary = synthesis.get("ai_summary", "")
    keywords = synthesis.get("keywords", [])

    # Format keywords as hashtags
    hashtags_list = [f"#{kw.lower().replace(' ', '-')}" for kw in keywords]
    hashtags_str = ", ".join(hashtags_list)

    # Format output file name: YYYYMMDDHHMM-slug.md
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', vietnamese_title.lower())
    slug = re.sub(r'[\s-]+', '-', slug).strip('-')

    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    processed_filename = f"{timestamp}-{slug}-processed.md"
    processed_filepath = os.path.join(PROCESSED_DIR, processed_filename)

    processed_fm = {
        "id": f"{timestamp}-{slug}-processed",
        "aliases": [vietnamese_title],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": "processed-note",
        "source_note": f"[[{CLIPPINGS_DIR}/{filename}]]",
        "tags": ["processed", "clippings"] + [kw.lower().replace(' ', '-') for kw in keywords[:3]],
        "short_summary": short_summary,
        "keywords": keywords
    }

    processed_body = f"""{serialize_frontmatter(processed_fm)}

# {vietnamese_title}

## 🤖 Tóm tắt Ngắn (AI Summary)
> {short_summary}

## 📝 Chi tiết Nghiên cứu & Chắt lọc Tri thức
{ai_summary}

### 🔑 Từ khóa kỹ thuật (Keywords)
{hashtags_str}

---
*Ghi chú này được dịch nghĩa và chắt lọc tự động từ bản Clipping gốc: [[{CLIPPINGS_DIR}/{filename}|{title}]]*
"""

    with open(processed_filepath, "w", encoding="utf-8") as f:
        f.write(processed_body)
    print(f"Success: Processed Vietnamese note written to {processed_filepath}")

    # Update raw clipping frontmatter status to processed
    fm_dict["status"] = "processed"
    fm_dict["summary"] = short_summary
    fm_dict["keywords"] = keywords

    updated_clipping_content = serialize_frontmatter(fm_dict) + "\n\n" + body.strip() + "\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_clipping_content)
    print(f"Success: Source Clipping {filepath} updated with status: processed.")
    return True

def main():
    api_key = get_api_key()
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)

    if not os.path.exists(CLIPPINGS_DIR):
        print(f"Clippings directory '{CLIPPINGS_DIR}' does not exist.")
        sys.exit(1)

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    processed_count = 0
    errors_count = 0

    for filename in os.listdir(CLIPPINGS_DIR):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(CLIPPINGS_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            continue

        fm_dict, body, fm_raw = parse_frontmatter(content)

        status = fm_dict.get("status", "pending") # Default status to pending if not present

        # Ensure status is initialized to pending if missing
        if "status" not in fm_dict:
            fm_dict["status"] = "pending"
            updated_content = serialize_frontmatter(fm_dict) + "\n\n" + body.strip() + "\n"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)
            status = "pending"

        # Check if the clipping note is pending to be processed
        if status == "pending":
            try:
                success = process_clipping(filepath, filename, api_key, model)
                if success:
                    processed_count += 1
                else:
                    errors_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}", file=sys.stderr)
                errors_count += 1

    print(f"\nClippings pipeline finished. Processed: {processed_count} notes. Errors: {errors_count} notes.")

if __name__ == "__main__":
    main()
