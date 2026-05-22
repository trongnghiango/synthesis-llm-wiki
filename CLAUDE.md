# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code and architectural documents in this repository.

## Repository Overview & Architecture
This repository is an Obsidian-based personal knowledge management (PKM) vault ("synthesis-llm-wiki") designed for AI-assisted note-taking, synthesis, and knowledge accumulation across a 3-layered knowledge pipeline. It acts as the **strategic brain** for enterprise-grade software development.

### Directory Structure & Layers
*   **Layer 1: Raw** (`0-Inbox/`): Stores incoming raw notes, clipped web pages, articles, BA requirements, and design proposals (naming convention: `YYYYMMDDHHMM-slug.md`).
    *   New notes start with `status: raw`. When the user is ready to process them, they change status to `status: to-process`.
*   **Layer 2: Processed / Synthesized** (`2-Processed/`): Contains distilled summaries, key takeaways, Bounded Context boundaries, Domain Models, and API contracts extracted from raw notes.
*   **Layer 3: Distilled / My Thoughts** (`3-Distilled/`): Contains user-written prose, architectural commentary, trade-off evaluations, and original insights linking back to Processed (Layer 2) notes.
*   `1-Journal/`: Contains daily notes structured by year and month (folder structure: `1-Journal/YYYY/MM/`, naming convention: `YYYY-MM-DD-dddd.md`).
*   `Templates/`: Layouts for Obsidian daily notes, processed notes, and distilled thoughts.
*   `scripts/`: Automation scripts for the vault pipeline.
*   `.obsidian/`: Obsidian settings, CSS styling, plugin details, and metadata.
*   `.agent/`: Built-in specialized technical agent skills for System Design and Development.

### Pipeline Automation Command
To run the automated pipeline that processes raw inbox notes with status `to-process` into Layer 2 processed notes using the Claude API:
```bash
export ANTHROPIC_API_KEY="your-key-here"
python3 scripts/process_vault.py
```

---

## 🎯 Target Architecture Standard: NestJS + DDD + Clean Architecture
When analyzing, reviewing, or designing backend features (specifically referencing the `STAX_ASP` project), you MUST adhere to the following standards:

### 1. Architectural Boundaries (Strict Separation of Concerns)
Every domain module must enforce 3 distinct layers:
*   **Domain Layer (`domain/`):** Pure TypeScript only. No NestJS decorators, no ORM (Drizzle/TypeORM) entities. Contains Rich Domain Entities (with invariants), Value Objects, Domain Events (`IAuditableEvent`), and Repository interfaces (Ports).
*   **Application Layer (`application/`):** Orchestrators only. Contains Use Cases, Services, and Ports. Coordinates transactional boundaries via Async Local Storage (`ITransactionManager.runInTransaction`).
*   **Infrastructure Layer (`infrastructure/`):** Framework and database aware. Contains HTTP Controllers, DTOs, Drizzle DB schemas (`pgTable`, `pgEnum`), Mappers (`toDomain` ↔ `toPersistence`), and Repository implementations (Adapters inheriting `DrizzleBaseRepository`).

### 2. Core Guardrails (The Technical Constitution)
*   **Tenant Isolation:** Always filter queries by `organizationId` fetched from JWT/Session context. Never trust `organizationId` from client query strings unless explicitly bypass-authorized (e.g., STAX Internal Admin).
*   **Domain Purity:** `grep -r "@nestjs\|drizzle-orm" src/modules/{domain}/domain/` MUST return empty.
*   **Symbol DI Tokens:** Register and inject Repositories via Symbol Interfaces (Declaration Merging pattern: `export const IXxxRepository = Symbol('IXxxRepository')`) instead of concrete classes.
*   **Safe Mutation:** Always protect immutable fields (`id`, `organizationId`, `createdAt`) during updates by using the `this.mapToUpdate(data)` utility.
*   **Exception Safety:** Cấm ném `BadRequestException`, `NotFoundException` (NestJS exceptions) ở tầng Domain/Application. Bắt buộc ném `EntityNotFoundException` hoặc `BusinessRuleValidationException` từ `core/shared`.
*   **Event Integrity:** Publish Domain Events via `IEventBus` **after** the database transaction has successfully committed.
*   **Non-Blocking Side Effects:** Trigger audit logs and external notifications in a fire-and-forget manner (`this.auditLog.log(...).catch(() => {})`) outside of the primary database write transaction.

