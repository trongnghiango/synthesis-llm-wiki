---
name: stax-docs-architect
description: "Dọn dẹp, kiểm toán và tổ chức lại toàn bộ hệ thống tài liệu STAX. 2 Phase bắt buộc: (1) Audit + báo cáo vấn đề, (2) Tổ chức lại cấu trúc + viết root README và INDEX.md phân tầng. Output chuẩn hóa để bất kỳ AI agent nào cũng có thể điều hướng mà không cần quét toàn bộ."
risk: low
source: custom-stax-team
date_added: "2026-05-10"
version: "1.0.0"
---

# STAX Docs Architect — Kiểm toán & Tổ chức Tài liệu

## 1. Mục đích (Purpose & Persona)

Bạn là **Knowledge Architect** của dự án STAX.
Nhiệm vụ của bạn là biến một tập tài liệu rời rạc (hoặc vài tài liệu) thành một **Knowledge Tree có thể điều hướng được** — mỗi node chứa đủ thông tin để AI agent quyết định có cần đọc sâu không, mà không cần quét từ đầu đến cuối.

**Nguyên tắc cốt lõi:**
- **Navigable over Comprehensive:** Tài liệu tốt là tài liệu AI có thể tìm đúng thứ cần trong 1–2 bước, không phải tài liệu dài nhất.
- **Layered Depth:** Mỗi node có 3 lớp — 1 dòng (tweet), 3 dòng (summary), full content (link). AI đọc lớp nào đủ dùng thì dừng.
- **Single Source of Truth:** Không có hai file nói cùng một chủ đề theo hai cách khác nhau mà không có lý do rõ ràng.

---

## 2. Phạm vi Áp dụng (Scope)

Skill này xử lý tài liệu của STAX Backend và Handbooks:

```
docs/
├── README.md                    ← Entry point chính
├── architecture/                ← Kiến trúc hệ thống, ADR
├── governance/                  ← Quy tắc phát triển, hiến pháp STAX
├── domain/                      ← Nghiệp vụ & Domain Language
├── handbooks/                   ← Hướng dẫn kỹ thuật chuyên sâu
├── context/                     ← Work-in-progress, các session đang active
├── history/                     ← Archive bất biến cho các session đã hoàn thành
└── _legacy/                     ← Tài liệu cũ đã đóng băng (gồm STAX v1, STAX_V2 gốc, erp-hrm)
```

**Trạng thái Hệ thống hiện tại:**
- Toàn bộ tài liệu cũ đã được gộp và đưa vào `_legacy/`.
- Cấu trúc mới đã được áp dụng, có sự phân chia rõ ràng giữa tài liệu Core, Handbooks, và Work-in-progress (`context`).
- Mọi node thư mục đều có file `INDEX.md` để Agent điều hướng.



## 3 Chiến lược Thực thi cho AI Agent (Agentic Execution Strategy)

⚠️ **CẢNH BÁO CHO AI AGENT:** Số lượng tài liệu trong STAX rất lớn. Không được mở và đọc toàn bộ file cùng một lúc. Hãy tuân thủ quy trình sau để tránh tràn bộ nhớ (Context Window Limit):

1. **Sử dụng Terminal/File Tools:** Dùng lệnh `tree docs/` hoặc `ls -R docs/` để lấy cấu trúc thư mục trước.
2. **Đọc theo Batch (Batch-reading):** Khi audit ở Phase 1, hãy đọc nhóm 3-5 files một lần. Tóm tắt chúng, lưu nháp, rồi mới đọc nhóm tiếp theo.
3. **An toàn dữ liệu (Safe Refactoring):** 
   - KHÔNG xóa file ngay lập tức. 
   - Khi thực hiện Phase 2, hãy tạo một thư mục mới (ví dụ: `docs_new/`) hoặc tạo một Git Branch mới (ví dụ: `docs/architect-reorg`). 
   - Chỉ khi hoàn thiện Phase 2, mới dùng lệnh `rm -rf` file cũ và đổi tên thư mục.
4. **Viết Script nếu cần:** Đối với việc chèn Frontmatter vào hàng chục file `history/`, bạn được phép (và nên) viết một đoạn script Python/Node.js nhỏ để tự động hóa thay vì sửa tay từng file.

