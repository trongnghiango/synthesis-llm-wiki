---
id: dom-hrm_positions_management
title: Quản lý Vị trí Định biên HRM
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Đặc tả kỹ thuật và cấu trúc triển khai giao diện quản lý vị trí định biên (Positions) thuộc phân hệ HRM."
tags: [hrm, positions, route-setup, ui-component]
---

## 1. Thông tin Định tuyến & Menu
- **Route**: `/admin/hrm/positions`
- **File cấu hình cần cập nhật**:
  - Khai báo Route tại `hrm-routes.tsx` và import vào `index.tsx`.
  - Cấu hình hiển thị tại `admin-menu.ts` (đặt giữa menu `Employees` và `Organization`).

## 2. Thiết kế Giao diện (UI Components)
- **Trang chính**: `positions.tsx`
- **Thành phần giao diện**:
  - `PositionTable`: Bảng hiển thị (Mã vị trí, Tên vị trí, Đơn vị trực thuộc, Chức danh, Bậc lương, Tỷ lệ lấp đầy nhân sự).
  - `Filters`: Bộ lọc nhanh theo Đơn vị (Department) và Chức danh (Job Title).
  - Tái sử dụng `PositionModal.tsx` cho luồng Thêm mới / Cập nhật.

## 3. Tích hợp API & Dữ liệu
- **Tập tin API**: `hrm.api.ts`
- **Endpoints cần sử dụng**:
  - `getPositions(filters)`: Lấy danh sách và tỷ lệ lấp đầy định biên.
  - `createPosition(data)` / `updatePosition(id, data)`: Xử lý qua Modal.
- **Tương tác dữ liệu**: Kết nối qua thực thể schema cấu hình theo chuẩn của `[[hb-drizzle-base-repo]]`.