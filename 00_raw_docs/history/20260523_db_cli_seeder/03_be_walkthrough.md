# STAX Backend Integration Walkthrough: Database CLI Seeder & Utility Tool

## 1. Tóm tắt tính năng (Feature Summary)
- **Tier:** Tier 1 — Foundation (Utility / Dev-tooling).
- **CLI Commands đã tạo:**
  - `stax-cli seed:users` (hỗ trợ `--clean` và `--count <number>`).
- **NPM Shortcuts đã thêm:**
  - `npm run cli` - Điểm chạy CLI tổng quát (gọi `cross-env NODE_ENV=development tsx scripts/cli.ts`).
  - `npm run db:seed` - Gieo dữ liệu users mẫu nhanh.
- **Dependencies mới:**
  - Tích hợp thêm thư viện chuyên nghiệp `commander` vào dependencies của backend.

## 2. Quyết định kiến trúc (Architecture Decisions)
- **Modular Command Pattern:** Tách biệt database client và base interface với logic chạy của từng command. Điều này giúp các lệnh sau này (ví dụ: seed employees, seed CRM, clean audit logs...) có thể phát triển riêng rẽ ở các file tương ứng trong `backend/scripts/commands/` và chỉ cần import đăng ký trong `backend/scripts/cli.ts`.
- **Offline Direct connection:** Không boot NestJS application để kết nối tới database. CLI sử dụng trực tiếp pg Pool kết hợp Drizzle schema định nghĩa trong hệ thống, mang lại tốc độ chạy cực kỳ nhanh (dưới 1 giây).
- **Graceful Uniqueness Suffix:** Seed users mẫu sử dụng hậu tố timestamp/ngẫu nhiên ngắn (`Date.now().toString().slice(-6)`) cho phép chạy liên tiếp nhiều lần (`npm run db:seed`) mà không lo bị trùng lặp trường unique `username` trong database, đồng thời cung cấp tuỳ chọn `--clean` để làm sạch trước khi gieo.

## 3. Khó khăn & Xử lý (Troubleshooting)
- **Duplicate username key:** Ban đầu Drizzle báo lỗi unique constraint khi seed liên tục nhiều lần. Đã khắc phục bằng cách sử dụng random/timestamp suffix cho `username` và `email` để đảm bảo hoạt động an toàn và trơn tru.

## 4. Exit Verification Results
- **TypeScript compile:** ✅ `npm run build` compiled successfully.
- **Lint status:** ✅ `eslint backend/scripts/` verified 0 errors, 0 warnings.
- **Command execution:**
  - Lệnh trợ giúp: `npm run cli --help` hoạt động hoàn hảo.
  - Lệnh seed: `npm run db:seed` gieo dữ liệu thành công.
  - Tùy chọn dọn dẹp: `npm run cli -- seed:users --clean` dọn sạch dữ liệu cũ và gieo mới thành công.
