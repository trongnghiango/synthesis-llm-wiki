---
id: hb-standardization_and_cleanup
title: Quy trình Chuẩn hóa và Lộ trình Phát triển STAX
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
  - "[[dom-accounting-finote]]"
summary: "Lộ trình 11 Sprint phát triển hệ thống STAX (HRM, CRM, Finote, Audit Log, Tasks) tối ưu cho Solo-Developer."
tags: [roadmap, hrm, crm, audit-log, finote, drizzle]
---

### 1. Kiến trúc Mô-đun & Lộ trình Kỹ thuật (11 Sprints / 22 Tuần)
*   **Sprint 1: Core Platform:** Dọn dẹp Dental module, đóng băng Chatbot. Khởi tạo Docker, Postgres, Drizzle migration. Phân quyền RBAC.
*   **Sprint 2: Core HRM Org:** Entity `departments` (Materialized Path pattern), `jobs`, `employees`.
*   **Sprint 3: Storage & CRM:** Tích hợp `GoogleDriveAdapter` (Service Account) -> Schema `attachments`. CRM Lead Kanban state-machine.
*   **Sprint 4: Contracts & PDF:** Schema `contracts` (cronjob cảnh báo hết hạn) & `quotes` (PDF generation).
*   **Sprint 5: Workflow Finote:** Cơ chế phê duyệt tự động của `[[dom-accounting-finote]]` qua Cronjob (Auto-approve sau 3 ngày).
*   **Sprint 6-7: Internal QA, UAT 1 & Golive Phase 1.**
*   **Sprint 8: Enterprise Logging & Attendance:**
    *   Tích hợp `[[hb-delta-logging]]` thông qua Database Level Interception (Override update method trong `[[hb-drizzle-base-repo]]`).
    *   EventBus đẩy log xuống Postgres JSONB. Webhook nhận máy chấm công.
*   **Sprint 9: Task Management:** CRUD Tasks, Assignees, Deadline engine, Notification service.
*   **Sprint 10: Payroll Engine:** Dynamic Formula Parser (tính lương động dựa trên công thức cấu hình).
*   **Sprint 11: UAT 2 & Final Handover.**

### 2. Nguyên tắc Thiết kế Hệ thống cho Solo-Developer
*   **Scope Freeze & Timeboxing:** Cố định phạm vi từng Sprint. Phân chia: Sáng (Core logic, DB, API), Chiều (Integration, UI components như Ant Design/Mantine).
*   **Data Isolation:** Áp dụng `[[arch-als-tenant-isolation]]` xuyên suốt các bảng HRM/CRM.