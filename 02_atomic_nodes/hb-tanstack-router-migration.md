---
id: hb-tanstack-router-migration
title: Di trú TanStack Router & Tối ưu hóa UI/UX OrgChart
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-auth-flow]]"
summary: "Hướng dẫn chuyển đổi hệ thống routing sang TanStack Router, áp dụng Route Guard và tối ưu giao diện full-screen cho OrgChart."
tags: [tanstack-router, routing, layout, orgchart, ux-optimization]
---

## 1. Kiến trúc Routing mới (TanStack Router)
- **Centralized Route Tree**: Định nghĩa tập trung tại `/client/src/app/router/routes/` thay thế cho `wouter`.
- **Persistent Layout**: Sử dụng `<Outlet />` trong `/client/src/layouts/admin-layout.tsx` để bảo toàn trạng thái Sidebar/Header khi chuyển trang.
- **Route Guard & Auto-Redirect**:
  - Khai báo `beforeLoad` tại root `/admin` để kiểm tra session qua `ensureQueryData`.
  - Tự động chuyển hướng (redirect) hợp lệ cho `/`, `/login`, và các admin sub-routes.
- **Type-safe Navigation**: Thay thế toàn bộ `setLocation` và `Link` cũ. Tham số ID được truyền tường minh qua route params để tránh lỗi `NaN`.

## 2. Tối ưu hóa UI/UX OrgChart (HRM)
- **Full-Screen View**: Loại bỏ giới hạn `max-w-7xl` tại `AdminLayout` khi xem sơ đồ tổ chức để tối ưu không gian hiển thị.
- **Tính toán chiều cao**: Khóa cứng chiều cao vùng chứa chart bằng `100vh - 56px` sát đáy màn hình.
- **Side Panel**: Định vị `absolute right-0` cho panel thông tin chi tiết, tránh làm biến dạng hoặc đẩy lệch cấu trúc của OrgChart khi đóng/mở.
- **Tương tác**: Kích hoạt kéo thả bằng chuột trái tại `OrgChart.tsx` và highlight trực quan node đang chọn.

## 3. Các file ảnh hưởng chính
- **Core Router**: `/client/src/app/router/index.tsx`, `/client/src/layouts/admin-layout.tsx`
- **CRM Pages**: `/client/src/pages/leads.tsx`, `/client/src/pages/clients.tsx`, `/client/src/pages/contracts.tsx`
- **HRM Pages**: `/client/src/pages/org-structure.tsx`, `/client/src/components/OrgChart.tsx`