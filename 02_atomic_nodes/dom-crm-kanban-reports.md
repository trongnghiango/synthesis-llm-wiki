---
id: dom-crm-kanban-reports
title: Quy trình Chuyển Giai đoạn Lead CRM & Kanban
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
summary: "Quy tắc chuyển trạng thái Lead CRM qua PATCH API, chặn WON trực tiếp và phát hành sự kiện."
tags: [crm, lead, kanban, domain-event, validation]
---

### 1. Luồng Nghiệp vụ & Thiết kế API
* **API Endpoint:** `PATCH /crm/leads/:id`
* **DTO Contract (`shared/contracts/crm.ts`):** `updateLeadSchema` bổ sung `status: z.string().optional()`.
* **Mapping Nội bộ:** `LeadMapper` ánh xạ trường `status` (Database/DTO) với thuộc tính `stage` (Domain Entity) để đảm bảo tính nhất quán dữ liệu.

### 2. Ràng buộc Nghiệp vụ Chốt WON
* **Quy tắc chặn:** Cấm chuyển trực tiếp trạng thái sang `WON` qua API `PATCH`.
* **Xử lý:** Nếu payload chứa `status: 'WON'` -> Service ném lỗi `BusinessRuleValidationException`.
* **Luồng hợp lệ cho WON:** Phải gọi qua API chuyên dụng `/crm/leads/:id/won` để thực thi đồng thời nghiệp vụ tạo hợp đồng và khởi tạo phiếu thu.
* **Các trạng thái cho phép qua PATCH:** `NEW`, `CONSULTING`, `NEGOTIATING`, `LOST`.

### 3. Kiến trúc Event-Driven & Logging
* Sau khi lưu thay đổi trạng thái Lead thành công vào DB, hệ thống phát hành sự kiện `LeadStatusChangedEvent`.
* **Subscribers:** Hệ thống Audit Log (chi tiết tại `[[hb-delta-logging]]`) đăng ký nhận sự kiện này để tự động ghi vết lịch sử thay đổi trạng thái (Lead History Log).

### 4. Tích hợp Frontend
* Cập nhật Kanban qua API: `crmApi.updateLead(leadId, { status: newStage })` (với `newStage` khác `WON`).
* Trạng thái `WON` yêu cầu mở Dialog/Form riêng để gọi API `/crm/leads/:id/won`.