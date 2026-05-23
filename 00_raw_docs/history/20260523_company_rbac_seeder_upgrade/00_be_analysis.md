# Business & Architectural Analysis — Company & RBAC Seeder Upgrade

## A. Phân loại Module (Module Classification)
* **Phân tầng (Tier)**: Đây là **Tier 2 (Domain Core)** vì nó khởi tạo và đồng bộ hóa trực tiếp dữ liệu cơ cấu tổ chức (`orgUnits`, `positions`, `grades`, `jobTitles`) và nhân sự (`users`, `employees`) - vốn là DNA/xương sống vận hành của hệ thống STAX.
* **Mối phụ thuộc (Dependencies)**:
  - **Module phụ thuộc vào nó**: Các module nghiệp vụ thuộc Tier 3 (như `CRM`, `Accounting`, `Contracts`) phụ thuộc chặt chẽ vào cơ cấu phòng ban, định biên vị trí và tài khoản nhân viên hợp lệ để thực thi phân quyền và phê duyệt tài liệu.
  - **Module nó phụ thuộc**: Module `Rbac` (Tier 1) để liên kết quyền (`permissions`) vào vai trò (`roles`), gán vai trò vào người dùng (`userRoles`).

## B. Bounded Context & Ubiquitous Language
* **Domain**: `Organization Structure & HRM`
* **Từ điển Nghiệp vụ (Ubiquitous Language)**:
  | Thuật ngữ nghiệp vụ | Tên kỹ thuật trong cơ sở dữ liệu (Drizzle Schema) |
  | :--- | :--- |
  | Đơn vị Cơ cấu / Phòng ban | `orgUnits` |
  | Nhóm chức năng (con) | `orgUnits` (type: `'TEAM'`) |
  | Ban Giám đốc | `orgUnits` (type: `'BOD'`) |
  | Định biên Vị trí | `positions` |
  | Cấp bậc | `grades` |
  | Chức danh công việc | `jobTitles` |
  | Hồ sơ nhân sự | `employees` |
  | Tài khoản người dùng | `users` |
  | Gán vai trò người dùng | `userRoles` |

## C. Data Flow & API Design
Vì đây là một tác vụ chạy qua giao diện dòng lệnh (CLI Utility) để hỗ trợ quá trình gieo dữ liệu (seeder) cực nhanh không thông qua NestJS IoC:
* **Dòng dữ liệu (Data Flow)**:
  - CLI `npm run db:seed:company` ➔ `scripts/cli.ts` ➔ `seedCompanyCommand` ➔ Đọc `STAFF.csv` và `THONG TIN NHAN VIEN.csv` ➔ Kết nối trực tiếp qua `pg` connection pool ➔ Thực thi Drizzle Query và Insert/Update lên Database.
* **API Endpoints**: Không áp dụng vì đây là tác vụ offline/CLI seeder.

## D. Cross-module dependencies
* **Port/Interface**: Không áp dụng trực tiếp do CLI chạy độc lập bằng raw Drizzle.
* **Domain Events**: CLI không phát sinh Domain Events thời gian thực để tránh nghẽn hàng đợi (message queue/event bus) trong lúc seed dữ liệu số lượng lớn.

## E. Multi-tenancy
* Toàn bộ dữ liệu phòng ban, định biên, nhân viên đều được gắn chặt vào `organizationId = 1` đại diện cho `STAX ENTERPRISE` (Master Organization).
* Logic cô lập (Tenant Isolation) được đảm bảo: không bypass, mọi bản ghi đều gắn khóa ngoại `organizationId` chỉ đến STAX.

## F. Security & RBAC (`_actions` / Server-Driven UI)
* Mọi nhân sự được đồng bộ sẽ được gán các vai trò tương thích tự động dựa trên vị trí:
  - `Tổng Giám đốc` ➔ `ADMIN` (kế thừa đầy đủ đặc quyền quản trị).
  - `Giám đốc` ➔ `MANAGER` (vai trò quản lý bộ phận).
  - `Chuyên viên B1 / B2` ➔ `SPECIALIST` (vai trò chuyên viên nghiệp vụ).
  - `Trợ lý A1 / A2 / A1.2` ➔ `ASSISTANT` (vai trò trợ lý hỗ trợ).
* Việc phân quyền được kiểm soát chặt chẽ thông qua việc kế thừa quyền (`copyPermissions`) giữa các vai trò cha-con (`SUPER_ADMIN` -> `ADMIN`, `STAFF` -> `SPECIALIST`/`ASSISTANT`).