---

## 📋 BA & Ubiquitous Language Protocol
When processing raw requirements or business documents (`inbox-note` status: `to-process`):

1.  **Extract Ubiquitous Language:** Define a glossary mapping business terms to exact technical names (e.g., "Phiếu thu/chi" ↔ `Finote`, "Cơ cấu" ↔ `OrgUnit`, "Đại diện KH" ↔ `Contact`).
2.  **Verify Identity Integrity (ID Suffixes):**
    *   `organizationId`: Multi-tenancy context boundary.
    *   `userId`: Login/Identity credentials only.
    *   `employeeId`: Internal human resource context.
    *   `contactId`: CRM customer representative.
    *   `actorId`: Exclusively used inside audit logging.
3.  **Establish Bounded Contexts:** Map domain inputs to Tier Levels:
    *   `Tier 1 - Foundation`: Business-agnostic core (`Rbac`, `AuditLog`, `Notification`).
    *   `Tier 2 - Domain Core`: Foundation models (`User`, `Employee`, `OrgStructure`). Tier 2 MUST NOT depend on Tier 3.
    *   `Tier 3 - Process Flow`: Dynamic business workflows (`CRM`, `Accounting`, `Contracts`).

---

## 🛠️ Specialized Agent Skills Orchestration
You have access to 8 custom agentic technical skills located inside `.agent/`. When working with the user in chat, you must dynamically orchestrate these workflows based on the request:

1.  **Brainstorming & Designing:** Trigger `@stax-think` (or `@stax-mindstorm` / `ka-think`) for architectural review, trade-offs, and Socratic questioning. **Strict rule: No production code or file edits are allowed during this stage.** Maintain the "Understanding Lock" gate before presenting approach options.
2.  **Full Feature Coding:** Trigger `@stax-backend` when implementing a new module or complex backend logic. Enforce the strict 4-step workflow:
    *   Step 1: Business Analysis (`00_be_analysis.md`) -> **Hard Stop (User OK)**.
    *   Step 2: Architecture & Schema Design (`01_be_implementation_plan.md`) -> **Hard Stop (User OK)**.
    *   Step 3: Tasks Checklist (`02_be_tasks.md`) -> **Hard Stop (User OK)**.
    *   Step 4: Implementation & Handoff Walkthrough (`03_be_walkthrough.md`).
3.  **Naming & Standard Auditing:** Trigger `@stax-naming-auditor` to perform a read-only audit on properties, enums, DB casing, and schemas. Generate a `02_fix_manifest.md` to hand off to development.
4.  **Micro-fixes & Hot patches:** Trigger `@stax-quick-task` for small bug fixes or auditor manifest implementation that affect **3 files or fewer** and don't modify DB schemas. Ensure changes are logged in `docs/STAX/06_CHANGELOG.md`.

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
Created automatically or manually inside `2-Processed/`:
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
Placed in `1-Journal/YYYY/MM/` with naming convention `YYYY-MM-DD-dddd.md`.
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

### 7. Interactive Knowledge Synthesis (Quy trình Tương tác Số hóa Tri thức)
When requested to perform synchronization, processing, or synthesis of raw documents under `00_raw_docs/STAX/history/` or `00_raw_docs/context/` into atomic notes:
*   **Step 1 (Diff Review):** Scan the folders and show the user a summary of changes or diffs. Do NOT trigger any LLM synthesis or file edits yet.
*   **Step 2 (Step-by-step Prompt):** Ask the user interactively, folder by folder: "Phát hiện thay đổi tại chuyên đề [{slug}]. Bạn có muốn đồng bộ (synthesis) tài liệu này không? (y/N)". Wait for user response for each file before proceeding to the next.
*   **Step 3 (Final Gate):** Display a summary of all selected folders and ask for final confirmation: "Bạn có chắc chắn muốn tiến hành gọi API để synthesis danh sách các tài liệu trên không? (y/N)".
*   **Step 4 (Execution):** Only execute the synthesis, write to `02_atomic_nodes/`, and update index/routing tables if the final confirmation is yes. Otherwise, do NOT call the API or modify any files.
