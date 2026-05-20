# Implementation Plan: Quản lý Vị trí định biên (Positions)

Trang này cung cấp giao diện quản lý tập trung cho toàn bộ các vị trí định biên trong hệ thống, giúp người quản trị dễ dàng theo dõi tình trạng lấp đầy nhân sự trên quy mô toàn công ty.

## 1. Thành phần giao diện (UI Components)
- **PositionTable**: Bảng hiển thị danh sách các vị trí với các cột: Mã vị trí, Tên vị trí, Đơn vị trực thuộc, Chức danh, Bậc lương, và Tỷ lệ lấp đầy.
- **Filters**: Bộ lọc nhanh theo Đơn vị và Chức danh.

## 2. Điều hướng & Menu (Navigation)
- **Route**: `/admin/hrm/positions`
- **Vị trí Menu**: Nằm giữa `Employees` và `Organization` trong mục HRM.

## 3. Tái sử dụng Code (Clean Code)
- Tái sử dụng `PositionModal.tsx` để thực hiện các thao tác Thêm/Sửa.
- Tận dụng `hrm.api.ts` đã có các endpoint `getPositions`, `createPosition`, v.v.

## 4. Các bước thực hiện
1. Tạo trang `positions.tsx`.
2. Đăng ký Route trong `hrm-routes.tsx` và `index.tsx`.
3. Cập nhật `admin-menu.ts`.
