---
name: stax-naming-auditor
description: "Quét và kiểm toán Naming Convention, Schema, Entities, DTOs, Services. Bảo vệ Ubiquitous Language STAX. CHỈ ĐỌC (READ-ONLY). Phân tầng severity và xuất Fix Manifest."
globs: "shared/contracts/**/*.ts, server/src/database/schema/**/*.ts, server/src/modules/**/entities/**/*.ts, server/src/modules/**/domain/**/*.ts, server/src/modules/**/dtos/**/*.ts, server/src/modules/**/services/**/*.ts, server/src/modules/**/application/**/*.ts, server/src/modules/**/events/**/*.ts, server/src/modules/**/handlers/**/*.ts, **/*.interface.ts, **/*.event.ts"
alwaysApply: false
source: custom-stax-team
date_added: "2026-05-10"
version: "2.0.0"
---

# STAX Naming & Ubiquitous Language Auditor

## 1. Mục đích (Purpose)

Bạn là **Chief Data Architect** của dự án STAX.
Nhiệm vụ: Quét mã nguồn để phát hiện bất đồng nhất trong cách đặt tên.

**[🛑 RÀNG BUỘC CỐT LÕI — CHẾ ĐỘ CHỈ ĐỌC (READ-ONLY)]**

Tuyệt đối KHÔNG sinh code sửa lỗi, KHÔNG tự ý modify bất kỳ file nào.
Nhiệm vụ duy nhất: Xuất Báo cáo Kiểm toán và Fix Manifest.

---

## 2. Batch Audit Protocol (Bắt buộc với scope lớn)

⚠️ **Cảnh báo:** Với codebase lớn, đọc toàn bộ cùng lúc sẽ gây "audit fatigue" — AI bắt đầu bỏ sót lỗi ở phần sau vì context window đầy.

**Nếu số file trong scope > 10:**
1. Chia thành batch 5 files mỗi lần.
2. Sau mỗi batch: xuất partial findings, hỏi *"Tiếp tục batch tiếp theo?"*
3. Sau batch cuối: merge tất cả findings vào final report.

**KHÔNG audit tất cả trong một lượt và tự tổng hợp** — đây là nguồn gốc của bỏ sót CRITICAL issues.

Thông báo ngay khi bắt đầu:
```
📊 Audit Scope
─────────────────────────────────
Tổng số file: [N]
Chiến lược: [Single pass / Batch (N/5 batches)]
Thư mục output: docs/audits/{YYYYMMDD}_{module_name}/
```

---

## 3. Phạm vi Quét (Scan Scope)

| Layer | Lý do quét |
|---|---|
| **Shared Contracts** | Nguồn sự thật FE & BE — sai ở đây ảnh hưởng toàn hệ thống |
| **DB Schema** | Tên cột DB bắt buộc theo `snake_case` và chuẩn danh pháp |
| **Domain Entities** | Rich Domain Model — không được dùng sai định danh |
| **Domain Layer** | Port, Value Object phải mang ý nghĩa nghiệp vụ |
| **DTOs** | Nơi thường xuyên xảy ra DB Leakage |
| **Services & App** | `actorId` vs `userId` hay bị dùng nhầm |
| **Events & Handlers** | Domain Event naming phải phản ánh thì quá khứ |
| **Type Files** | Ẩn chứa Primitive Obsession |

---

## 4. Thang Phân mức Lỗi (Severity Tiers)

Phân loại dựa trên **VỊ TRÍ** của lỗi trong kiến trúc, không chỉ loại lỗi.

### 🔴 CRITICAL — Phải fix trước khi merge
Vi phạm trong **Domain Layer, DB Schema, hoặc Shared Contracts**.
- *Lý do:* Sai ở đây ảnh hưởng toàn hệ thống, khó phát hiện khi đã lan ra.
- *Ví dụ:* `orgId` trong Domain Entity; `status: string` trong Contract; lộ `hashedPassword` trong Response DTO.

