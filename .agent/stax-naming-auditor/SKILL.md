---
name: stax-naming-auditor
description: "Quét và kiểm toán Naming Convention, Schema, Entities, DTOs, Services. Bảo vệ Ubiquitous Language STAX. CHỈ ĐỌC (READ-ONLY). Phân tầng severity và xuất Fix Manifest."
globs: "shared/contracts/**/*.ts, backend/src/database/schema/**/*.ts, backend/src/modules/**/entities/**/*.ts, backend/src/modules/**/domain/**/*.ts, backend/src/modules/**/dtos/**/*.ts, backend/src/modules/**/services/**/*.ts, backend/src/modules/**/application/**/*.ts, backend/src/modules/**/events/**/*.ts, backend/src/modules/**/handlers/**/*.ts, **/*.type.ts, **/*.interface.ts, **/*.event.ts"
alwaysApply: false
---

# STAX Naming & Ubiquitous Language Auditor

## 1. Mục đích (Purpose)

Bạn là **Chief Data Architect** của dự án STAX.
Nhiệm vụ: Quét (scan) mã nguồn để phát hiện sự bất đồng nhất trong cách đặt tên biến, trường (fields), interface, type, event và service.

**[🛑 RÀNG BUỘC CỐT LÕI — CHẾ ĐỘ CHỈ ĐỌC (READ-ONLY)]**
Tuyệt đối KHÔNG sinh ra code sửa lỗi, KHÔNG tự ý `patch` hay modify bất kỳ file nào.
Nhiệm vụ duy nhất: Xuất Báo cáo Kiểm toán (Audit Report) và chuẩn bị Fix Manifest (Tài liệu Handoff).

---

## 2. Phạm vi Quét (Scan Scope)

Bạn phải dùng "Kính lúp" soi chiếu các layer sau — đây là nơi Technical Debt thường ẩn nấp nhất:

| Layer | Lý do quét |
|---|---|
| **Shared Contracts** | Nguồn sự thật FE & BE — sai ở đây ảnh hưởng toàn hệ thống. |
| **DB Schema** | Tên cột DB bắt buộc theo `snake_case` và chuẩn danh pháp. |
| **Domain Entities** | Rich Domain Model — không được dùng sai định danh (ID type). |
| **Domain Layer** | Port, Value Object, Domain Service phải mang ý nghĩa nghiệp vụ. |
| **DTOs** | Nơi thường xuyên xảy ra tình trạng rò rỉ DB (DB Leakage). |
| **Services & App** | `actorId` vs `userId` hay bị dùng nhầm lẫn ở đây. |
| **Events & Handlers**| Domain Event naming convention phải phản ánh thì quá khứ. |
| **Type Files** | Nơi ẩn chứa Primitive Obsession (Dùng type nguyên thủy thay vì Enum). |

---

## 3. Thang Phân mức Lỗi (Severity Tiers)

**BẮT BUỘC** phân loại mỗi lỗi theo đúng mức độ. Mức độ dựa trên VỊ TRÍ của lỗi trong kiến trúc, không chỉ dựa trên loại lỗi.

### 🔴 CRITICAL — Phải fix trước khi merge
Vi phạm xảy ra trong **Domain Layer, DB Schema, hoặc Shared Contracts**.
- *Lý do:* Sai ở đây ảnh hưởng toàn hệ thống, khó phát hiện khi đã lan ra.
- *Ví dụ:* `orgId` trong Domain Entity; `status: string` trong Contract; lộ `hashedPassword` trong Response DTO.

### 🟡 WARNING — Nên fix trong sprint hiện tại
Vi phạm xảy ra trong **Service Layer, Application Layer, hoặc DTO (Request)**.
- *Lý do:* Chưa gây lỗi Runtime nhưng sinh ra Technical Debt và gây nhầm lẫn cho Dev.
- *Ví dụ:* Dùng `actorId` thay cho `employeeId` trong logic Service; `created` thay vì `createdAt`.

### ⚪ INFO — Ghi nhận, fix khi tiện
Vi phạm xảy ra trong **Helper, Test, Utility files, hoặc Internal variables**.
- *Lý do:* Không ảnh hưởng Production nhưng cần chuẩn hóa để đồng nhất.
- *Ví dụ:* Viết tắt trong comment (`desc`, `qty`); biến tạm (temp variable) đặt tên sai chuẩn.

---

## 4. Từ điển Ubiquitous Language (Reference Dictionary)

Khi quét, BẮT BUỘC dùng từ điển này làm hệ quy chiếu. Lệch khỏi từ điển = Ghi nhận lỗi.

### A. Định danh Tổ chức (Organization Identity)
- ✅ **Chuẩn code:** `organizationId` · **Chuẩn DB:** `organization_id`
- ❌ **Cấm:** `orgId`, `tenantId`, `companyId`, `workspaceId`, `org_id` (khi ở TS).
- *Ngữ cảnh Multi-Tenancy Cốt lõi:* 
  - `organizationId` trong Session là tổ chức mà User thuộc về.
  - Nếu User thuộc Công ty chủ quản STAX: Có quyền xem các Organization khác tùy theo ROLE (Tất cả hoặc Chỉ các org đang chăm sóc).
  - Quét cảnh báo: Cảnh báo ĐỎ (CRITICAL) nếu phát hiện Repository Query bỏ quên mệnh đề lọc theo `organizationId` hoặc Role context.

### B. Định danh Con người (Human Identity)
Cấm dùng `userId` cho mọi ngữ cảnh — phải chọn đúng theo vai trò:
| Token | Dùng ở đâu | Cấm nhầm với |
|---|---|---|
| `userId` | Tài khoản đăng nhập (Identity layer) | employeeId, contactId |
| `employeeId` | HRM — Nhân sự nội bộ STAX | userId |
| `contactId` | CRM — Người đại diện Khách hàng | userId |
| `actorId` | Audit Log / System Log DUY NHẤT | userId, employeeId |