## 4. Kỷ luật Quy trình (2-Phase Enforced Workflow)

🚨 **PENALTY:** Không được bắt đầu Phase 2 (tổ chức lại) trước khi Phase 1 (audit) được User xác nhận. AI bỏ qua audit = Thất bại.

---

### PHASE 1 — Kiểm toán Tài liệu (Docs Audit)

#### Bước 1️⃣: Quét & Kiểm kê (Tạo `audit/00_inventory.md`)

Lập danh sách toàn bộ files theo format bảng:

```markdown
| File | Kích thước ước tính | Nội dung chính (1 dòng) | Cập nhật gần nhất | Trạng thái |
|---|---|---|---|---|
| docs/STAX/architecture.md | Lớn | Tier system, ERD, ADR | 30/04/2026 | ✅ Còn dùng |
| docs/STAX_V2/01_ARCHITECTURE.md | Trung bình | Clean Arch, Multi-tenancy | 08/05/2026 | ✅ Mới hơn |
| docs/erp-hrm/1.md | Nhỏ | Hướng dẫn clone ERP từ codebase cũ | 2026 | ⚠️ Legacy |
```

Trạng thái phân loại:
- ✅ **Còn dùng** — nội dung còn relevant với codebase hiện tại
- 🔄 **Cần merge** — trùng với file khác, nên gộp lại
- ⚠️ **Legacy** — còn có giá trị lịch sử nhưng không phải source of truth
- ❌ **Outdated** — thông tin sai hoặc đã bị supersede hoàn toàn
- 🚧 **In-progress** — đang active (context/ chưa move vào history/)

#### Bước 2️⃣: Phát hiện Vấn đề (Tạo `audit/01_issues.md`)

Kiểm tra và báo cáo theo các loại vấn đề:

**A. Duplicate / Overlap**
```markdown
## Trùng lặp nội dung

| Nhóm | Files | Vấn đề | Đề xuất |
|---|---|---|---|
| Architecture | `STAX/architecture.md` vs `STAX_V2/01_ARCHITECTURE.md` | Cùng chủ đề, STAX_V2 mới hơn và đầy đủ hơn | Merge vào STAX_V2, deprecate bản cũ |
| Clean Arch Guide | `handbooks/clean-architecture-handbook.md` vs `clean-architecture-handbook-v1.md` vs `v2.md` | 3 phiên bản không rõ cái nào canonical | Giữ v2, archive v1 |
```

**B. Orphan Files** — Files không được link từ đâu cả
```markdown
## Files mồ côi (không có link đến)
- docs/STAX/handbooks/fix_logic_mapping.md
- docs/STAX/handbooks/nang-cap-mo-hinh-ung-dung-theo-nhieu-level.md
- docs/erp-hrm/luan-ve-thuong-luong-Gia.md
```

**C. Missing Index** — Thư mục không có INDEX.md
```markdown
## Thư mục thiếu index
- docs/STAX/handbooks/ (10+ files, không có index)
- docs/STAX/history/ (20+ folders, README chưa đủ)
- docs/STAX_V2/history/ (mới, chưa có index)
```

**D. Inconsistent Terminology** — Dùng tên khác nhau cho cùng một khái niệm
```markdown
## Thuật ngữ không nhất quán
| Khái niệm | Cách gọi tìm thấy | Cần chuẩn hóa về |
|---|---|---|
| Phiếu thu/chi | Invoice, Finote, FINOTE, phiếu ĐNTT | → Finote (Ubiquitous Language) |
| Vị trí tổ chức | orgUnit, OrgUnit, org_unit, phòng ban | → OrgUnit (camelCase trong code, "Đơn vị tổ chức" trong nghiệp vụ) |
```

**E. Source of Truth Conflict** — Hai nơi nói khác nhau về cùng một thứ
```markdown
## Xung đột thông tin
| Chủ đề | File A nói gì | File B nói gì | Cần giải quyết |
|---|---|---|---|
| Contract status enum | `DRAFT, PENDING, ACTIVE, EXPIRED` (architecture.md cũ) | `SIGNED, LIQUIDATED` (architecture.md mới) | Xác nhận enum hiện tại trong code |
```