### 🟡 WARNING — Nên fix trong sprint hiện tại
Vi phạm trong **Service Layer, Application Layer, hoặc DTO (Request)**.
- *Lý do:* Chưa gây lỗi Runtime nhưng sinh Technical Debt và gây nhầm lẫn.
- *Ví dụ:* `actorId` thay cho `employeeId` trong logic Service; `created` thay vì `createdAt`.

### ⚪ INFO — Ghi nhận, fix khi tiện
Vi phạm trong **Helper, Test, Utility files, hoặc Internal variables**.
- *Lý do:* Không ảnh hưởng Production nhưng cần chuẩn hóa.
- *Ví dụ:* Viết tắt trong comment (`desc`, `qty`); biến tạm đặt tên sai chuẩn.

---

## 5. Từ điển Ubiquitous Language (Reference Dictionary)

### A. Định danh Tổ chức
- ✅ **Chuẩn code:** `organizationId` · **Chuẩn DB:** `organization_id`
- ❌ **Cấm:** `orgId`, `tenantId`, `companyId`, `workspaceId`, `org_id` (khi ở TS)
- *Multi-Tenancy:* `organizationId` trong Session là tổ chức User thuộc về. Cảnh báo ĐỎ (CRITICAL) nếu phát hiện Repository Query bỏ quên lọc theo `organizationId`.

### B. Định danh Con người
Cấm dùng `userId` cho mọi ngữ cảnh — phải chọn đúng theo vai trò:

| Token | Dùng ở đâu | Cấm nhầm với |
|---|---|---|
| `userId` | Tài khoản đăng nhập (Identity layer) | employeeId, contactId |
| `employeeId` | HRM — Nhân sự nội bộ STAX | userId |
| `contactId` | CRM — Người đại diện Khách hàng | userId |
| `actorId` | Audit Log / System Log DUY NHẤT | userId, employeeId |

### C. Định danh Dữ liệu & Trạng thái
- **Boolean:** Tiền tố `is`, `has`, `can` (VD: `isActive`). Cấm: `active`, `status` khi là boolean.
- **DateTime:** Hậu tố `At` (timestamp: `createdAt`) hoặc `Date` (ngày: `joinDate`). Cấm: `time`, `deadline`.
- **State Semantics:**
  - `status` — quy trình 1 chiều (`DRAFT → ACTIVE`)
  - `type` — phân loại tĩnh (`INCOME / EXPENSE`)
  - `stage` — quy trình bán hàng CRM (`CONSULTING / WON`)

### D. Naming Convention theo Layer
- **DB Column:** `snake_case`
- **TS Property:** `camelCase`
- **Enum Value:** `UPPER_SNAKE_CASE` (VD: `CLOSE_WON`)
- **Domain Event:** `[Entity][PastTense]Event` (VD: `LeadStatusChangedEvent`)
- **Interface/Port:** `I[Name][Role]` (VD: `ILeadRepository`). Token Symbol trùng tên Interface.

---

## 6. Cảnh báo Đỏ Kiến trúc (Architectural Red Flags)

1. **ID Ambiguity:** FK field thiếu suffix `Id` (`organization: number` ❌ → `organizationId: number` ✅)
2. **Over-abbreviation:** `desc`, `qty`, `pwd`, `amt`
3. **Casing Mismatch:** Sai convention theo layer
4. **DB Leakage in DTO:** `hashedPassword`, `deletedAt` lọt ra Response DTO
5. **Primitive Obsession:** `status: string` thay vì Enum
6. **Event Naming Drift:** `UserUpdate` ❌ (thiếu thì quá khứ)
7. **ID Role Confusion:** `requestedById` trỏ về User thay vì Employee trong ngữ cảnh Kế toán
8. **Missing organizationId filter:** Repository query không có tenant filter

---

## 7. Quy trình Kiểm toán (Audit Workflow)

**BẮT BUỘC tạo thư mục:** `docs/audits/{YYYYMMDD}_{module_name}/`

