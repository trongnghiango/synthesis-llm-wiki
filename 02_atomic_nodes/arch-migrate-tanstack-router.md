---
id: arch-migrate-tanstack-router
title: Di cư TanStack Router & Tối ưu Layout CRM/HRM
layer: 3-atomic
parent: "[[01_core_architecture]]"
summary: "Chuyển đổi từ wouter sang TanStack Router, nâng cấp Type-Safe Navigation, Router Guards và tối ưu hóa UI Org Chart"
tags: [routing, tanstack-router, react, layout, org-chart]
---

## 1. Kiến trúc Routing mới (TanStack Router)
- **Cấu trúc Route tập trung:** Toàn bộ route chuyển về `client/src/app/router/routes/` để tối ưu code-splitting.
- **Persistent Layout:** Sử dụng `<Outlet />` trong `AdminLayout` để duy trì state Sidebar/Header khi chuyển trang.
- **Type-Safe Navigation:** Thay thế hoàn toàn `setLocation` và thẻ `Link` cũ bằng cơ chế Type-Safe nghiêm ngặt.
- **Router Guards:** Áp dụng `beforeLoad` tại `/admin` để xác thực Session qua `ensureQueryData` trước khi render.

## 2. Tối ưu hóa Layout & Tương tác CRM/HRM
- **Full-Screen Org Chart:** Loại bỏ `max-w-7xl` tại `AdminLayout` cho module cơ cấu tổ chức; chiều cao đạt tối đa `100vh - 56px`.
- **Non-blocking Side Panel:** Chuyển panel thông tin sang `absolute right-0` để không ảnh hưởng layout biểu đồ.
- **Cải tiến Tương tác:** Kích hoạt left-click drag và làm nổi bật selected state trong `OrgChart.tsx`.
- **Fix Bugs:** Khắc phục lỗi `NaN` ID parameters bằng cách truyền kiểu dữ liệu rõ ràng qua Route Params trong các module CRM (`leads`, `clients`, `contracts`).

## 3. Các tệp tin cốt lõi ảnh hưởng
- `client/src/app/router/index.tsx` (Cấu hình Router chính)
- `client/src/layouts/admin-layout.tsx` (Layout động)
- `client/src/pages/admin/hrm/org-structure.tsx` & `OrgChart.tsx` (UI/UX Org Chart)
- `client/src/pages/admin/crm/` (`leads.tsx`, `clients.tsx`, `contracts.tsx` - Type-safe migration)