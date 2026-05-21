---
id: dom-crm-naming-migration-stage1
title: Di cư CRM Stage 1 - Đồng nhất Organization Name
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[dom-accounting-finote]]"
summary: "Chuẩn hóa schema CRM từ companyName sang organizationName, tách contacts và xử lý tương thích ngược API."
tags: [crm, database-migration, backend, refactor, drizzle]
---

## 1. Database Schema Refactoring
- **Bảng `organizations`**: Đổi tên cột `company_name` thành `organization_name`.
- **Enum `lead_source`**: Bổ sung các giá trị mới (`SOCIAL`, `ZALO`, `FACEBOOK`).
- **Bảng `leads`**:
  - Thêm `contact_id` thiết lập quan hệ 1-1 với bảng `contacts`.
  - Loại bỏ các cột thông tin liên hệ cũ: `contact_name`, `contact_email`, `contact_phone`.
- **Troubleshooting**: `drizzle-kit` gặp lỗi silent khi thực hiện đồng thời `ALTER TYPE` và `RENAME COLUMN`. Khắc phục bằng cách chạy script SQL di cư thủ công (Manual Migration). Tham khảo chuẩn migration tại `[[hb-drizzle-base-repo]]`.

## 2. Logic Nghiệp vụ & API Contracts
- **Tương thích ngược**: API DTO duy trì trả về song song `organizationName` và `companyName` (đánh dấu `@deprecated`) phục vụ Clients cũ trước khi xóa hoàn toàn ở Stage 2.
- **Tác động Services**:
  - `LeadIntakeService`: Cập nhật logic tạo mới Organization & mapping Contact.
  - `CrmLegacyMigrationService`: Khớp lại cấu trúc import dữ liệu lịch sử.
  - `IncomeTargetStrategy`: Cập nhật hiển thị tên đối tượng thuộc Module Accounting (chi tiết tại `[[dom-accounting-finote]]`).

## 3. Testing & Verification
- Cập nhật các câu lệnh SQL hardcoded trong `test-db.helper.ts` theo schema mới.
- Kết quả kiểm thử: 32/32 Unit Tests module CRM đạt trạng thái **100% PASS**.