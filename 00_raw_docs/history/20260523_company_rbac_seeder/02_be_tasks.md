# Corporate & Specialized RBAC Seeder Implementation Tasks

Triển khai lệnh CLI `seed:company` đồng bộ hóa toàn bộ nhân sự thật và phân quyền dựa trên sơ đồ chức vụ.

## Danh sách Tasks thực thi tuần tự:
- [ ] 1. Vô hiệu hóa tính năng chạy seeder cũ khi NestJS boot (`RUN_SEEDS=false` mặc định trong config hoặc `.env.development`) để tối ưu hóa thời gian boot NestJS.
- [ ] 2. Tạo file script mới: `backend/scripts/commands/seed-company.command.ts`
- [ ] 3. Triển khai logic nạp Master Org STAX, Roles & Permissions (`ADMIN`, `MANAGER`, `SPECIALIST`, `ASSISTANT`) vào database.
- [ ] 4. Triển khai logic đọc tệp [THONG TIN NHAN VIEN.csv](THONG TIN NHAN VIEN.csv), parse dữ liệu tiếng Việt có dấu.
- [ ] 5. Triển khai logic tự động trích xuất & đồng bộ hóa `locations`, `grades`, `job_titles`, và `positions` từ dữ liệu thực tế của nhân sự.
- [ ] 6. Triển khai logic tạo `users`, `userMetadata` và liên kết `employees` với các thông tin cực kỳ chi tiết (SĐT, CCCD, Ngân hàng, Người thân).
- [ ] 7. Đăng ký lệnh `seedCompanyCommand` vào `backend/scripts/cli.ts`.
- [ ] 8. Cập nhật `package.json` để bổ sung alias script `npm run db:seed:company`.
- [ ] 9. Thực thi chạy thử nghiệm: `npm run db:seed:company`.
- [ ] 10. Chạy kiểm tra TypeScript compile và ESLint check trên toàn bộ thư mục `backend/scripts/`.
- [ ] 11. Chạy Unit Test suite để xác nhận không phát sinh lỗi biên dịch hay runtime.
- [ ] 12. Di chuyển toàn bộ tài liệu thiết kế nghiệp vụ vào `docs/history/20260523_company_rbac_seeder/`.
