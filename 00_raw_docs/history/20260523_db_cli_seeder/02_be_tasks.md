# CLI Utility & Seeder Tool Implementation Tasks

Triển khai công cụ CLI chạy seeds và utility commands theo Modular Command Pattern.

## Danh sách Tasks thực thi tuần tự:
- [ ] 1. Khởi tạo cấu trúc thư mục `backend/scripts/` và `backend/scripts/commands/`
- [ ] 2. Tạo DB Client kết nối trực tiếp: `backend/scripts/db-client.ts`
- [ ] 3. Tạo Base Interface cho Command: `backend/scripts/commands/base.command.ts`
- [ ] 4. Tạo Command mẫu seed users: `backend/scripts/commands/seed-users.command.ts`
- [ ] 5. Tạo Điểm khởi chạy CLI chính: `backend/scripts/cli.ts`
- [ ] 6. Cập nhật NPM Scripts trong `backend/package.json`
- [ ] 7. Chạy thử nghiệm CLI: xem danh sách trợ giúp help
- [ ] 8. Chạy thử nghiệm CLI: thực thi seed:users --count 3 --clean
- [ ] 9. Kiểm tra biên dịch dự án: `npm run build`
- [ ] 10. Chạy Exit Verification checks và tạo tài liệu `03_be_walkthrough.md`
