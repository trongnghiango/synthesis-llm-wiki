# Business & Architecture Analysis: Corporate Seeder & Specialized RBAC System

## A. Phân loại Module
- **Tier phân loại:** Tier 1 — Foundation (Dev-tooling / Identity / RBAC).
- **Dependencies:** `drizzle-orm`, `pg`, `commander`, `csv-parse`, `tsx`.
- **Quy tắc cô lập:** Tuyệt đối không nạp NestJS IoC runtime để giữ tốc độ chạy CLI dưới 1 giây. Set `RUN_SEEDS=false` trong NestJS bootstrap để giải phóng NestJS khởi động cực nhanh, chuyển giao trách nhiệm seeding hoàn toàn cho CLI script.

## B. Bounded Context & Ubiquitous Language

| Tên nghiệp vụ | Tên kỹ thuật trong code | Mô tả |
|---|---|---|
| Master Organization | `STAX ENTERPRISE` | Tổ chức mẹ sở hữu sơ đồ phòng ban và quản lý nhân sự |
| Vị trí định biên | `positions` | Thực thể định danh vị trí công việc, liên kết giữa Phòng ban, Chức danh và Bậc lương |
| Hồ sơ nhân sự | `employees` | Thực thể chứa dữ liệu hành chính chi tiết (SĐT, CCCD, Ngân hàng, Gia đình...) |
| Lệnh Seed doanh nghiệp | `seed:company` | Script tự động đọc `THONG TIN NHAN VIEN.csv` và đồng bộ hóa toàn bộ sơ đồ |

## C. Data Flow & CLI Design
- **Flow:** `npm run cli -- seed:company` -> Commander Parser -> `seedCompanyCommand.action` -> parse [THONG TIN NHAN VIEN.csv](THONG TIN NHAN VIEN.csv) -> Drizzle ORM -> PostgreSQL database.
- **Workflow cấp phát phân quyền (Role Assignment Logic):**
  - **CEO** -> Gán vai trò `ADMIN` + full permissions.
  - **Quản lý** -> Gán vai trò `MANAGER` + permissions quản lý phòng ban.
  - **Chuyên viên B1 / B2** -> Gán vai trò `SPECIALIST` + permissions nghiệp vụ nâng cao.
  - **Trợ lý A1 / A2** -> Gán vai trò `ASSISTANT` + permissions nhập liệu và crm cơ bản.

## D. Multi-tenancy
- Tất cả các bản ghi `employees`, `orgUnits`, `locations`, `positions`, `grades`, `jobTitles` của STAX nhân viên đều được gắn cứng `organizationId` của `STAX ENTERPRISE` được tạo tự động ở Bước 1.

## E. Security (`_actions` / Server-Driven UI)
- Trạng thái hoạt động (`status`) của nhân viên lấy từ cột `TÌNH TRẠNG LÀM VIỆC`:
  - `Working` -> `ACTIVE` (Cho phép kích hoạt tài khoản `users`).
  - `Left` -> `RESIGNED` (Vô hiệu hóa tài khoản `users.isActive = false`).

---

Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết (Bước 2).
