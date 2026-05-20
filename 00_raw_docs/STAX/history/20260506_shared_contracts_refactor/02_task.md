# Task List — Shared Contracts Refactor

> Trạng thái: HOÀN THÀNH
> Context: Phase 2 của dự án Clean Architecture.

- [x] Phân tích `shared/schema.ts` và phân loại theo Domain.
- [x] Tạo cấu trúc thư mục `shared/contracts/`.
- [x] Khởi tạo `shared/contracts/common.ts` (Primitives).
- [x] Khởi tạo `shared/contracts/auth.ts` (Auth & Profile).
- [x] Khởi tạo `shared/contracts/crm.ts` (Leads, Quotes, Organizations).
- [x] Khởi tạo `shared/contracts/accounting.ts` (Finotes, Money).
- [x] Khởi tạo `shared/contracts/rbac.ts` (Roles).
- [x] Cấu trúc lại `shared/index.ts` (Barrel Export).
- [x] Chạy `npm run check` và sửa lỗi Import (Bao gồm cập nhật `tsconfig.json`).
