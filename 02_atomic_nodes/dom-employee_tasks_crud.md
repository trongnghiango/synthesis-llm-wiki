```yaml
---
id: dom-employee_tasks_crud
title: Quản lý Công việc Nhân viên (Employee Tasks)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
summary: "Thiết kế DB, API nested resource và phân quyền cho tính năng Employee Tasks."
tags: [hrm, employee-task, crud, api-design, multi-tenancy]
---

## 1. Mô hình Dữ liệu (EmployeeTask)
- **Cấu trúc bảng**:
  - `id`: UUID (PK)
  - `organizationId`: UUID (FK, `[[arch-als-tenant-isolation]]`)
  - `employeeId`: UUID (FK, Target Employee)
  - `creatorId`: UUID (FK, Creator)
  - `title`: Varchar(255)
  - `description`: Text (Markdown support)
  - `status`: Enum (BACKLOG, TODO, IN_PROGRESS, DONE, CANCELED)
  - `priority`: Enum (NONE, LOW, MEDIUM, HIGH, URGENT)
  - `dueDate`: Timestamp
  - `completedAt`: Timestamp (Null khi chưa hoàn thành)
- **Chỉ mục (Index)**: B-Tree trên `(organizationId, employeeId, status)` để tối ưu hóa truy vấn O(log N).

## 2. API Contracts (Nested Resources)
- `GET /api/hrm/employees/:employeeId/tasks` - Lấy danh sách task (Hỗ trợ lọc & sắp xếp theo `dueDate`, `priority`).
- `POST /api/hrm/employees/:employeeId/tasks` - Giao việc mới cho nhân viên.
- `PATCH /api/hrm/employees/:employeeId/tasks/:taskId` - Cập nhật trạng thái/nội dung task.
- `DELETE /api/hrm/employees/:employeeId/tasks/:taskId` - Xóa task.

## 3. Bảo mật & Phân quyền
- **Cô lập dữ liệu**: Kiểm tra trùng khớp `organizationId` thông qua cơ chế của `[[arch-als-tenant-isolation]]`.
- **Permissions**:
  - `task:read`: Đọc danh sách/chi tiết task.
  - `task:create`: Giao việc mới.
  - `task:update`: Chỉ Creator hoặc Assignee được phép chỉnh sửa.
  - `task:delete`: Chỉ Creator hoặc Admin được phép xóa.

## 4. Kỹ thuật & Quy tắc Nghiệp vụ
- Logic cập nhật trạng thái `DONE` phải tự động đồng bộ thời gian `completedAt` ngay trong Domain Entity.
- Sử dụng DTO (`class-transformer`) để chuẩn hóa định dạng Date đầu vào tại tầng Controller.
```