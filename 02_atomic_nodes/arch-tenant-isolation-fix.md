---
id: arch-tenant-isolation-fix
title: Cơ chế Cô lập Tenant cho CRM & Accounting
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[arch-als-tenant-isolation]]"
summary: "Nâng cấp applyTenantIsolation trong Drizzle Base Repository nhằm tự động hóa việc cô lập dữ liệu theo tổ chức cho các module CRM, HRM, Accounting và System."
tags: [tenant-isolation, drizzle-orm, multi-tenancy, repository-pattern]
---

## 1. Cơ Chế Cô Lập Cốt Lõi (Base Repository Upgrade)
- Cập nhật hàm `applyTenantIsolation` trong `[[hb-drizzle-base-repo]]`:
  - Thêm cơ chế kiểm tra đặc hiệu: `'organizationName' in table` để nhận diện bảng `organizations`.
  - Tự động ánh xạ tenant isolation key vào trường khóa chính `id` đối với thực thể Organization, thay vì dùng trường ngoại khóa `tenantId`/`organizationId` thông thường.

## 2. Phạm Vi Tích Hợp Repository
Áp dụng bộ lọc cô lập tenant tự động trên tất cả các phương thức truy vấn (`findAll`, `findById`, `count`, và các finder đặc thù):
- **CRM**: `DrizzleOrganizationRepository`, `DrizzleLeadRepository`, `DrizzleQuoteRepository`, `DrizzleContactRepository`, `DrizzleAssignmentRepository`.
- **HRM**: `DrizzleEmployeeRepository`, `DrizzleEmployeeTaskRepository`, `DrizzleOrgStructureRepository`.
- **Accounting (`[[dom-accounting-finote]]`)**: `DrizzleFinoteRepository`, `DrizzleCashFundRepository`, `DrizzleAccountRepository`, `DrizzleJournalRepository`, `DrizzleFinotePaymentRepository`.
- **System**: `DrizzleAttachmentRepository`, `DrizzleNotificationRepository`.

## 3. Thiết Kế Nghiệp Vụ & Ràng Buộc
- **ALS Context**: Mọi truy vấn từ luồng request của người dùng bắt buộc phải phân giải `tenantId` thông qua `[[arch-als-tenant-isolation]]`.
- **Bypass Rule**: Chỉ cho phép bỏ qua cô lập tenant (bypass isolation) đối với các tiến trình chạy nền hệ thống (System/Cron jobs) được cấu hình tường minh.