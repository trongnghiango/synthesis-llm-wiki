---
id: dom-crm-naming-migration-stage1
title: Di cư định danh CRM Đợt 1 (Backend)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[dom-accounting-finote]]"
summary: "Chuẩn hóa Schema CRM (company_name -> organization_name, chuẩn hóa 1-1 leads-contacts) và hỗ trợ tương thích ngược API."
tags: [crm, database-migration, api-refactor, backward-compatibility]
---

## 1. Thay đổi Database & Schema (Drizzle)
- **Bảng `organizations`**: Đổi tên cột `company_name` -> `organization_name`.
- **Bảng `leads`**:
  - Thêm cột `contact_id` thiết lập quan hệ 1-1 với bảng `contacts`.
  - Drop các cột thông tin liên hệ cũ: `contact_name`, `contact_email`, `contact_phone`.
- **Enum `lead_source`**: Mở rộng thêm `SOCIAL`, `ZALO`, `FACEBOOK`.
- **Testing**: Cập nhật mock SQL trong `test-db.helper.ts` (kế thừa cấu trúc từ `[[hb-drizzle-base-repo]]`).

## 2. Domain & API Layer (Backward Compatibility)
- **Entity**: `Organization` refactor toàn bộ getter/setter sang thuộc tính `organizationName`.
- **API DTO**: Trả về song song cả `organizationName` và `companyName` (deprecated) để tránh gây lỗi cho các ứng dụng client cũ.
- **Dịch vụ ảnh hưởng**:
  - `LeadIntakeService`: Cập nhật logic khởi tạo Organization mới.
  - `CrmLegacyMigrationService`: Đồng bộ logic import dữ liệu lịch sử.
  - `IncomeTargetStrategy` (Liên kết nghiệp vụ: `[[dom-accounting-finote]]`): Cập nhật hiển thị tên đối tượng.

## 3. Sự cố & Khắc phục (Troubleshooting)
- **Vấn đề**: `drizzle-kit` gặp lỗi silent error (không in log) do xung đột giữa lệnh `ALTER TYPE` (mở rộng enum) và `RENAME COLUMN` trong cùng một phiên chạy.
- **Giải pháp**: Tách tệp migration và thực thi bằng script **Manual Migration** để đảm bảo an toàn dữ liệu.

## 4. Kế hoạch tiếp theo (Stage 2)
- Đợi team Frontend hoàn tất chuyển đổi sang dùng `organizationName`.
- Thực hiện xóa hoàn toàn trường `companyName` khỏi API DTO để làm sạch code.