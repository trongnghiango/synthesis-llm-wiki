---
id: arch-tanstack-router-migration
title: Di chuyển TanStack Router & Tối ưu hóa UI/UX OrgChart
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-core-routing]]"
summary: "Chuyển đổi hệ thống routing từ wouter sang TanStack Router bảo đảm type-safe và tối ưu hóa UI/UX sơ đồ tổ chức (OrgChart)."
tags: [routing, tanstack-router, frontend, org-chart, ui-ux]
---

## 1. Kiến trúc Routing mới (TanStack Router)
- **Centralized Route Tree**: Định nghĩa tập trung tại `client/src/app/router/routes/` giúp tối ưu code-splitting.
- **Persistent Layout**: Sử dụng `<Outlet />` trong `AdminLayout` để bảo toàn trạng thái sidebar/header.
- **Type-Safe Navigation**: Thay thế toàn bộ `setLocation` và `Link` legacy bằng API an toàn kiểu dữ liệu của TanStack.
- **Route Guarding**: Kiểm thực session thông qua `beforeLoad` sử dụng `ensureQueryData` trước khi render route `/admin`.

## 2. API & Cấu hình Routes chính
- `client/src/app/router/index.tsx`: Khởi tạo và cấu hình chính cho Router.
- `client/src/layouts/admin-layout.tsx`: Layout quản trị hỗ trợ co giãn động.
- **Params Mapping**: Khắc phục triệt để lỗi `NaN` tham số bằng cách ép kiểu tường minh ID truyền qua Route Params đối với các chi tiết thực thể CRM (leads, clients, contracts).

## 3. Thiết kế UI/UX Org Chart (HRM)
- **Full-Width View**: Loại bỏ giới hạn `max-w-7xl` tại `AdminLayout` khi xem sơ đồ cây.
- **Height Calibration**: Khóa cứng chiều cao vùng chứa chính ở mức `100vh - 56px` để tràn màn hình.
- **Side Panel**: Thiết lập `absolute right-0` cho panel thông tin chi tiết để tránh làm dịch chuyển/vỡ layout của biểu đồ chính.
- **Interaction**: Kích hoạt kéo thả bằng chuột trái (left-click dragging) trực tiếp trên `OrgChart` và highlight node đang chọn.