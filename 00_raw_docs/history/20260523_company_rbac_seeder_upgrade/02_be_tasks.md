# Implementation Tasks — Company & RBAC Seeder Upgrade

Quy trình nâng cấp và kiểm thử bộ seeder CLI `seed:company` theo cơ cấu tổ chức STAFF.csv kết hợp:

```
[ ] 1.  Khởi tạo cấu trúc Hybrid và phân tích hai tệp CSV trong scripts/commands/seed-company.command.ts.
[ ] 2.  Triển khai thuật toán xóa dấu tiếng Việt nâng cao và fuzzy match so khớp hậu tố.
[ ] 3.  Triển khai thuật toán sinh Username chuẩn dạng [tên_chính][họ_chính] viết liền không dấu.
[ ] 4.  Bổ sung logic tạo cây phòng ban đa tầng: BOD độc lập, DỊCH VỤ KHÁCH HÀNG và các TEAM 01..04 phân cấp dưới DỊCH VỤ KHÁCH HÀNG.
[ ] 5.  Tự động hóa sinh Position chi tiết theo từng Team (ví dụ: Chuyên viên B2 thuộc TEAM 01).
[ ] 6.  Hỗ trợ định biên vị trí trống ("Tuyển mới") trong bảng positions mà không gắn user/employee.
[ ] 7.  Cập nhật thuật toán Upsert tài khoản users để tự động đồng bộ lại hashedPassword mới cho cả các user cũ.
[ ] 8.  Gán vai trò phân quyền tự động theo sơ đồ mới (ADMIN, MANAGER, SPECIALIST, ASSISTANT).
[ ] 9.  Đắp 100% dữ liệu hành chính sâu (CCCD, Ngân hàng, Bảo hiểm, Địa chỉ) từ THONG TIN NHAN VIEN.csv vào metadata JSONB của employees.
[ ] 10. Giải phóng kết nối PostgreSQL kết thúc an toàn.
[ ] 11. Dọn dẹp dữ liệu cũ bị sai lệch và chạy thử seeder.
[ ] 12. Thực thi kiểm thử TypeScript (npx tsc --noEmit) đảm bảo không có lỗi biên dịch.
```
