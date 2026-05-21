---
id: dom-crm-naming-migration-stage1
title: Đồng bộ Naming CRM Stage 1 - Backend
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Chuẩn hóa CRM naming từ companyName sang organizationName tại DB Schema và API Layer hỗ trợ tương thích ngược."
tags: [crm, migration, database-schema, backward-compatibility, backend]
---

## 1. Thay đổi Database Schema
- **Bảng `organizations`**: Đổi tên `company_name` $\rightarrow$ `organization_name`.
- **Bảng `leads`**: 
  - Thêm `contact_id` (Quan hệ 1-1 trỏ tới bảng `contacts`).
  - Xóa bỏ các trường phẳng cũ: `contact_name`, `contact_email`, `contact_phone`.
- **Enum `lead_source`**: Bổ sung các giá trị mới (`SOCIAL`, `ZALO`, `FACEBOOK`).
- **Troubleshooting**: `drizzle-kit` gặp lỗi không ghi log khi chạy đồng thời `ALTER TYPE` và `RENAME COLUMN`. Đã khắc phục bằng SQL migration script thủ công.

## 2. API Contract & Logic Layer
- **Tương thích ngược**: API Response DTO duy trì song song cả `organizationName` và `companyName` (đánh dấu `@deprecated`).
- **Tác động nghiệp vụ**:
  - `LeadIntakeService`: Cập nhật logic tạo thực thể Organization mới.
  - `CrmLegacyMigrationService`: Cập nhật logic import dữ liệu migration.
  - Phân hệ Kế toán (Liên kết: [[dom-accounting-finote]]): Cập nhật `IncomeTargetStrategy` để hiển thị đúng tên đối tượng mới.

## 3. Kế hoạch Kiểm thử & Rollout
- **Kiểm thử**: Cập nhật mock SQL trong `test-db.helper.ts`. Đảm bảo 100% (32/32) CRM Unit Tests pass.
- **Kế hoạch Stage 2**: Team Frontend hoàn tất chuyển đổi $\rightarrow$ Thực hiện xóa hoàn toàn trường `companyName` ở API DTO để làm sạch code.