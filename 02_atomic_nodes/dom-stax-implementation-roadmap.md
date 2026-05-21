---
id: dom-stax-implementation-roadmap
title: Lộ trình Triển khai STAX & Thiết kế Kiến trúc Phân rã
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
  - "[[dom-accounting-finote]]"
summary: "Lộ trình triển khai STAX 22 tuần (11 Sprints) kèm đặc tả kiến trúc kỹ thuật lõi."
tags: [roadmap, agile, architecture-design, db-schema]
---

### 1. Phân rã Kỹ thuật Giai đoạn 1 (Sprint 1 - 7): Core, HRM, CRM & Finote
*   **Sprint 1 (Core & Auth):** Chuyển dịch PostgreSQL + Drizzle ORM. Thiết lập RBAC dynamic matrix.
*   **Sprint 2 (HRM OrgChart):** Sử dụng cấu trúc **Materialized Path** (`path` varchar) cho bảng `departments` để tối ưu truy vấn sơ đồ cây phòng ban.
*   **Sprint 3 (Storage & CRM):**
    *   Xây dựng `GoogleDriveAdapter` (Service Account authorization). Bảng `attachments` mapping trực tiếp với Drive File ID.
    *   Thiết kế bảng `crm_leads` hỗ trợ trạng thái Kanban (Enum: LEAD, CONTACT, DEAL, CLOSED).
*   **Sprint 4 (Contract & PDF):** Lập lịch Cronjob kiểm tra `expire_date` trên bảng `contracts`. Tích hợp PDF generator engine cho `quotes`.
*   **Sprint 5 (Finote Workflow):** Tích hợp quy trình `[[dom-accounting-finote]]`. Cronjob quét tự động chuyển trạng thái từ `PENDING` sang `APPROVED` sau 3 ngày không thao tác.
*   **Sprint 6 & 7:** UAT Giai đoạn 1 & Golive Core.

### 2. Phân rã Kỹ thuật Giai đoạn 2 (Sprint 8 - 11): Audit Log, Task & Payroll
*   **Sprint 8 (Audit Log & Timesheet Checkin):**
    *   Can thiệp tầng Database thông qua việc override các phương thức cập nhật dữ liệu của `[[hb-drizzle-base-repo]]`.
    *   Sử dụng EventBus để publish và lưu trữ thay đổi dưới dạng Delta Log `[[hb-delta-logging]]` xuống bảng `audit_logs` (cột `payload` kiểu JSONB).
    *   Xây dựng Webhook tiếp nhận dữ liệu định dạng chuẩn từ máy chấm công.
*   **Sprint 9 (Task Management):** Schema bảng `tasks` hỗ trợ quan hệ Many-to-Many (`task_assignees`). Thiết kế Pub/Sub Event thông báo qua WebSocket/SSE.
*   **Sprint 10 (Payroll Engine):**
    *   Phát triển AST Parser tính toán lương động từ biểu thức công thức (String formula).
    *   Thiết kế bảng `payrolls` lưu trữ snapshot kết quả tính toán cuối kỳ (Immutable State).
*   **Sprint 11:** Nghiệm thu tổng thể và đóng gói phân phối API Docs.