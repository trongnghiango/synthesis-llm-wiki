---
id: arch-crm-normalization-migration
title: Chuẩn hóa Schema CRM và Di trú Dữ liệu Leads
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Phục hồi thiết kế chuẩn hóa CRM, tách Contact/Organization khỏi Leads và thực hiện di trú dữ liệu qua Drizzle ORM."
tags: [crm, db-schema, drizzle, data-migration, domain-model]
---

### 1. Thay đổi Database Schema
- **Bảng `leads`**:
  - Loại bỏ các cột phẳng: `contact_name`, `contact_phone`, `contact_email`.
  - Bổ sung: Khóa ngoại `contact_id` (FK) liên kết tới bảng `contacts`.
  - Lưu trữ động: Gom `serviceNeed` và `note` vào trường `metadata` (JSONB) để giữ schema tinh gọn.

### 2. Thiết kế Domain & Nghiệp vụ
- **Thực thể `Lead`**:
  - Khôi phục các phương thức core: `assignTo()`, `closeAsWon()`.
  - `LeadMapper`: Ánh xạ dữ liệu ảo từ cột `metadata` JSONB thành các thuộc tính của Entity.
- **Dịch vụ `CrmLegacyMigrationService`**:
  - Luồng xử lý: Tìm/Tạo `Organization` -> Tìm/Tạo `Contact` -> Tạo `Lead` liên kết qua `contactId`.
  - Kết quả di trú: 1172 bản ghi cũ được chuẩn hóa thành công.

### 3. Tầng Persistence & API
- **`DrizzleLeadRepository.findAll`**:
  - Thực hiện `LEFT JOIN` giữa `leads` với `contacts` và `organizations`.
  - Hỗ trợ truy vấn và tìm kiếm trực tiếp trên các trường thông tin liên hệ được join.
- **API `GET /crm/leads`**:
  - Trả về payload cấu trúc phẳng chứa chi tiết liên hệ đã join: `{ id, contactId, contactName, contactPhone, ... }`.