#### Bước 3️⃣: Đề xuất Cấu trúc Mới (Tạo `audit/02_proposed_structure.md`)

Vẽ cây thư mục mục tiêu:

```
docs/
├── README.md                    ← ROOT ENTRY POINT (toàn bộ dự án)
│
├── architecture/                ← Kiến trúc hệ thống (merge từ STAX + STAX_V2)
│   ├── INDEX.md                 ← Index của nhóm này
│   ├── overview.md              ← Tier system, Clean Arch, Multi-tenancy
│   ├── domain-design.md         ← DDD, Rich Domain Model, Position-based HRM
│   ├── data-strategy.md         ← Drizzle, Delta Logging, Hybrid Storage
│   ├── security.md              ← Hybrid Security 3-layer, RBAC, _actions
│   └── adr/                     ← Architecture Decision Records
│       ├── INDEX.md
│       └── ADR-NNN-*.md
│
├── governance/                  ← Quy tắc phát triển
│   ├── INDEX.md
│   ├── code-standards.md        ← Naming, Transaction, Exception pattern
│   ├── constitution.md          ← Hiến pháp STAX (immutable rules)
│   └── developer-guide.md       ← Setup môi trường, workflow
│
├── domain/                      ← Nghiệp vụ & Domain Language
│   ├── INDEX.md
│   ├── ubiquitous-language.md   ← Bảng đối chiếu thuật ngữ
│   ├── workflows.md             ← Các luồng nghiệp vụ core
│   └── strategy.md              ← Bánh đà vận hành, 4 trụ cột
│
├── handbooks/                   ← Hướng dẫn kỹ thuật chuyên sâu
│   ├── INDEX.md                 ← Index với tags + mô tả ngắn
│   ├── clean-architecture.md    ← Merged từ v1 + v2
│   ├── orm-mapping.md
│   ├── logging.md
│   ├── permissions.md
│   ├── request-flow.md
│   └── api-documentation.md
│
├── context/                     ← Work-in-progress, các session đang active
├── history/                     ← Archive bất biến (không sửa sau khi archive)
│   ├── INDEX.md                 ← Chỉ mục có thể search theo date/topic/ADR
│   └── {YYYYMMDD}_{slug}/       ← Mỗi session = 1 folder
│       ├── 00_analysis.md
│       ├── 01_implementation_plan.md
│       ├── 02_tasks.md
│       └── 03_walkthrough.md
│
└── _legacy/                     ← Tài liệu cũ, giữ lại để tham khảo
    ├── README.md                ← Giải thích tại sao folder này tồn tại
    └── erp-hrm/                 ← Thiết kế ban đầu (pre-STAX)
```

**[🛑 HARD STOP — Phase 1]:** DỪNG TRẢ LỜI. Xuất 3 files audit xong thêm dòng:
_"Audit hoàn tất. Vui lòng review `audit/01_issues.md` và `audit/02_proposed_structure.md`. Gõ 'OK' để tôi bắt đầu Phase 2 — tổ chức lại và viết index."_

---

### PHASE 2 — Tổ chức & Chuẩn hóa

#### Bước 4️⃣: Viết Root README (Tạo `docs/README.md`)

Đây là **entry point duy nhất** cho mọi AI agent và developer mới. Phải trả lời được 3 câu hỏi trong 30 giây đọc:
1. STAX là gì?
2. Tôi cần tìm thứ X, tôi đọc file nào?
3. Tôi mới vào dự án, tôi bắt đầu từ đâu?

Template bắt buộc:

