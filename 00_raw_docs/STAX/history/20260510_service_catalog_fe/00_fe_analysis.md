# Bước 1: Phân tích Nghiệp vụ & UX — Frontend Service Catalog

## A. Mục tiêu & Đối tượng
- **Mục tiêu:** 
  1. Quản lý danh mục dịch vụ tập trung (Admin).
  2. Tối ưu hóa việc nhập liệu trong các workflow bán hàng và kế toán (Sales/Accountant).
- **Tiêu chí UX (Zero-Learning):** Giao diện phải mang tính gợi ý cao, giảm thiểu việc gõ phím, ưu tiên lựa chọn và tự động điền (Auto-fill).

## B. Phân tích các trang/thành phần mới

### 1. Trang Quản lý Service Catalog (`/admin/crm/services`)
- **Layout:** Dạng Grid hoặc List với các thẻ (Cards) hiển thị thông tin trực quan.
- **Tính năng:**
  - Danh sách dịch vụ với badge phân loại (RETAINER/ONE_OFF).
  - Quick-edit giá và trạng thái ngay tại danh sách.
  - Bộ lọc thông minh theo loại hình dịch vụ.

### 2. Thành phần "Service Picker" (Tích hợp vào Form)
Đây là trái tim của trải nghiệm người dùng trong Quote/Contract/Finote.
- **UX Concept:** Thay vì một `Select` dropdown đơn điệu, chúng ta sẽ dùng một `ServiceSelector` kết hợp Search-as-you-type.
- **Smart Logic:** 
  - Khi chọn một dịch vụ, hệ thống tự động điền: Mô tả, Đơn giá gốc.
  - Cho phép ghi đè (Override) giá nếu nhân viên có quyền chiết khấu.
- **Vị trí tích hợp:**
  - **Quote Form:** Thêm dòng mới bằng cách chọn dịch vụ.
  - **Contract Draft:** Cho phép bổ sung dịch vụ phát sinh.
  - **Finote (Phiếu ĐNTT):** Liên kết chi phí với một dịch vụ cụ thể để theo dõi P&L (Lợi nhuận) sau này.

## C. Zero-Learning UX Strategy
- **Micro-copy:** Sử dụng ngôn ngữ gần gũi (VD: "Chọn dịch vụ STAX cung cấp" thay vì "Service ID").
- **Visual Feedback:** Hiển thị preview tổng tiền ngay khi thay đổi số lượng hoặc chọn dịch vụ khác.
- **Defaults:** Tự động chọn đơn vị tiền tệ và loại hình phổ biến nhất.

## D. Luồng dữ liệu (Data Flow)
- **Queries:** Sử dụng TanStack Query để cache danh mục dịch vụ, đảm bảo picker phản hồi tức thì (<100ms).
- **Mutations:** Cập nhật giỏ hàng (Quote Items) trong local state trước khi submit server.

---
Vui lòng gõ 'OK' để tôi tiến hành lập Kế hoạch Kỹ thuật & Contract.
