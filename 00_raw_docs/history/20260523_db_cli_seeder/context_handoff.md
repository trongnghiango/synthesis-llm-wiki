# Handoff Summary: CLI Utility & Seeder Tool Setup

## Tổng quan
Bàn giao tài liệu thiết kế và lộ trình triển khai hệ thống CLI công cụ dùng để seed database hoặc chạy các tác vụ quản trị tiện ích bằng `tsx` và Drizzle client trực tiếp trên STAX Backend.

- **Skill vừa hoàn thành:** `stax-think` (Tư duy kiến trúc & Thiết kế)
- **Skill tiếp theo:** `stax-backend` (Cài đặt backend logic)

---

## Các quyết định đã khóa (KHÔNG được mở lại)
- **[D1] Engine kết nối:** Sử dụng `tsx` nạp trực tiếp Drizzle client độc lập, không thông qua NestJS IoC.
- **[D2] CLI Framework:** Sử dụng `commander` để xử lý parsing arguments/options.
- **[D3] Mô hình thiết kế:** Modular Command Pattern (mỗi command nằm ở một file riêng trong thư mục `backend/scripts/commands/`).
- **[D4] NPM Integration:** Thêm shorthand scripts trong `backend/package.json` (`cli`, `db:seed`, `db:seed:clean`).

---

## Các Giả định đã Document [ASSUMPTION]
- **[A1]:** Scripts chạy offline không yêu cầu các middleware, auth guard, hay context ALS (Async Local Storage) của NestJS hoạt động.
- **[A2]:** Dữ liệu mật khẩu seed mẫu được hash sẵn bằng thuật toán tương đương bcrypt được cấu hình trong hệ thống (`$2b$10$...`) để bypass việc sử dụng `AuthService`.
- **[A3]:** Connection string (`DATABASE_URL`) và các biến môi trường sẽ được load từ file `.env` (hoặc `.env.development`) phù hợp với môi trường đang chạy.

---

## Chi tiết các tệp tin cần tạo mới & Chỉnh sửa trong bước Cài đặt:

### 1. Tạo file cấu hình Client kết nối: `backend/scripts/db-client.ts`
Chứa logic cấu hình `Pool` từ `pg` và export `db` instance được liên kết với toàn bộ STAX `schema`.

### 2. Tạo Base Interface: `backend/scripts/commands/base.command.ts`
Chứa khai báo kiểu `CliCommand` thống nhất giao diện đầu vào cho mọi script command.

### 3. Tạo Điểm khởi chạy CLI: `backend/scripts/cli.ts`
Nơi nạp `commander`, đăng ký danh sách commands, chạy parse arguments và đóng pool connection an toàn khi hoàn thành.

### 4. Tạo Command mẫu: `backend/scripts/commands/seed-users.command.ts`
Triển khai logic seed User (hỗ trợ `--clean` và `--count`).

### 5. Cập nhật `backend/package.json`
Thêm các lệnh npm tương ứng.
