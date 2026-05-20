# Research: Triển khai Danh mục HRM (Master Data)

## 1. Hiện trạng hệ thống
- **Org Structure**: Đã có quản lý Đơn vị (Org Unit) và Vị trí (Position).
- **Position**: Đang có các trường `jobTitleId` và `gradeId` nhưng chưa có dữ liệu tra cứu (Lookups).
- **UI**: Thiếu giao diện để người dùng định nghĩa các danh mục cơ sở này.

## 2. Yêu cầu kiến trúc (Clean Architecture Compliance)
- **Modularity**: Phải nằm trong module `hrm`.
- **Data Flow**: Tuân thủ Unidirectional Data Flow của TanStack Query.
- **Type Safety**: Phải có DTO và Interface rõ ràng từ `@shared`.

## 3. Các thực thể cần bổ sung
### A. Chức danh (Job Title)
- Cung cấp tên gọi nghề nghiệp chung (VD: Software Engineer, Accountant).
- Được dùng để phân loại Vị trí (Position) trên toàn hệ thống.

### B. Bậc lương (Salary Grade)
- Định nghĩa khung lương/cấp bậc gắn với Chức danh.
- Hỗ trợ việc tự động hóa tính toán lương trong tương lai.
