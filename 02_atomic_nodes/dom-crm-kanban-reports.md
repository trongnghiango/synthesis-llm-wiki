---
id: dom-crm-kanban-reports
title: Thiết kế Kanban & Chuyển đổi Trạng thái CRM Lead
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
summary: "Quy trình chuyển đổi trạng thái Lead qua PATCH API, chặn chuyển WON trực tiếp và tích hợp Domain Event kích hoạt ghi nhật ký."
tags: [crm, kanban, lead-status, domain-event, architecture]
---

### 1. API & Ánh xạ Dữ liệu (Mapping)
*   **API Endpoint:** `PATCH /crm/leads/:id`
    *   Payload DTO sử dụng `updateLeadSchema` (`shared/contracts/crm.ts`) chứa trường tùy chọn `status: z.string().optional()`.
*   **Data Mapping:** 
    *   Database schema dùng trường `status` trong khi Domain Entity dùng `stage`.
    *   Đồng bộ thông qua `LeadMapper` tại tầng Service để đảm bảo tính nhất quán của Domain Model mà không phá vỡ schema hiện tại.

### 2. Ràng buộc Nghiệp vụ (Business Rules)
*   **Trạng thái hợp lệ:** Cho phép cập nhật trực tiếp qua API PATCH giữa các trạng thái: `NEW`, `CONSULTING`, `NEGOTIATING`, `LOST`.
*   **Chặn WON trực tiếp:**
    *   Nếu payload truyền `status: 'WON'`, Service chặn và ném `BusinessRuleValidationException`.
    *   **Yêu cầu luồng:** Bắt buộc Client mở dialog chuyên dụng và gọi API `/crm/leads/:id/won` để xử lý đồng thời các nghiệp vụ phụ thuộc (tạo hợp đồng, sinh phiếu thu kế toán liên kết với `[[dom-accounting-finote]]`).

### 3. Sự kiện Hệ thống & Audit Log
*   **Domain Event:** Cập nhật trạng thái thành công kích hoạt phát hành `LeadStatusChangedEvent`.
*   **Event Handler:** Hệ thống Audit Log đăng ký lắng nghe event này để tự động ghi vết lịch sử thay đổi trạng thái (sử dụng cơ chế ghi nhận tương tự `[[hb-delta-logging]]`).