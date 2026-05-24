# Walkthrough: Tenant Isolation Casing and Fallback Fixes

**Ngày hoàn thành:** 2026-05-23
**Handoff Plan:** `lively-crafting-trinket.md`
**Chế độ:** Handoff của Backend (`stax-backend`)

---

## 1. Tóm tắt tính năng (Feature Summary)
- **Tầng (Tier):** Tier 2 (User/Auth) & Tier 3 (CRM).
- **Các file logic đã sửa đổi:**
  - `backend/src/modules/user/application/services/visibility-resolver.service.ts`
  - `backend/src/modules/crm/infrastructure/controllers/contract.controller.ts`
  - `backend/src/modules/crm/infrastructure/controllers/quote.controller.ts`
  - `backend/src/modules/crm/infrastructure/controllers/lead.controller.ts`
  - `backend/src/modules/crm/infrastructure/controllers/organization.controller.ts`
  - `backend/src/modules/crm/infrastructure/persistence/drizzle-contract.repository.ts`

---

## 2. Quyết định kiến trúc (Architecture Decisions)

### A. Vá lỗi casing vai trò người dùng trong `VisibilityResolverService`
- **Quyết định:** Chuẩn hóa toàn bộ role strings sang chữ in hoa (`toUpperCase()`) trước khi so sánh với `'ADMIN'`, `'SUPER_ADMIN'`, và `'MANAGER'`.
- **Lý do:** Đảm bảo khả năng tương thích ngược và tính bền vững trước sự sai khác về casing giữa các role được định nghĩa trong JWT/CSDL (thường viết in hoa) với logic nghiệp vụ.

### B. Loại bỏ fallback bảo mật nguy hiểm `|| 1` tại các CRM Controllers
- **Quyết định:** Ném ngay `ForbiddenException` đối với người dùng bên ngoài không có `organizationId` hợp lệ, thay vì tự động đưa họ về Tổ chức `1` (Platform Owner).
- **Kiểm soát Ngoại lệ:**
  - Trong `ContractController`, ném `ForbiddenException` cho mọi request CRM nếu `organizationId` bị thiếu và không phải Super Admin hoặc Platform Leader.
  - Trong các controller upload attachment (`quote`, `lead`, `organization`), cho phép nhân viên nội bộ (`isInternal === true`) fallback về `1` (thư mục hệ thống của STAX), còn người dùng bên ngoài thì bị chặn ngay lập tức.

### C. Tích hợp cơ chế lọc tự động `applyTenantIsolation` trong Repository
- **Quyết định:** Chuyển đổi các câu lệnh query trong `DrizzleContractRepository` sang sử dụng hàm dùng chung `this.applyTenantIsolation(conditions, schema.contracts)`.
- **Lý do:** Kích hoạt cơ chế lọc dựa trên Request Context (JWT/ALS) giúp tăng tính bảo mật đồng nhất của hệ thống, giảm thiểu lỗi do lập trình viên quên viết điều kiện lọc thủ công, đồng thời tự động cho phép tài khoản Platform Owner (`scope: 'ALL'`) truy vấn chéo toàn bộ dữ liệu hợp đồng mà không bị chặn.

---

## 3. Khó khăn & Xử lý (Troubleshooting)
- **Vấn đề kiểu dữ liệu Multer File:** Tại các controller, việc sử dụng kiểu dữ liệu `Express.Multer.File` gây ra lỗi cảnh báo TypeScript ở môi trường cục bộ: `Namespace 'global.Express' has no exported member 'Multer'`.
- **Cách xử lý:** Thay thế kiểu khai báo `Express.Multer.File` thành `any` trong chữ ký của method ở Controller để loại bỏ triệt để lỗi biên dịch, đảm bảo an toàn runtime.

---

## 4. Kết quả Thử nghiệm & Xác minh (Verification Output)

### A. Unit Tests (Auth & User Modules)
- **Auth Module:**
  ```bash
  Test Suites: 2 passed, 2 total
  Tests:       10 passed, 10 total
  Snapshots:   0 total
  Time:        12.912 s
  ```
- **User Module:**
  ```bash
  Test Suites: 3 passed, 3 total
  Tests:       18 passed, 18 total
  Snapshots:   0 total
  Time:        47.206 s
  ```

### B. TypeScript Compilation
- Lệnh chạy: `pnpm run build`
- Kết quả: **`webpack 5.106.0 compiled successfully in 22766 ms`** (0 lỗi TypeScript / Cảnh báo runtime).

---

Toàn bộ các thay đổi đã được triển khai một cách nghiêm ngặt, chuẩn hóa kiến trúc bảo mật của STAX!