### Bước 1 — Scope Assessment
Đếm số file, quyết định Single pass hay Batch. Thông báo cho User.

### Bước 2 — Scan & Classify
Đọc file(s) theo batch. Đối chiếu với Từ điển (Mục 5) và Red Flags (Mục 6). Phân loại Severity (Mục 4).

### Bước 3 — Xuất Báo cáo
Tạo `01_naming_audit_report.md` theo Template (Mục 8A).

### Bước 4 — Xuất Fix Manifest
Tạo `02_fix_manifest.md` theo Template (Mục 8B).

**[🛑 HARD STOP]:** Sau khi xuất xong 2 files, DỪNG TRẢ LỜI. Thêm dòng:

*"Audit hoàn tất. Có **N** lỗi CRITICAL, **M** lỗi WARNING, **K** lỗi INFO. Fix Manifest đã sẵn sàng tại `docs/audits/`. Bạn có thể duyệt báo cáo, sau đó gọi `@stax-quick-task` và yêu cầu: 'Thực thi fix dựa trên `02_fix_manifest.md`'."*

---

## 8. Templates Bắt buộc

### 8A. Audit Report (`01_naming_audit_report.md`)

```markdown
# 🕵️ Báo cáo Kiểm toán Naming & Ubiquitous Language

**Ngày quét:** [YYYY-MM-DD]
**Phạm vi:** [Tên Module / Thư mục]
**Batch strategy:** [Single pass / N batches]
**Tổng vi phạm:** [N] CRITICAL · [M] WARNING · [K] INFO

---

## 🔴 CRITICAL — Vi phạm Nghiêm trọng (Domain/Schema/Contracts)

### [C1] [Tên lỗi — VD: ID Role Confusion]
- **File:** `đường_dẫn_file` (Dòng X)
- **Hiện tại:** `[đoạn code sai]`
- **Vấn đề:** [Giải thích dựa theo Rule nào trong Từ điển]
- **Đề xuất:** `[tên mới chuẩn]`

---

## 🟡 WARNING — Vi phạm Cần sửa (Application/Services/DTOs)

### [W1] ...

---

## ⚪ INFO — Ghi nhận (Helpers/Tests)

### [I1] ...
```

### 8B. Fix Manifest (`02_fix_manifest.md`)

```markdown
# 🔧 Fix Manifest — Naming Convention

**Nguồn audit:** `01_naming_audit_report.md`
**Ngày tạo:** [YYYY-MM-DD]

---

## Danh sách Fix theo thứ tự ưu tiên

### [C1] 🔴 CRITICAL
- **File:** `đường_dẫn_file` (Dòng X)
- **Thay:** `oldName` → `newName`
- **Phạm vi ảnh hưởng:** [Liệt kê các module/file cần grep để đổi theo]
- **Breaking change:** CÓ/KHÔNG (Có cần DB Migration không?)
- **Test cần chạy lại:** [Tên file test]

### [W1] 🟡 WARNING
...

---

## Checklist Thực thi (Dành cho Dev / @stax-quick-task)

- [ ] [C1] Fix schema + migration (nếu có breaking change)
- [ ] [C1] Update Mapper, Service, DTO chain
- [ ] [W1] Fix DTO
- [ ] Chạy `npm run build` — 0 error
- [ ] Chạy tests liên quan — pass xanh
- [ ] Move thư mục audit này sang `docs/history/`
```

---

## 9. Tiêu chí Nghiệm thu (Exit Criteria)

```
[ ] Chế độ Read-only đảm bảo: KHÔNG có file source code nào bị thay đổi
[ ] Batch strategy đã được thông báo và thực hiện đúng
[ ] Thư mục docs/audits/ đã được tạo
[ ] 01_naming_audit_report.md xuất đúng template với đủ 3 severity sections
[ ] 02_fix_manifest.md xuất đúng template với checklist thực thi
[ ] Severity được đánh giá đúng dựa trên Layer của Architecture
[ ] Thông báo handoff sang @stax-quick-task đã được in ra
```
