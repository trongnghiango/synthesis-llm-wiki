```yaml
---
id: hb-stax-implementation-roadmap
title: Lộ trình Chuẩn hóa và Triển khai STAX (Solo-Dev Master Schedule)
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[hb-delta-logging]]"
  - "[[dom-accounting-finote]]"
summary: "Lộ trình 22 tuần chia thành 11 Sprints tối ưu hóa cho Solo-Developer triển khai hệ thống STAX (HRM, CRM, Finote, Task & Payroll) sử dụng Drizzle ORM và PostgreSQL."
tags: [roadmap, project-management, sprint, solo-dev, tech-stack]
---

### 1. Quy tắc Vận hành & Phát triển (Workflow Rules)
* **Quy trình:** Agile, Sprint 2 tuần. Hoàn thiện Backend (API, DB, Logic) trước, ghép Frontend sau.
* **Scope Control:** Áp dụng *Scope Freeze* đầu mỗi Sprint; tuyệt đối không chèn thêm yêu cầu giữa chừng.
* **Tối ưu UI:** Sử dụng Template Ant Design (React) / Mantine nhằm đẩy nhanh tiến độ phía client.

### 2. Thành phần Kỹ thuật Cốt lõi (Core Technical Architecture)
* **Database & ORM:** PostgreSQL + Drizzle ORM. Triển khai migration tự động.
* **Sơ đồ tổ chức (HRM):** Áp dụng cấu trúc *Materialized Path* cho bảng Phòng ban.
* **Storage Adapter:** Triển khai `GoogleDriveAdapter` (Service Account) liên kết qua bảng `attachments`.
* **Tự động hóa Finote:** Thiết lập Cronjob tự động chuyển trạng thái sang `APPROVED` sau 3 ngày không duyệt.
* **Audit Log & Security:** Override hàm update trong `DrizzleBaseRepository` (tham chiếu `[[hb-drizzle-base-repo]]`), đẩy log qua EventBus xuống Postgres JSONB (tham chiếu `[[hb-delta-logging]]`).
* **Tính toán Lương:** Thiết kế Dynamic Payroll Parser thực thi các công thức tính toán động từ cấu hình DB.

### 3. Lịch trình Triển khai Chi tiết (11 Sprints)
#### Giai đoạn 1: Core, HRM Cơ bản, CRM & [[dom-accounting-finote]] (Sprint 1 - 7)
* **Sprint 1 (Tuần 1-2):** Dọn dẹp Dental module. Setup Docker, PostgreSQL, Drizzle. API Auth, RBAC Matrix.
* **Sprint 2 (Tuần 3-4):** API CRUD Phòng ban (Materialized Path), Chức danh, Nhân sự. OrgChart UI.
* **Sprint 3 (Tuần 5-6):** Tích hợp `GoogleDriveAdapter`. Database Schema `attachments`. API Kanban CRM Leads.
* **Sprint 4 (Tuần 7-8):** Database Schema `contracts` (liên kết Org). Cronjob cảnh báo hết hạn. API Export PDF Quote.
* **Sprint 5 (Tuần 9-10):** API CRUD Finote & Cronjob Auto-Approve (3 ngày). Màn hình Approval Workflow.
* **Sprint 6 (Tuần 11-12):** Tối ưu hóa UI/UX, viết Unit Test & Manual Test toàn diện.
* **Sprint 7 (Tuần 13-14):** Triển khai VPS/Cloud, chạy thử nghiệm UAT Giai đoạn 1 & Golive.

#### Giai đoạn 2: Task, Payroll & Audit Log (Sprint 8 - 11)
* **Sprint 8 (Tuần 15-16):** Database Level Interception ghi Audit Log JSONB. Webhook nhận log máy chấm công.
* **Sprint 9 (Tuần 17-18):** API/DB CRUD Tasks, Assignees, Deadline. System Notification Event Bus (bắn chuông).
* **Sprint 10 (Tuần 19-20):** Engine Dynamic Payroll Parser. Thiết lập bảng lương tháng & Payslip.
* **Sprint 11 (Tuần 21-22):** UAT Giai đoạn 2, đóng gói Source code, API Docs & bàn giao.
```