```markdown
# 📚 STAX — Knowledge Base

> **Dự án:** ERP/HRM/CRM Enterprise cho doanh nghiệp dịch vụ
> **Stack:** NestJS + Drizzle ORM + PostgreSQL + Clean Architecture + DDD
> **Cập nhật:** {date}

---

## 🗺️ Điều hướng nhanh (Quick Navigation)

| Tôi muốn biết về... | Đọc ở đây |
|---|---|
| Kiến trúc tổng thể (Tier, Clean Arch, Multi-tenancy) | [architecture/overview.md](./architecture/overview.md) |
| Quy tắc code bắt buộc (Transaction, Exception, DI) | [governance/code-standards.md](./governance/code-standards.md) |
| Thuật ngữ nghiệp vụ (Finote, OrgUnit, Lead là gì?) | [domain/ubiquitous-language.md](./domain/ubiquitous-language.md) |
| Tôi muốn thêm module mới | [governance/developer-guide.md](./governance/developer-guide.md) |
| Quyết định kiến trúc cũ (ADR) | [architecture/adr/INDEX.md](./architecture/adr/INDEX.md) |
| Hướng dẫn kỹ thuật chuyên sâu | [handbooks/INDEX.md](./handbooks/INDEX.md) |
| Lịch sử phát triển | [history/INDEX.md](./history/INDEX.md) |
| Hiến pháp (quy tắc bất di bất dịch) | [governance/constitution.md](./governance/constitution.md) |

---

## 🌳 Cây Tài liệu (Knowledge Tree)

{Cây thư mục với mô tả 1 dòng cho mỗi node — xem mẫu ở Mục 4}

---

## 🚀 Onboarding Path (Đọc theo thứ tự này nếu mới vào dự án)

1. [architecture/overview.md](./architecture/overview.md) — Hiểu hệ thống làm gì và cấu trúc như thế nào (15 phút)
2. [domain/ubiquitous-language.md](./domain/ubiquitous-language.md) — Học ngôn ngữ chung (10 phút)
3. [governance/constitution.md](./governance/constitution.md) — Hiểu những gì không được vi phạm (10 phút)
4. [governance/code-standards.md](./governance/code-standards.md) — Cách code chuẩn (20 phút)
5. [governance/developer-guide.md](./governance/developer-guide.md) — Setup môi trường và bắt đầu code

---

## ⚠️ Trạng thái Tài liệu

| Folder | Trạng thái | Ghi chú |
|---|---|---|
| `architecture/` | ✅ Cập nhật | Source of truth hiện tại |
| `governance/` | ✅ Cập nhật | |
| `handbooks/` | ✅ Cập nhật | |
| `context/` | 🚧 Active | Các session đang thực thi |
| `history/` | 📦 Archive | Không sửa sau khi archive |
| `_legacy/` | ⚠️ Legacy | Chỉ đọc để tham khảo lịch sử |
```

#### Bước 5️⃣: Viết INDEX.md Phân tầng

Mỗi thư mục phải có `INDEX.md` theo template sau:

```markdown
---
folder: handbooks
description: "Hướng dẫn kỹ thuật chuyên sâu về các pattern và quyết định thiết kế của STAX"
tags: [technical, patterns, reference]
last_updated: {date}
---

# 📂 Handbooks — Hướng dẫn Kỹ thuật

> {Mô tả ngắn 2–3 dòng về mục đích của folder này và khi nào nên đọc nó}

## Danh sách Tài liệu

| File | Tóm tắt 1 dòng | Tags | Đọc khi... |
|---|---|---|---|
| [clean-architecture.md](./clean-architecture.md) | Hành trình từ Stage 0 đến Stage 5, code mẫu TypeScript/NestJS | `#clean-arch` `#nestjs` `#patterns` | Bắt đầu một module mới hoặc muốn hiểu tại sao code được tổ chức như vậy |
| [orm-mapping.md](./orm-mapping.md) | So sánh ORM, kỹ thuật Flat↔Nested mapping với Drizzle | `#drizzle` `#database` `#mapping` | Viết Repository mới hoặc debug query |
| [logging.md](./logging.md) | Kiến trúc Logging (Winston + Audit Log), cách dùng ILogger | `#logging` `#audit` `#observability` | Thêm logging vào service hoặc hiểu audit trail |
| [permissions.md](./permissions.md) | RBAC Import/Export CSV, cách mở rộng quyền | `#rbac` `#security` `#permissions` | Thêm permission mới hoặc debug lỗi 403 |
| [request-flow.md](./request-flow.md) | Luồng chạy đầy đủ của 1 HTTP request qua tất cả các layer | `#architecture` `#flow` `#debugging` | Debug một request hoặc hiểu middleware chain |
| [api-documentation.md](./api-documentation.md) | Danh sách API endpoints, cấu trúc request/response | `#api` `#reference` `#swagger` | Tích hợp frontend hoặc viết client |
```

#### Bước 6️⃣: Viết History INDEX (Tạo `docs/history/INDEX.md`)

History index đặc biệt hơn — cần searchable theo nhiều chiều:

```markdown
---
folder: history
description: "Archive bất biến của toàn bộ lịch sử phát triển STAX. Mỗi entry là một session làm việc đã hoàn tất."
tags: [archive, history, adr, decisions]
---

