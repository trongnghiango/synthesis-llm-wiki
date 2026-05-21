---
id: dom-service-catalog
title: Danh mục Dịch vụ & Liên kết Hợp đồng
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Chuẩn hóa dịch vụ từ free-text sang structured data và tự động đồng bộ Quote sang Contract khi Lead WON."
tags: [service-catalog, crm, schema, ddd, workflow]
---

## 1. Database Schema
- **`services`**: Danh mục dịch vụ gốc (`id`, `name`, `status`, `base_price`,...).
- **`contract_items`**: Lưu snapshot của dịch vụ tại thời điểm ký (`contract_id`, `service_id`, `price`, `description`).
- **`quote_items`**: Bổ sung cột `service_id` liên kết ngoại tới `services`.

## 2. Domain & DDD Architecture
- **Domain Entity `Service`**: Đóng gói quy tắc nghiệp vụ `activate()`, `archive()`, `updatePrice()`.
- **Infrastructure**:
  - `DrizzleServiceRepository` kế thừa `[[hb-drizzle-base-repo]]`.
  - `ContractRepository` & `QuoteRepository`: Load/Save aggregate root cùng các items liên quan.
  - `ServiceMapper`: Chuyển đổi dữ liệu (ORM Model <-> Domain Entity).

## 3. Luồng Nghiệp vụ (Lead-to-Contract)
- **`LeadWorkflowService`**: Kích hoạt khi trạng thái Lead chuyển sang **WON**.
- **Cơ chế sao chép**: 
  - Đọc `quote_items` từ Báo giá hiện tại.
  - Snapshot và ghi đè dữ liệu trực tiếp sang `contract_items` của Hợp đồng mới.
  - Đảm bảo tính nhất quán dữ liệu lịch sử giá tại thời điểm chốt hợp đồng.

## 4. API Specification
- `GET /api/crm/services` - Lấy danh sách dịch vụ phục vụ giao diện FE chọn sẵn.
- `POST /api/crm/services` - Khởi tạo dịch vụ mới.
- `PATCH /api/crm/services/:id` - Cập nhật thông tin/trạng thái dịch vụ.