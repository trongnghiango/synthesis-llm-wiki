# Implementation Plan — Shared Contracts Refactor (Phase 2)

Tái cấu trúc file "God Object" `shared/schema.ts` thành các domain-specific contracts để phục vụ mục tiêu "Source of Truth" cho cả FE và BE.

## User Review Required
> [!IMPORTANT]
> Việc tách file này sẽ làm thay đổi đường dẫn import của hầu hết các file trong dự án. Tôi sẽ sử dụng kỹ thuật "Barrel Export" tại `shared/index.ts` để giảm thiểu việc phá vỡ code hiện tại (Breaking changes).

## Proposed Changes

### 1. Cấu trúc thư mục mới
Tổ chức lại `shared/` theo domain:
- `shared/contracts/auth/auth.schema.ts`
- `shared/contracts/crm/leads.schema.ts`
- `shared/contracts/crm/quotes.schema.ts`
- `shared/contracts/hrm/employees.schema.ts`
- `shared/contracts/rbac/rbac.schema.ts`
- `shared/primitives/common.ts` (Dành cho các type dùng chung như Pagination, BaseResponse).

### 2. Chiến lược Di trú (Migration Strategy)
- **Bước A**: Tách dần từng khối code từ `shared/schema.ts` sang các file mới.
- **Bước B**: Cập nhật `shared/index.ts` để re-export tất cả từ các file mới.
- **Bước C**: Refactor dần các import ở Client và Server từ `import { ... } from "@shared/schema"` sang các sub-paths cụ thể nếu cần, hoặc giữ qua index.

### 3. Đồng bộ với Tài liệu
- Cập nhật **[api_contracts.md](../../standards/api_contracts.md)** để phản ánh đúng vị trí mới của các Schema.

## Verification Plan
- Chạy `npm run check` sau mỗi lần tách 1 domain để đảm bảo tính nhất quán của TypeScript.
- Kiểm tra Drizzle ORM (Backend) vì nó phụ thuộc trực tiếp vào các schema này.
