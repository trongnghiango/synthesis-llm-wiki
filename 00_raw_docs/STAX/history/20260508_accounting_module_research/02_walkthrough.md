# Walkthrough: Accounting Module Implementation (Phase 1)

Phân hệ Kế toán (Accounting) đã được xây dựng hoàn chỉnh về mặt giao diện và kết nối API, bám sát nghiệp vụ thực tế và phong cách thiết kế hiện đại của STAX.

## 1. Giao diện Tổng quan (Dashboard)
- **Bento Grid Stats**: Hiển thị nhanh các chỉ số quan trọng (Tài sản, Nợ, Doanh thu, Chi phí).
- **Dòng tiền trực quan**: Biểu đồ AreaChart so sánh Doanh thu vs Chi phí trong 6 tháng.
- **Tài khoản chính**: Theo dõi nhanh số dư của các tài khoản quan trọng (111, 112).

## 2. Hệ thống tài khoản (Chart of Accounts)
- **Cấu trúc phân tầng**: Hiển thị tài khoản dạng cây (Hierarchy) tương đồng với Sơ đồ tổ chức.
- **Phân loại thông minh**: Sử dụng màu sắc và icon riêng cho từng loại tài khoản (ASSET, LIABILITY...).
- **Khởi tạo nhanh**: Nút "Khởi tạo mẫu" giúp tạo nhanh bộ tài khoản chuẩn Thông tư 200/133.

## 3. Nhật ký chung (General Ledger)
- **Quản lý trạng thái**: Phân biệt rõ bút toán `Draft` (Nháp) và `Posted` (Đã ghi sổ).
- **Form Bút toán kép (Double-entry)**: 
    - Cho phép thêm/xóa dòng linh hoạt.
    - **Tính năng Balance Scale**: Tự động tính tổng Nợ/Có và hiển thị trạng thái "Cân đối" hoặc số tiền chênh lệch.
    - Ngăn chặn lưu bút toán nếu chưa cân đối, giúp giảm thiểu sai sót cho người dùng không chuyên.

## 4. Tích hợp Lead-to-Contract-to-Finote
- **Luồng chuyển đổi khép kín**: Khi chốt Lead thành Hợp đồng, người dùng có tùy chọn tạo ngay **Phiếu thu (Finote)** đợt 1.
- **Tự động hóa dữ liệu**: Số tiền và nội dung thu được kế thừa từ Báo giá (Quote), giúp giảm thiểu sai sót nhập liệu.
- **Liên kết nghiệp vụ**: Phiếu thu được liên kết trực tiếp với mã Hợp đồng mới tạo, giúp bộ phận kế toán dễ dàng theo dõi nguồn gốc dòng tiền.

## 5. Kỹ thuật & Kiến trúc
- **API Modular**: Tách biệt `accounting.api.ts` để dễ bảo trì.
- **TanStack Router**: Đăng ký Route sạch sẽ trong `accounting-routes.tsx`.
- **Zustand Persist**: Ghi nhớ trang làm việc cuối cùng (đã triển khai ở task trước).

---
*Mọi thành phần UI đã được tối ưu hóa cho cả Dark/Light mode và tuân thủ các quy tắc thẩm mỹ premium của STAX.*
