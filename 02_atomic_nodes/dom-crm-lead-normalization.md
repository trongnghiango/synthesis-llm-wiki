---
id: dom-crm-lead-normalization
title: Chuẩn hóa Schema CRM & Di trú dữ liệu Lead
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Chuẩn hóa thực thể Lead bằng cách liên kết Contact qua contact_id và di trú thành công 1172 records kế thừa."
tags: [crm, database-normalization, drizzle, lead-migration]
---

## 1. Cấu trúc Schema & Thiết kế Domain mới
- **Bảng `leads` (Database)**:
  - Loại bỏ các cột trực tiếp: `contact_name`, `contact_phone`, `contact_email`.
  - Thêm khóa ngoại: `contact_id` (FK -> bảng `contacts`).
  - Cột `metadata` (JSONB): Lưu trữ động `serviceNeed` và `note` để tối ưu hóa schema.
- **Thực thể `Lead` (Domain Layer)**:
  - Khôi phục các phương thức nghiệp vụ: `assignTo()`, `closeAsWon()`.
  - `LeadMapper`: Ánh xạ trường ảo từ thuộc tính `metadata` JSONB sang Object Model.

## 2. Persistence & Dịch vụ Di trú
- **`DrizzleLeadRepository`**:
  - Cập nhật phương thức `findAll()` thực hiện `LEFT JOIN` với `contacts` và `organizations`.
  - Hỗ trợ truy vấn tìm kiếm trực tiếp trên dữ liệu liên kết của Contact.
- **`CrmLegacyMigrationService`**:
  - Luồng xử lý: Tìm/Tạo `Organization` & `Contact` trước -> Tạo `Lead` liên kết với `contactId`.
  - Kết quả: Di trú thành công 1172 leads cũ, tự động liên kết Contact tương ứng.

## 3. API Contract & Xác thực
- **API `GET /crm/leads`**: Trả về danh sách Lead kèm thông tin phẳng từ bảng Contact liên kết (`contactName`, `contactPhone`).
- **Kiểm thử**: Đạt 100% build thành công (`npx tsc --noEmit` pass không lỗi).