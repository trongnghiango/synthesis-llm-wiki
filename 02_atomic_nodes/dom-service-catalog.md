---
id: dom-service-catalog
title: Thiết kế Module Service Catalog
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Cấu trúc schema, DDD domain model và workflow chuyển đổi Lead-to-Contract của module Service Catalog."
tags: [service-catalog, domain-driven-design, database-schema, workflow-automation]
---

### 1. Database Schema
- `services`: Lưu danh mục dịch vụ gốc (`id`, `name`, `code`, `base_price`, `status` [active/archived]).
- `contract_items`: Snapshot dịch vụ khi ký hợp đồng (`id`, `contract_id`, `service_id`, `snapshot_price`, `description`).
- `quote_items`: Bổ sung trường `service_id` (FK) liên kết danh mục dịch vụ.

### 2. Kiến trúc DDD & Patterns
- **Domain Entity (`Service`):** Đảm nhiệm business rules về vòng đời dịch vụ (kích hoạt/lưu trữ) và cập nhật giá.
- **Infrastructure Layer:**
  - `DrizzleServiceRepository` thực thi truy vấn qua ORM, kế thừa `[[hb-drizzle-base-repo]]`.
  - `ServiceMapper` thực hiện chuyển đổi dữ liệu hai chiều (Domain Entity <=> DB Schema).

### 3. Workflow Tự động hóa: Lead to Contract
- Tích hợp logic tại `LeadWorkflowService`.
- **Trigger:** Khi trạng thái Lead cập nhật thành `WON` từ một Báo giá (`Quote`) hợp lệ.
- **Action:** 
  - Hệ thống tự động nhân bản toàn bộ `quote_items` thành các `contract_items` tương ứng của Hợp đồng mới.
  - Snapshot trực tiếp đơn giá và mô tả tại thời điểm chốt hợp đồng để đảm bảo tính bất biến của dữ liệu lịch sử.

### 4. Hệ thống API Contract
- `GET /api/crm/services`: Trả về danh sách dịch vụ active phục vụ UI Dropdown.
- `POST /api/crm/services`: Khởi tạo dịch vụ mới trong danh mục.
- `PATCH /api/crm/services/:id`: Cập nhật thuộc tính dịch vụ hoặc chuyển trạng thái sang `archived`.
- Các endpoints của Quote và Contract tự động populate mảng `items` chi tiết kèm theo.