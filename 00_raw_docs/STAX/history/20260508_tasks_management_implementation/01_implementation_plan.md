# Implementation Plan: Module Quản lý Công việc (Tasks)

Mục tiêu là tạo ra một trang quản lý công việc hiện đại, đơn giản nhưng mang lại cảm giác cao cấp (Premium feel) tương tự như Linear.

## 1. Kiến trúc trang (Page Structure)
- **File**: `client/src/pages/admin/hrm/tasks.tsx`
- **Layout**: Sử dụng "Bento Grid" cho Dashboard và "Data Grid" cao cấp cho danh sách công việc.

## 2. Các thành phần UI mới (New Components)
- **TaskCard**: Thẻ hiển thị task trong Board view với hiệu ứng Hover mượt mà.
- **TaskStatusBadge**: Badge trạng thái có gradient và icon động.
- **TaskFilters**: Bộ lọc thông minh theo người thực hiện, độ ưu tiên và thời hạn.
- **TaskDetailDrawer**: Cửa sổ trượt hiển thị chi tiết và lịch sử công việc.

## 3. Thẩm mỹ & Hiệu ứng (Aesthetics)
- **Glassmorphism**: Header và Sidebar sẽ có nền mờ (blur).
- **Smooth Transitions**: Chuyển đổi giữa các tab (List/Board) bằng Framer Motion LayoutId.
- **Colors**: Sử dụng bảng màu dịu (Pastel) cho các tag và màu Vibrant cho các trạng thái quan trọng.

## 4. Lộ trình thực hiện
1. Đăng ký Route `/admin/hrm/tasks`.
2. Xây dựng giao diện Layout chính của trang Task.
3. Triển khai View Danh sách (List View).
4. Triển khai View Bảng (Board View).
5. Tích hợp chức năng tạo Task nhanh.
