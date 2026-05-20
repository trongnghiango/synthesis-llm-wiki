# Walkthrough: Hoàn tất Module Danh mục HRM

Chúng ta đã thành công trong việc xây dựng hệ thống quản trị danh mục nền tảng cho HRM, giải quyết vấn đề "dữ liệu trống" khi tạo Vị trí định biên.

## Các thay đổi chính

### 1. Quản lý Chức danh & Bậc lương
- **Trang mới**: `Danh mục HRM` (nằm trong menu HRM).
- **Tính năng**: Cho phép khai báo đầy đủ danh mục nghề nghiệp và khung bậc lương của công ty.
- **Giao diện**: Thiết kế dạng Tabs hiện đại, hỗ trợ tìm kiếm nhanh và Modal nhập liệu tiện lợi.

### 2. Đồng bộ dữ liệu (Lookups)
- Hook `useLookups` đã được nâng cấp để tự động nạp dữ liệu từ các danh mục mới này.
- Khi bạn thêm một Chức danh mới ở trang Danh mục, nó sẽ lập tức xuất hiện trong danh sách chọn khi bạn tạo Vị trí (Position) ở trang Sơ đồ tổ chức.

### 3. Tuân thủ Clean Architecture
- Toàn bộ logic API được tập trung tại `hrm.api.ts`.
- Component được tổ chức theo module, dễ dàng bảo trì và mở rộng.

## Hướng dẫn sử dụng
1. Vào menu **HRM > Danh mục HRM**.
2. Thêm một vài **Chức danh** (VD: Kế toán trưởng, Nhân viên tư vấn).
3. Thêm một vài **Bậc lương** (VD: Bậc 1, Bậc 2).
4. Quay lại trang **Sơ đồ tổ chức**, chọn một phòng ban -> Thêm vị trí. Bạn sẽ thấy các danh mục vừa tạo đã sẵn sàng để chọn.
