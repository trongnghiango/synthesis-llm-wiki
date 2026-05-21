---
id: dom-crm-activity-feed-metadata
title: Thiết kế Activity Feed và Structured Metadata cho CRM
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
summary: "Chuẩn hóa cơ chế Activity Feed, Audit Trail và liên kết dữ liệu Timeline đa thực thể (Lead, Org, Contract) tích hợp Actor Tracking."
tags: [crm, activity-feed, audit-log, metadata, event-driven]
---

### 1. Kiến trúc Core Audit Trail & Actor Tracking
- **`AuditEntryPayload`**: Bổ sung `actorId?: string` và `actorName?: string` ở cấp root-level, tránh việc phải parse deep JSON payload khi truy vấn danh tính người thực hiện.
- **Event Coverage**: Đảm bảo 100% các sự kiện CRM truyền tải thông tin Actor:
  - `LeadCreatedEvent`, `OrganizationCreatedEvent` (kèm flag `isNewCustomer`).
  - `ContractCreatedEvent` (chứa metadata cấu trúc: `fee`, `taxCode`, `serviceType`).
  - `QuoteCreatedEvent`, `QuoteStatusChangedEvent`, `LeadStatusChangedEvent`, `LeadAssignedEvent`.
- **`AuditDomainEventHandler`**: Bộ xử lý trung tâm tự động lắng nghe và ghi nhận các sự kiện trên vào hệ thống Log tập trung.

### 2. Cơ chế Gom nhóm & Định dạng Timeline
- **Truy vấn Tổng hợp (`ActivityFeedService`)**: Khi xem timeline của một `Lead`, hệ thống tự động gộp (aggregate) cả các sự kiện khởi tạo của thực thể cha `Organization` liên quan.
- **Định dạng hiển thị (`ActivityFormatter`)**: Chuẩn hóa map mã sự kiện sang ngôn ngữ Tiếng Việt chuyên nghiệp kèm icon tương ứng trên UI:
  - `LEAD.STATUS_CHANGED`: Thay đổi trạng thái của Lead.
  - `CONTRACT.CREATED`: Khởi tạo hợp đồng thành công.

### 3. Luồng Dữ liệu (Data Flow)
- **Controller/Service**: `LeadController` và `LeadIntakeService` bắt buộc trích xuất ngữ cảnh định danh từ Session (`user.id` -> `actor`) để truyền vào tham số khởi tạo các Workflow Actions và Domain Events.