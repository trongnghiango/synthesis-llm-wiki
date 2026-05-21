```yaml
---
id: arch-stax-implementation-roadmap
title: Lộ trình triển khai phân rã & chuẩn hóa hệ thống STAX
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[dom-accounting-finote]]"
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
summary: "Lộ trình 11 Sprint kiến trúc & phát triển độc lập STAX: Core, HRM (Org Tree), CRM (Leads/Drive), Finote (Auto-Approve), Audit Log và Dynamic Payroll."
tags: [roadmap, architecture, materialized-path, audit-log, auto-approve]
---

### 1. KIẾN TRÚC PHÂN KỲ & THIẾT KẾ KỸ THUẬT CỐT LÕI

*   **Sprint 1-2 (Core & Auth):** Dọn dẹp mã nguồn cũ; khởi tạo Postgres + Drizzle ORM; thiết kế RBAC Matrix API.
*   **Sprint 3-4 (HRM Org-Tree):** Lưu trữ cấu trúc phòng ban sử dụng mô hình **Materialized Path**. API CRUD Employees.
*   **Sprint 5-6 (Storage & CRM):**
    *   Thiết lập `GoogleDriveAdapter` tích hợp Google Service Account.
    *   Thiết kế Schema `attachments` lưu trữ siêu dữ liệu (metadata) liên kết thực thể.
    *   CRM Leads: API chuyển trạng thái Kanban (State Machine).
*   **Sprint 7-8 (Contracts & Quotes):** Cronjob quét thời hạn `Contracts`. Tích hợp PDF Engine sinh Báo giá tự động.
*   **Sprint 9-10 (Workflow Finote):**
    *   Liên kết nghiệp vụ dòng tiền qua `[[dom-accounting-finote]]`.
    *   Cronjob Auto-Approve: Tự động chuyển trạng thái `APPROVED` sau 72 giờ không có tương tác phê duyệt.
*   **Sprint 15-16 (Enterprise Logging & Check-in):**
    *   **Database Level Interception**: Ghi đè phương thức write trong `[[hb-drizzle-base-repo]]`.
    *   **EventBus**: Đẩy bất đồng bộ cấu trúc Delta Log xuống Postgres JSONB theo chuẩn `[[hb-delta-logging]]`.
    *   Webhook tiếp nhận và chuẩn hóa dữ liệu chấm công từ thiết bị ngoại vi.
*   **Sprint 17-18 (Task Management):** Thiết lập cơ chế bắn sự kiện (Event-driven Notification) qua Web-push/SSE khi có cập nhật hoặc cận deadline.
*   **Sprint 19-20 (Payroll Engine):** Xây dựng Dynamic Formula Parser để thông dịch và tính toán lương dựa trên công thức động lưu trong cơ sở dữ liệu.

### 2. NGUYÊN TẮC VẬN HÀNH KỸ THUẬT (SOLO-DEV)
*   **Scope Freeze**: Đóng băng API Contract và Schema Database đầu mỗi Sprint; xử lý yêu cầu phát sinh dạng hàng đợi (Queue) cho Sprint kế tiếp.
*   **Tách biệt Tầng (Layer Separation)**: Phát triển và kiểm thử độc lập API (Integration Test) trước khi tích hợp vào giao diện (Ant Design / Mantine).
```