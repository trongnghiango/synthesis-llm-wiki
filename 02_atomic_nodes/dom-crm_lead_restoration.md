---
id: dom-crm_lead_restoration
title: Chuẩn hóa Schema CRM và Di trú Lead
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Chuẩn hóa thực thể Lead qua liên kết contact_id và tối ưu hóa lưu trữ thuộc tính động bằng cột metadata JSONB."
tags: [crm, schema-normalization, drizzle, data-migration]
---

### 1. Thay đổi Database Schema
- **Bảng `leads`**:
  - Loại bỏ các cột phẳng: `contact_name`, `contact_phone`, `contact_email`.
  - Bổ sung khóa ngoại: `contact_id` (FK liên kết đến bảng `contacts.id`).
  - Metadata mở rộng: Sử dụng cột `metadata` (JSONB) để lưu trữ động trường `serviceNeed` và `note`.
- Đồng bộ hóa database bằng `drizzle-kit push`.

### 2. Thiết kế Domain & Persistence Layer
- **Lead Entity**: Khôi phục các phương thức nghiệp vụ cốt lõi `assignTo()` và `closeAsWon()`.
- **Lead Mapper**: Chuyển đổi hai chiều giữa dữ liệu DB (`contact_id`, JSONB `metadata`) và các thuộc tính ảo của Domain Entity.
- **DrizzleLeadRepository**:
  - Nâng cấp phương thức `findAll()` sử dụng `LEFT JOIN` với `contacts` và `organizations` để tối ưu hóa truy vấn thông tin liên hệ.
  - Tương thích với Base Repository tại `[[hb-drizzle-base-repo]]`.

### 3. Quy trình Di trú Dữ liệu (Migration)
- **CrmLegacyMigrationService**:
  1. Phân tích dữ liệu phẳng từ nguồn cũ để tìm hoặc tạo mới `Organization` và `Contact`.
  2. Tạo mới và liên kết thực thể `Lead` với `Contact` tương ứng thông qua `contactId`.
- **Kết quả**: Di trú và chuẩn hóa thành công 1,172 bản ghi Lead, đảm bảo toàn vẹn dữ liệu qua API `GET /crm/leads`.