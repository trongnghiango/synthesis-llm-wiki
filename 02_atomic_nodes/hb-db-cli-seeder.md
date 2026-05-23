```yaml
---
id: hb-db-cli-seeder
title: Công cụ CLI Seeder & Dọn dẹp Database
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Tích hợp CLI tool gieo dữ liệu mẫu (seeder) trực tiếp qua pg Pool & Commander, tối ưu hóa tốc độ và an toàn unique constraint."
tags: [cli, seeder, drizzle, pg-pool, developer-tooling]
---

## 1. Thiết kế Kiến trúc (Architecture Decisions)
- **Modular Command Pattern**: Tách biệt logic các commands tại `backend/scripts/commands/` (ví dụ: `seed:users`) và đăng ký tập trung tại entrypoint `backend/scripts/cli.ts`.
- **Offline Direct Connection**: Kết nối trực tiếp qua `pg` Pool và Drizzle schema, hoàn toàn không boot NestJS application nhằm tối ưu tốc độ thực thi (< 1 giây).
- **Graceful Uniqueness Suffix**: Sử dụng hậu tố thời gian ngẫu nhiên (`Date.now().toString().slice(-6)`) cho `username` và `email` để tránh lỗi unique constraint khi chạy liên tiếp.

## 2. CLI Contracts & NPM Commands
### CLI Commands:
```bash
# Gieo dữ liệu users (hỗ trợ dọn dẹp bảng trước khi gieo)
stax-cli seed:users [--clean] [--count <number>]
```

### NPM Scripts tích hợp (`backend/package.json`):
- `npm run cli` : Điểm thực thi CLI tổng quát (`cross-env NODE_ENV=development tsx scripts/cli.ts`).
- `npm run db:seed` : Alias chạy nhanh lệnh gieo dữ liệu users mẫu.

## 3. Ràng buộc Kỹ thuật & Khắc phục lỗi
- **Dependencies**: Tích hợp gói `commander` làm core xử lý CLI Arguments.
- **Tính năng Clean**: Flag `--clean` thực hiện truncate an toàn dữ liệu cũ trước khi chèn tập dữ liệu mới.
- **Tiêu chuẩn kiểm thử**: Đảm bảo TypeScript biên dịch thành công (`npm run build`) và ESLint kiểm tra `backend/scripts/` đạt `0 errors, 0 warnings`.
```