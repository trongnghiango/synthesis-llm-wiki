---
id: hb-stax-safe-update-pattern
title: Mẫu Thiết Kế Safe-Update Trong Drizzle Repository
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Giải pháp Safe-Update tự động loại bỏ các trường bất biến (id, organizationId,...) khi cập nhật dữ liệu qua Drizzle Repository."
tags: [drizzle, repository, safe-update, data-security, refactoring]
---

## 1. Vấn Đề
Lỗi `Database Update Constraint Violation` xảy ra khi cập nhật thực thể chứa các trường bất biến hoặc khóa chính, gây vi phạm ràng buộc dữ liệu nghiêm trọng.

## 2. Giải Pháp: Safe-Update Pattern
Tích hợp phương thức `mapToUpdate` vào lớp cơ sở `DrizzleBaseRepository` (chi tiết tại `[[hb-drizzle-base-repo]]`).

### Cơ chế hoạt động
Tự động lọc bỏ các trường bất biến khỏi payload trước khi thực thi câu lệnh `UPDATE`:
- **Khóa chính & Metadata:** `id`, `createdAt`
- **Ràng buộc cô lập Tenant:** `organizationId`, `sourceOrgId` (đảm bảo an toàn theo `[[arch-als-tenant-isolation]]`)

### Các Repositories đã áp dụng
- **CRM:** `Organization`, `Lead`, `Contact`, `Quote`
- **HRM:** `Employee`
- **Core:** `User`, `Notification`
- **Accounting:** `Finote` (chi tiết tại `[[dom-accounting-finote]]`)

## 3. Kiểm Thử & Xác Minh
- **Môi trường:** PGLite Integration Test.
- **Kết quả:** `DrizzleOrganizationRepository.save (UPDATE)` và toàn bộ suite (6/6 tests) hoạt động chính xác (**PASS**).