# Task Checklist: HRM Master Data Implementation

- [x] **Infrastructure**
    - [x] Định nghĩa Interface tại `@shared` (nếu chưa có).
    - [x] Cập nhật `hrm.api.ts` với các phương thức CRUD mới.
- [x] **Presentation Components**
    - [x] Phát triển `JobTitleTable.tsx` (Bảng và Form thêm/sửa).
    - [x] Phát triển `SalaryGradeTable.tsx` (Bảng và Form thêm/sửa).
- [x] **Pages & Routing**
    - [x] Tạo trang `master-data.tsx` tích hợp các Table trên.
    - [x] Đăng ký Route trong `hrm-routes.tsx`.
    - [x] Cập nhật Menu trong `admin-menu.ts`.
- [x] **Integration & UX**
    - [x] Cập nhật `useLookups.ts` để lấy dữ liệu mới.
    - [x] Kiểm tra tính liền mạch trong `PositionModal.tsx`.
