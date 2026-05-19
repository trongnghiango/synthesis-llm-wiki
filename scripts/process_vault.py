#!/usr/bin/env python3
import os
import re
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# Directory Paths (Relative to vault root)
INBOX_DIR = "0-Inbox"
PROCESSED_DIR = "2-Processed"

# API Settings
API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-3-5-sonnet-20241022"

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
    # Pattern to match YAML frontmatter
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content, ""

    fm_raw = match.group(1)
    body = match.group(2)

    # Simple YAML parser
    fm_dict = {}
    for line in fm_raw.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")

            # Handle list parsing if applicable (e.g. keywords: [a, b])
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
            # Escape strings if they contain double quotes or colons
            if isinstance(v, str) and (":" in v or '"' in v or "'" in v):
                # Escape double quotes
                safe_v = v.replace('"', '\\"')
                lines.append(f'{k}: "{safe_v}"')
            else:
                lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)

def make_claude_request(prompt, api_key, model):
    """
    Makes a request to the Anthropic API.
    Uses standard library urllib to avoid requiring external packages.
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
        API_URL,
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

def process_note(filepath, filename, api_key, model):
    print(f"\nProcessing: {filename}...")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fm_dict, body, fm_raw = parse_frontmatter(content)

    # Determine the title of the note
    title = fm_dict.get("aliases", [None])[0] if isinstance(fm_dict.get("aliases"), list) else fm_dict.get("aliases")
    if not title:
        # Try to find first H1 header in the body
        h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
        else:
            # Fallback to filename slug without date prefix
            title = filename
            # Strip date prefix e.g. 202604221412-title -> title
            title_match = re.match(r"^\d+-(.+)$", filename)
            if title_match:
                title = title_match.group(1).replace("-", " ").title()

    # Prompt formulation
    prompt = f"""You are an expert knowledge curator. Your task is to process a raw note (web clip or article) and synthesize it into a clean, highly structured processed note.

Please analyze the raw content below and extract:
1. A very concise 1-2 sentence short summary.
2. A detailed structured bullet-point summary (AI summary) capturing the core insights, key concepts, arguments, or lessons.
3. A list of important keywords relevant to the content.

Please output your response strictly as a JSON object with this exact structure:
{{
  "short_summary": "1-2 sentence summary here.",
  "ai_summary": "Detailed bullet-point summary in markdown here.",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Make sure your output is valid JSON and only the JSON object. Do not include any explanations, markdown code fences like ```json, or headers.

Raw Content:
Title: {title}
Body:
{body}
"""

    response_text = make_claude_request(prompt, api_key, model)

    # Clean response text in case Claude adds markdown code fences
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
        print(f"Failed to parse JSON response from Claude: {e}")
        print(f"Raw response was:\n{response_text}")
        return False

    short_summary = synthesis.get("short_summary", "")
    ai_summary = synthesis.get("ai_summary", "")
    keywords = synthesis.get("keywords", [])

    # Format keywords as a list of hashtags
    hashtags_list = [f"#{kw.lower().replace(' ', '-')}" for kw in keywords]
    hashtags_str = ", ".join(hashtags_list)

    # Write layer 2 note
    processed_filename = filename
    processed_filepath = os.path.join(PROCESSED_DIR, processed_filename)

    processed_fm = {
        "id": fm_dict.get("id", f"{datetime.now().strftime('%Y%m%d%H%M')}-{filename[:-3]}") + "-processed",
        "aliases": [f"Processed: {title}"],
        "date": fm_dict.get("date", datetime.now().strftime("%Y-%m-%d")),
        "type": "processed-note",
        "source_note": f"[[{INBOX_DIR}/{filename}]]",
        "tags": ["processed"] + [kw.lower().replace(' ', '-') for kw in keywords[:5]],
        "short_summary": short_summary,
        "keywords": keywords
    }

    processed_body = f"""{serialize_frontmatter(processed_fm)}

# Processed: {title}

## 🤖 AI Summary
> {short_summary}

### Key Takeaways
{ai_summary}

### 🔑 Keywords
{hashtags_str}

### 📝 Core Content Reference
*Synthesized from raw note: [[{INBOX_DIR}/{filename}|{title}]]*

#### Key Highlights & Raw Text Extracts:
{body[:2000] + ("..." if len(body) > 2000 else "")}
"""

    with open(processed_filepath, "w", encoding="utf-8") as f:
        f.write(processed_body)
    print(f"Success: Processed note written to {processed_filepath}")

    # Update raw note frontmatter status to processed
    fm_dict["status"] = "processed"
    fm_dict["summary"] = short_summary
    fm_dict["keywords"] = keywords

    updated_raw_content = serialize_frontmatter(fm_dict) + "\n\n" + body.strip() + "\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_raw_content)
    print(f"Success: Raw note {filepath} updated with status: processed.")
    return True

def main():
    api_key = get_api_key()
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)

    if not os.path.exists(INBOX_DIR):
        print(f"Inbox directory '{INBOX_DIR}' does not exist.")
        sys.exit(1)

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    processed_count = 0
    errors_count = 0

    for filename in os.listdir(INBOX_DIR):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(INBOX_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            continue

        fm_dict, _, _ = parse_frontmatter(content)

        status = fm_dict.get("status")
        # Check if the note is designated to be processed
        if status == "to-process":
            try:
                success = process_note(filepath, filename, api_key, model)
                if success:
                    processed_count += 1
                else:
                    errors_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}", file=sys.stderr)
                errors_count += 1

    print(f"\nPipeline finished. Processed: {processed_count} notes. Errors: {errors_count} notes.")

if __name__ == "__main__":
    main()