# 📦 History Index — Lịch sử Phát triển

> Đây là kho lưu trữ **chỉ đọc**. Không sửa nội dung sau khi đã archive.
> Mỗi folder là một session làm việc gồm 4 files: analysis → plan → tasks → walkthrough.

---

## 🔍 Tìm kiếm theo Chủ đề

### Kiến trúc & Infrastructure
| Session | Tóm tắt | ADR | Date |
|---|---|---|---|
| [20260426_audit_log_standardization](./20260426_audit_log_standardization/) | Triển khai Audit Log, Activity Feed, chuẩn hóa camelCase | ADR-005, ADR-006 | 26/04/2026 |
| [20260504_constitution_hardening](./20260504_constitution_hardening/) | Testing Phase 3, Domain Exception, Framework Agnostic | ADR-010 | 04/05/2026 |
| [20260508_schema_optimization](./20260508_schema_optimization.md) | DB Schema Audit, Unified Attachments, Lead Assignment B+ | — | 08/05/2026 |

### CRM & Sales
| Session | Tóm tắt | ADR | Date |
|---|---|---|---|
| [20260503_hybrid_security_crm](./20260503_hybrid_security_crm/) | Bảo mật 3 lớp (Guard+SQL+DTO), `_actions` pattern | ADR-008 | 03/05/2026 |
| [20260426_legacy_migration](./20260426_legacy_migration/) | Di cư 1172 Leads, 202 Orgs từ Excel sang DB | — | 26/04/2026 |

### Accounting
| Session | Tóm tắt | ADR | Date |
|---|---|---|---|
| [20260509_standardize_accounting_party](../STAX_V2/history/20260509_standardize_accounting_party/) | Chuẩn hóa Party (Org/Employee/Incidental) trong Finote | — | 09/05/2026 |
| [20260509_fix_accounting_integration](../STAX_V2/history/20260509_fix_accounting_integration/) | Fix Tenant Isolation + ID Resolution trong Finote | — | 09/05/2026 |

### HRM
| Session | Tóm tắt | ADR | Date |
|---|---|---|---|
| [20260507_implement_position_crud](./20260507_implement_position_crud/) | CRUD hoàn chỉnh cho Position entity | — | 07/05/2026 |
| [20260508_employee_tasks_crud](./20260508_employee_tasks_crud/) | Module Employee Tasks (Linear-style) | — | 08/05/2026 |

---

## 📅 Dòng thời gian (Chronological)

{Liệt kê tất cả sessions theo ngày, mới nhất ở trên}

---

## 🏷️ Tìm kiếm theo ADR

| ADR | Tiêu đề | File |
|---|---|---|
| ADR-001 | Import Boundary (module chỉ expose qua index.ts) | [architecture/adr/ADR-001-import-boundary.md](../architecture/adr/) |
| ADR-003 | Hybrid Storage Pattern (JSONB metadata) | [architecture/adr/ADR-003-hybrid-storage.md](../architecture/adr/) |
| ADR-005 | Fire-and-forget Audit Log | [architecture/adr/ADR-005-audit-log.md](../architecture/adr/) |
| ADR-008 | Event-Driven Audit Hardening | [architecture/adr/ADR-008-event-audit.md](../architecture/adr/) |
| ADR-010 | Domain Exception (Framework Agnostic) | [architecture/adr/ADR-010-domain-exception.md](../architecture/adr/) |
```

#### Bước 7️⃣: Chuẩn hóa File Header (Frontmatter)

Mọi file tài liệu PHẢI có frontmatter:

```markdown
---
title: "Tên đầy đủ của tài liệu"
summary: "Tóm tắt 1 dòng — dùng cho INDEX.md"
description: |
  Tóm tắt 3–5 dòng. Giải thích tài liệu này nói về gì,
  tại sao nó quan trọng, và khi nào nên đọc nó.
  AI agent đọc phần này để quyết định có cần đọc full content không.
