# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview & Architecture
This repository is an Obsidian-based personal knowledge management (PKM) vault ("synthesis-llm-wiki") designed for AI-assisted note-taking, synthesis, and knowledge accumulation across a 3-layered knowledge pipeline.

### Directory Structure & Layers
*   **Layer 1: Raw** (`0-Inbox/`): Stores incoming raw notes, clipped web pages, articles, and references (naming convention: `YYYYMMDDHHMM-slug.md`).
    *   New notes start with `status: raw`. When the user is ready to process them, they change status to `status: to-process`.
*   **Layer 2: Processed / Synthesized** (`2-Processed/`): Contains distilled summaries, key takeaways, and relevant keywords extracted using the Claude API from raw notes.
*   **Layer 3: Distilled / My Thoughts** (`3-Distilled/`): Contains user-written prose, commentary, and original insights linking back to Processed (Layer 2) notes.
*   `1-Journal/`: Contains daily notes structured by year and month (folder structure: `1-Journal/YYYY/MM/`, naming convention: `YYYY-MM-DD-dddd.md`).
*   `Templates/`: Layouts for Obsidian daily notes, processed notes, and distilled thoughts.
*   `scripts/`: Automation scripts for the vault pipeline.
*   `.obsidian/`: Obsidian settings, CSS styling, plugin details, and metadata.

### Pipeline Automation Command
To run the automated pipeline that processes raw inbox notes with status `to-process` into Layer 2 processed notes using the Claude API:
```bash
# Requires setting your ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY="your-key-here"
python3 scripts/process_vault.py
```

---

## Metadata & Frontmatter Conventions

### 1. Inbox Notes (type: inbox-note) - Layer 1
Every note created in `0-Inbox/` must have the following YAML frontmatter:
```yaml
---
id: YYYYMMDDHHMM-kebab-case-slug
aliases:
  - Note Title in Title Case
date: YYYY-MM-DD
type: inbox-note
summary: ""
keywords: []
status: "raw" # raw | to-process | processed
---
```

### 2. Processed Notes (type: processed-note) - Layer 2
Created automatically by `scripts/process_vault.py` inside `2-Processed/`:
```yaml
---
id: YYYYMMDDHHMM-kebab-case-slug-processed
aliases:
  - "Processed: Note Title"
date: YYYY-MM-DD
type: processed-note
source_note: "[[0-Inbox/YYYYMMDDHHMM-kebab-case-slug.md]]"
tags:
  - processed
  - keyword1
  - keyword2
short_summary: "A very concise 1-2 sentence overview of the article."
keywords: ["keyword1", "keyword2"]
---
```

### 3. Distilled Thoughts (tag: distilled, insight) - Layer 3
Created by the user inside `3-Distilled/` using the `Templates/Distilled-Thought-Template.md` structure:
```yaml
---
id: YYYYMMDDHHMM-distilled
aliases:
  - "Distilled: My Thought Title"
tags:
  - distilled
  - insight
date: YYYY-MM-DD
---
```

### 4. Journal Notes (tag: daily)
Daily journal files placed in `1-Journal/YYYY/MM/` must have the following YAML frontmatter and markdown structure:
```yaml
---
id: YYYYMMDDHHMM-YYYY-MM-DD-day
aliases:
  - YYYY-MM-DD-day
tags:
  - daily
date: YYYY-MM-DD
---
```
**File Structure:**
```markdown
# [DayName], [Day] [MonthName] [Year]

<< [Prev-Date](1-Journal/YYYY/MM/YYYY-MM-DD-prev.md) | [Next-Date](1-Journal/YYYY/MM/YYYY-MM-DD-next.md) >>

## 📝 Notes

- [[0-Inbox/related-note-link|Note Title]]

## ✅ Tasks

- [ ]
```

---

## AI Chat & Coding Protocols (HƯỚNG DẪN XỬ LÝ TRONG CHAT)

When answering questions, discussing design, or modifying/writing markdown files or scripts in this repository, follow these precise protocols:

### 1. Clarification & Understanding (Hiểu rõ trước khi trả lời)
*   State your understanding of the prompt clearly. If anything is ambiguous, ask the user to clarify.
*   If there are multiple ways to interpret or implement a request, list the options. Do not make assumptions or self-select an option without consulting the user.

### 2. Code Snippets (Code ngắn gọn, dễ copy)
*   Ensure all code snippets provided in chat or written to files are concise and focused solely on what is requested.
*   Do not add redundant features, boilerplate, or extra functions. If a 200-line solution can be written in 50 lines, write the 50-line version.

### 3. Targeted Edits Only (Chỉ sửa đúng chỗ được hỏi)
*   Only modify the exact code block, line, or note section that the user asks about.
*   Do not perform unsolicited styling adjustments, formatting cleanups, or refactoring in surrounding areas or adjacent files.
*   Provide edits as precise diffs or isolated code blocks.

### 4. Progress Updates (Theo dõi tiến trình)
*   Provide a brief, 1–2 sentence summary of what has been accomplished and what steps are next every 2–3 turns of conversation.
*   Resolve any ambiguity prior to writing or modifying files.

### 5. Content Summarization & Distillation
When asked to summarize or ingest articles, extract three precise fields:
*   `short_summary`: ""
*   `ai_summary`: ""
*   `keywords`: []

### 6. Non-Intrusive Reasoning
*   Do not attempt to guide, correct, or intervene in the user's personal thought process or reasoning style. The user's input/thought process is sovereign.
