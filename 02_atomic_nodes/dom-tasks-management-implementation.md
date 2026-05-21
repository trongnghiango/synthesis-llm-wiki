---
id: dom-tasks-management-implementation
title: Triển khai Module Quản lý Công việc (Tasks)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[arch-als-tenant-isolation]]"
  - "[[hb-delta-logging]]"
summary: "Thiết kế kỹ thuật và lộ trình triển khai module Quản lý Công việc (Tasks) cao cấp cho HRM."
tags: [hrm, tasks, frontend, premium-ui, kanban]
---

## 1. Kiến trúc & Routing
- **Đường dẫn**: `client/src/pages/admin/hrm/tasks.tsx`
- **Layout**: Bento Grid (Dashboard) & Data Grid (Danh sách).
- **Trạng thái UI**: Quản lý tập trung qua React Context/Zustand phục vụ đồng bộ filter và Drawer.

## 2. Thành phần UI & UX Premium
- `TaskCard`: Thẻ Kanban sử dụng Framer Motion `layoutId` để chuyển cảnh mượt mà.
- `TaskStatusBadge`: Badge động với hiệu ứng gradient dựa trên trạng thái và độ ưu tiên.
- `TaskFilters`: Bộ lọc đa điều kiện (assignee, priority, due date) đồng bộ URL query params.
- `TaskDetailDrawer`: Drawer trượt quản lý chi tiết task, hoạt động tương tác và log.
- **Phong cách**: Glassmorphism (backdrop-blur cho header/sidebar) kết hợp bảng màu Pastel/Vibrant.

## 3. Thiết kế Schema & API (Đề xuất)
Áp dụng cơ chế cô lập `[[arch-als-tenant-isolation]]` và mẫu repo `[[hb-drizzle-base-repo]]`.

### Cấu trúc Schema `tasks`:
- `id` (UUID, PK)
- `tenant_id` (UUID, FK - Tenant Isolation)
- `title` (varchar, required)
- `description` (text)
- `status` (enum: 'todo', 'in_progress', 'review', 'done')
- `priority` (enum: 'low', 'medium', 'high', 'urgent')
- `assignee_id` (UUID, FK -> users)
- `due_date` (timestamp)
- `created_at` / `updated_at` (timestamp)

## 4. Lộ trình Triển khai
1. **Route & Schema**: Định nghĩa route `/admin/hrm/tasks`, migrate DB schema `tasks`.
2. **Layout & State**: Thiết lập khung Bento Grid và các global state quản lý filter.
3. **List View**: Tích hợp Data Grid hiển thị danh sách và component `TaskStatusBadge`.
4. **Board View**: Kéo thả Kanban tích hợp Framer Motion.
5. **Quick Action & Drawer**: Hoàn thiện Drawer xem chi tiết/cập nhật nhanh task.
6. **Logging**: Ghi nhận lịch sử thay đổi trạng thái qua `[[hb-delta-logging]]`.