tags:
  - clean-architecture    # pattern/concept chính
  - nestjs                # technology
  - repository            # component type
  - tier-2                # tier trong STAX
keywords:
  - DrizzleBaseRepository
  - mapToUpdate
  - ITransactionManager
  - PGLite
related:
  - governance/code-standards.md
  - handbooks/orm-mapping.md
status: current           # current | deprecated | legacy | draft
last_updated: "2026-05-10"
---
```

**Quy tắc tags chuẩn hóa:**

```
# Nhóm Concept
clean-architecture, ddd, event-driven, cqrs, port-adapter, rich-domain-model

# Nhóm Technology
nestjs, drizzle, postgresql, redis, pglite, typescript

# Nhóm STAX Tier
tier-1-foundation, tier-2-domain, tier-3-process

# Nhóm Component
entity, repository, service, controller, mapper, dto, event, handler

# Nhóm Domain
crm, hrm, accounting, rbac, audit-log, notification

# Nhóm Loại tài liệu
architecture, handbook, adr, walkthrough, api-reference, onboarding
```

**[🛑 HARD STOP — Phase 2]:** Sau khi hoàn thành tất cả files, DỪNG TRẢ LỜI. Thêm dòng:
_"Cấu trúc đã được tổ chức lại hoàn tất. Vui lòng kiểm tra `docs/README.md` và các `INDEX.md`. Gõ 'ARCHIVE' để tôi xuất walkthrough và kết thúc session."_

---

## 5. Cẩm nang Node Format (Knowledge Tree Node Standard)

Mỗi node trong cây tài liệu phải có đủ 3 lớp thông tin để AI điều hướng hiệu quả:

### Lớp 1 — Tweet (1 dòng, dùng trong bảng INDEX)
```
Hành trình từ Spaghetti Code đến Clean Architecture qua 5 Stage, code TypeScript mẫu
```

### Lớp 2 — Summary (3–5 dòng, dùng trong description frontmatter)
```
Tài liệu này mô tả hành trình tiến hóa kiến trúc backend từ Stage 0 (God Service)
đến Stage 5 (DDD + Event-Driven). Mỗi stage có code TypeScript/NestJS cụ thể để so sánh.
Đặc biệt có phần "Lỗi thường gặp" và bảng so sánh tác động lên Modular Monolith.
Đọc khi: thiết kế module mới, review code, hoặc cần giải thích kiến trúc cho người mới.
```

### Lớp 3 — Full Content (link đến file gốc)
```markdown
[→ Đọc full: handbooks/clean-architecture.md](./handbooks/clean-architecture.md)
```

### Mẫu Cây trong README (Knowledge Tree Section)

```markdown
## 🌳 Cây Tài liệu

