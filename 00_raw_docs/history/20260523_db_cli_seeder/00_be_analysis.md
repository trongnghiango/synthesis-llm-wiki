# Business & Architecture Analysis: Database CLI Seeder & Utility Tool

## A. Phân loại Module
- **Tier phân loại:** Tier 1 — Foundation (Utility / Dev-tooling).
- **Dependencies:** 
  - Phụ thuộc: `drizzle-orm`, `pg` (PostgreSQL Client), `commander` (CLI parser), `dotenv` (nạp config), `tsx` (runtime chạy TypeScript).
  - Trực tiếp thao tác với cơ sở dữ liệu qua các Schema định nghĩa trong `src/database/schema/`.
  - Phụ thuộc gián tiếp vào file `.env` hoặc `.env.development`.
- **Quy tắc cô lập:** Không import `@nestjs/common`, `@nestjs/core` hoặc bất kỳ NestJS module nào để đảm bảo tốc độ khởi chạy tối đa của CLI.

## B. Bounded Context & Ubiquitous Language
Hệ thống CLI đóng vai trò như một "phương tiện vận chuyển và gieo trồng" (Seeding & Utility Dispatcher).
- **Seeder (Công cụ gieo dữ liệu):** Nhập dữ liệu thô giả định vào các bảng dữ liệu để hỗ trợ phát triển local hoặc tự động chạy test.
- **Utility Command (Lệnh tiện ích):** Các lệnh dọn dẹp (clean/wipe DB), đồng bộ hoặc kiểm tra nhanh.

| Tên nghiệp vụ | Tên kỹ thuật trong code | Mô tả |
|---|---|---|
| Bộ nạp CLI chính | `cli.ts` | Điểm bắt đầu nhận tham số từ terminal và dispatch đến command tương ứng |
| Trình kết nối DB trực tiếp | `db-client.ts` | Khởi tạo PostgreSQL connection pool và Drizzle DB instance |
| Lệnh con | `CliCommand` | Interface chuẩn hóa cho từng command độc lập |
| Lệnh Seed người dùng | `seed:users` | Script tự động xóa/thêm dữ liệu user phát triển |

## C. Data Flow & CLI Command Design
- **Flow:** CLI invocation (`tsx scripts/cli.ts <command> <options>`) -> Commander Parser -> Target `CliCommand.action(options, db)` -> Drizzle ORM -> PostgreSQL Database.
- **API (CLI Interface) Design:**
  - `stax-cli seed:users [-c, --clean] [-n, --count <number>]`

## D. Cross-module dependencies
CLI tool này không có ràng buộc API HTTP. Nó import trực tiếp toàn bộ database schema được gộp tại `backend/src/database/schema/index.ts`. 

## E. Multi-tenancy
- Trong kịch bản seed dữ liệu mẫu, dữ liệu cần có `organizationId` hợp lệ. Dữ liệu gieo sẽ tự động tạo `organizationId` mặc định hoặc ngẫu nhiên nếu không truyền vào, đảm bảo tuân thủ cấu trúc Multi-tenancy của hệ thống STAX.

## F. Security & Permission
- Công cụ CLI này chỉ được kích hoạt chạy ở local hoặc trong CI/CD pipeline thông qua quyền truy cập shell trực tiếp tới Server/Workspace. Không được expose qua HTTP API công khai.
- Quyền kết nối được bảo vệ bằng thông tin mật trong file cấu hình `.env` trên môi trường chạy.

---

Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết.
