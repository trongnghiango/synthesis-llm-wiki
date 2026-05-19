# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview & Architecture
This repository is an Obsidian-based personal knowledge management (PKM) vault ("synthesis-llm-wiki") designed for AI-assisted note-taking, synthesis, and knowledge accumulation.

### Directory Structure
*   `0-Inbox/`: Stores incoming raw notes, articles, and references (naming convention: `YYYYMMDDHHMM-slug.md`).
*   `1-Journal/`: Contains daily notes structured by year and month (folder structure: `1-Journal/YYYY/MM/`, naming convention: `YYYY-MM-DD-dddd.md`).
*   `Templates/`: (Configured but empty) Standard layouts for Obsidian daily notes.
*   `.obsidian/`: Configuration, community plugins (minimal-settings, tasks, shellcommands, git, daily-nav, dataview, calendar), styling CSS, and vault metadata.

---

## Metadata & Frontmatter Conventions

### 1. Inbox Notes (type: inbox-note)
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
status: "raw" # raw | processed | distilled
---
```

### 2. Journal Notes (tag: daily)
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