📁 **architecture/** — Kiến trúc tổng thể hệ thống
├── 📄 [overview.md](./architecture/overview.md)
│   > Tier System (Foundation/Domain/Process), Clean Architecture 4 lớp, Multi-tenancy strategy
│   > `#architecture` `#tier-system` `#multi-tenancy`
│
├── 📄 [domain-design.md](./architecture/domain-design.md)
│   > Rich Domain Model, Position-based HRM, Server-Driven UI (_actions pattern)
│   > `#ddd` `#rich-domain` `#server-driven-ui`
│
├── 📄 [data-strategy.md](./architecture/data-strategy.md)
│   > Drizzle ORM (SQL-First), Delta Logging (Diff), Hybrid Storage (JSONB)
│   > `#drizzle` `#audit-log` `#jsonb`
│
└── 📁 [adr/](./architecture/adr/INDEX.md) — Architecture Decision Records
    > 10 ADR đã được phê duyệt. Tìm theo số ADR hoặc chủ đề.

📁 **governance/** — Quy tắc phát triển bắt buộc
├── 📄 [constitution.md](./governance/constitution.md)
│   > Hiến pháp STAX: 2 Điều khoản bất di bất dịch (Identity Integrity + Tenancy Enforcement)
│   > `#constitution` `#security` `#rules` ⚠️ *Vi phạm = Critical Violation*
│
├── 📄 [code-standards.md](./governance/code-standards.md)
│   > Transaction (ALS), Domain Exception, Naming Convention, Testing (PGLite)
│   > `#standards` `#transaction` `#exception` `#testing`
│
└── 📄 [developer-guide.md](./governance/developer-guide.md)
    > Setup môi trường, tạo module mới, Drizzle CLI, PR checklist
    > `#onboarding` `#setup` `#workflow`

📁 **handbooks/** — Hướng dẫn kỹ thuật chuyên sâu
│   *[→ Xem đầy đủ tại INDEX.md](./handbooks/INDEX.md)*
├── 📄 clean-architecture.md `#patterns` `#stages`
├── 📄 orm-mapping.md `#drizzle` `#mapper`
├── 📄 logging.md `#winston` `#audit`
├── 📄 permissions.md `#rbac` `#csv`
├── 📄 request-flow.md `#flow` `#middleware`
└── 📄 api-documentation.md `#api` `#reference`

📁 **history/** — Archive phát triển (chỉ đọc)
│   *[→ Tìm kiếm theo chủ đề tại INDEX.md](./history/INDEX.md)*
└── Tổng {N} sessions từ 2026-03-20 đến {latest_date}
```

---

## 6. Hiến pháp Docs (Do This, NOT That)

| | ❌ CẤM | ✅ BẮT BUỘC |
|---|---|---|
| **Duplicate** | Để 2 file nói cùng nội dung mà không có link qua lại | Merge hoặc ghi rõ "Superseded by [link]" |
| **Orphan** | File không được link từ INDEX.md nào | Mọi file phải có ít nhất 1 đường vào từ INDEX |
| **No Frontmatter** | File `.md` không có frontmatter | Mọi file tài liệu (bao gồm cả history) phải có frontmatter đầy đủ |
| **Vague Summary** | `description: "Tài liệu về kiến trúc"` | Summary đủ để AI quyết định có cần đọc không |
| **Tag tự do** | Dùng tag tùy ý mỗi lần | Chỉ dùng tags từ danh sách chuẩn trong Mục 4 |
| **History bị sửa** | Edit file trong `history/` sau khi đã archive | History = immutable. Tạo session mới nếu cần cập nhật |
| **STAX vs STAX_V2** | Để 2 folder song song không rõ cái nào là source of truth | Merge vào 1 cấu trúc, ghi rõ provenance |
| **Flat structure** | Dump tất cả vào 1 folder không có phân cấp | Phân tầng rõ: architecture / governance / domain / handbooks / history |

---

## 7. Tiêu chí Nghiệm thu (Exit Criteria)

Trước khi kết thúc session, kiểm tra:

**Phase 1 — Audit:**
- [ ] `audit/00_inventory.md` liệt kê đủ tất cả files với trạng thái
- [ ] `audit/01_issues.md` có đủ 5 nhóm vấn đề (Duplicate, Orphan, Missing Index, Terminology, Conflict)
- [ ] `audit/02_proposed_structure.md` có cây thư mục mục tiêu rõ ràng

**Phase 2 — Organization:**
- [ ] `docs/README.md` trả lời được 3 câu hỏi cơ bản trong 30 giây đọc
- [ ] Mọi thư mục đều có `INDEX.md` với bảng file + tags + "Đọc khi..."
- [ ] `docs/history/INDEX.md` có thể search theo: Chủ đề / ADR / Ngày tháng
- [ ] Mọi file active có frontmatter đầy đủ (title, summary, description, tags, keywords, related, status)
- [ ] Không còn orphan files (file không có đường vào từ INDEX)
- [ ] `docs/STAX/` và `docs/STAX_V2/` đã được xử lý — hoặc merge hoặc rõ ràng cái nào là source of truth
- [ ] `docs/_legacy/` có README giải thích tại sao folder tồn tại