# Task List — Client 360° View

> Trạng thái: In Progress
> Context: Phase 4 - Xây dựng hồ sơ khách hàng 360 độ chuyên sâu.

### 1. Nền tảng & Cấu trúc (Foundation)
- [x] Khởi tạo trang `client/src/pages/admin/crm/client-detail.tsx`.
- [x] Đăng ký Route `/admin/crm/clients/:id` trong `App.tsx`.
- [x] Cập nhật `crmApi` để bổ sung `getOrganizationById` và `getOrganizationActivities`.

### 2. Thành phần Giao diện (Components)
- [x] Xây dựng Sidebar thông tin định danh (Identity Card).
- [x] Xây dựng Top Metrics Bar (Compliance, Revenue, Tasks).
- [x] Xây dựng các Tab chính:
    - [x] Tab **Overview** (Charts & Key Contacts).
    - [x] Tab **Compliance** (Bảng theo dõi tuân thủ thuế).
    - [x] Tab **Contracts** (Sử dụng DataGrid).
    - [x] Tab **Documents** (Quản lý file).
- [x] Xây dựng **Interaction Timeline** (Dòng thời gian tương tác).

### 3. Tích hợp & Logic (Integration)
- [x] Kết nối API lấy dữ liệu chi tiết Organization.
- [x] Kết nối API lấy danh sách Contracts theo Organization.
- [x] Kết nối API Activity Log cho Organization.
- [x] Xử lý trạng thái Loading & Empty State cho từng tab.

### 4. Hoàn thiện & UX (Polishing)
- [x] Áp dụng hiệu ứng Glassmorphism & Framer Motion.
- [x] Kiểm tra Responsive trên Mobile (Stacking layout).
- [x] Viết Walkthrough hoàn thiện.