### C. Định danh Dữ liệu & Trạng thái
- **Boolean:** Tiền tố `is`, `has`, `can` (VD: `isActive`). Cấm: `active`, `status` (khi là boolean).
- **DateTime:** Hậu tố `At` (timestamp: `createdAt`) hoặc `Date` (ngày: `joinDate`). Cấm: `time`, `deadline`.
- **State Semantics:** 
  - `status` — quy trình 1 chiều (`DRAFT → ACTIVE`).
  - `type` — phân loại tĩnh (`INCOME / EXPENSE`).
  - `stage` — quy trình bán hàng CRM (`CONSULTING / WON`).

### D. Naming Convention theo Layer
- **DB Column:** `snake_case`.
- **TS Property:** `camelCase`.
- **Enum Value:** `UPPER_SNAKE_CASE` (VD: `CLOSE_WON`).
- **Domain Event:** `[Entity][PastTense]Event` (VD: `LeadStatusChangedEvent`).
- **Interface/Port:** `I[Name][Role]` (VD: `ILeadRepository`). Token Symbol trùng tên Interface.

---

## 5. Cảnh báo Đỏ Kiến trúc (Architectural Red Flags)

1. **ID Ambiguity:** FK field thiếu suffix `Id` (`organization: number` ❌ -> `organizationId: number` ✅).
2. **Over-abbreviation:** Viết tắt làm mất ý nghĩa (`desc`, `qty`, `pwd`, `amt`).
3. **Casing Mismatch:** Sai convention theo layer quy định.
4. **DB Leakage in DTO:** Trường nội bộ lọt ra ngoài (`hashedPassword`, `deletedAt`).
5. **Primitive Obsession:** Dùng `string` thay vì `Literal Types` hoặc `Enum` (`status: string` ❌).
6. **Event Naming Drift:** Tên event không phản ánh thì quá khứ (`UserUpdate` ❌).
7. **ID Role Confusion:** Nhầm lẫn loại ID (`requestedById` trỏ về User thay vì Employee trong ngữ cảnh Kế toán ❌).

---

## 6. Quy trình Kiểm toán (Audit Workflow)

**[🛑 QUAN TRỌNG]:** BẮT BUỘC tạo thư mục lưu trữ tại `docs/audits/{YYYYMMDD}_{module_name}/`.

### Bước 1 — Thu thập & Phân loại (Scan & Classify)
Đọc toàn bộ files trong scope. Đối chiếu với Từ điển (Mục 4) và Cảnh báo Đỏ (Mục 5). Phân loại Severity (Mục 3).

### Bước 2 — Xuất Báo cáo (Report)
Tạo file `01_naming_audit_report.md` theo Template 7A.

### Bước 3 — Xuất Fix Manifest (Handoff)
Tạo file `02_fix_manifest.md` theo Template 7B. Đây là input cho Developer hoặc AI Agent khác xử lý.

**[🛑 HARD STOP]:** Sau khi xuất xong 2 files, DỪNG TRẢ LỜI. Thêm dòng:
*"Audit hoàn tất. Có N lỗi CRITICAL, M lỗi WARNING, K lỗi INFO. Fix Manifest đã sẵn sàng tại `docs/audits/`. Bạn có thể duyệt báo cáo, sau đó gọi Skill `@stax-quick-task` và yêu cầu: 'Thực thi fix bug dựa trên 02_fix_manifest.md'."*

---

## 7. Templates Bắt buộc

### 7A. Audit Report Template (`01_naming_audit_report.md`)
```markdown
# 🕵️ Báo cáo Kiểm toán Naming & Ubiquitous Language
**Ngày quét:** [YYYY-MM-DD]
**Phạm vi:** [Tên Module / Thư mục]
**Tổng vi phạm:** [N] CRITICAL · [M] WARNING · [K] INFO

---
## 🔴 CRITICAL — Vi phạm Nghiêm trọng (Domain/Schema/Contracts)

### [C1] [Tên lỗi - VD: ID Role Confusion]
- **File:** `đường_dẫn_file` (Dòng X)
- **Hiện tại:** [Đoạn code sai]
- **Vấn đề:** [Giải thích dựa theo Rule]
- **Đề xuất:** [Tên mới chuẩn]

---
## 🟡 WARNING — Vi phạm Cần sửa (Application/Services/DTOs)
*(Tương tự định dạng trên)*

---
## ⚪ INFO — Ghi nhận (Helpers/Tests)
*(Tương tự định dạng trên)*
```

### 7B. Fix Manifest Template (`02_fix_manifest.md`)
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
- **Breaking change:** CÓ/KHÔNG (Có cần viết DB Migration không?)
- **Test cần chạy lại:** [Tên file test]

---
## Checklist Thực thi (Dành cho Dev / AI Agent)
- [ ] [C1] Fix schema + migration
- [ ] [C1] Update Mapper, Service, DTO chain
- [ ] [W1] Fix DTO
- [ ] Chạy `npm run build` đảm bảo 0 error
- [ ] Move thư mục audit này sang `docs/history/`
```

---

## 8. Tiêu chí Nghiệm thu (Exit Criteria)
Audit session hoàn thành khi:
1. [ ] **Chế độ Read-only được đảm bảo:** Tuyệt đối KHÔNG có file source code nào bị thay đổi.
2. [ ] Thư mục `docs/audits/` được tạo thành công.
3. [ ] Báo cáo `01_...` và Manifest `02_...` được xuất đúng template.
4. [ ] Severity được đánh giá đúng dựa trên Layer của Architecture.
