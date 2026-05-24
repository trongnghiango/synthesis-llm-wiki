# Tasks Checklist: Tenant Isolation & Casing Fix

**Ngày checklist:** 2026-05-23
**Handoff Plan:** `lively-crafting-trinket.md`
**Chế độ:** Handoff của Backend (`stax-backend`)

---

## 📋 Danh sách Task Thực thi

- [ ] **1. Sửa lỗi casing trong `VisibilityResolverService`**
  - [ ] Cập nhật file: `backend/src/modules/user/application/services/visibility-resolver.service.ts`
  - [ ] Chuẩn hóa `roles` của user sang chữ in hoa (`toUpperCase()`) trước khi so sánh với `'ADMIN'`, `'SUPER_ADMIN'`, `'MANAGER'`.

- [ ] **2. Siết chặt bảo mật Fallback tại `ContractController`**
  - [ ] Cập nhật file: `backend/src/modules/crm/infrastructure/controllers/contract.controller.ts`
  - [ ] Import `ForbiddenException` từ `@nestjs/common` (nếu chưa có).
  - [ ] Cập nhật logic `tenantId` cho các endpoint `getContracts` và `getContractDetail` để ngăn chặn fallback mặc định về `1` đối với người dùng bên ngoài không có `organizationId`.
  - [ ] Áp dụng logic kiểm tra và ném `ForbiddenException` cho các endpoint `activateContract`, `suspendContract`, `terminateContract`, `uploadAttachment`, `generatePdf`.

- [ ] **3. Siết chặt bảo mật Fallback tại các Controller khác khi Upload Attachment**
  - [ ] Cập nhật file: `backend/src/modules/crm/infrastructure/controllers/quote.controller.ts`
  - [ ] Cập nhật file: `backend/src/modules/crm/infrastructure/controllers/lead.controller.ts`
  - [ ] Cập nhật file: `backend/src/modules/crm/infrastructure/controllers/organization.controller.ts`
  - [ ] Đảm bảo chỉ có nhân viên nội bộ (`isInternal === true`) mới được phép fallback về `1` nếu thiếu `organizationId`, còn lại ném lỗi `ForbiddenException` ngay lập tức.

- [ ] **4. Tích hợp `applyTenantIsolation` vào `DrizzleContractRepository`**
  - [ ] Cập nhật file: `backend/src/modules/crm/infrastructure/persistence/drizzle-contract.repository.ts`
  - [ ] Thay thế kiểm tra `orgId > 1` thủ công bằng lời gọi `this.applyTenantIsolation(conditions, schema.contracts)`.
  - [ ] Cập nhật các hàm `findById`, `findDetailById`, và `findMany` để sử dụng cơ chế bảo mật tự động này.

- [ ] **5. Kiểm toán & Chạy thử nghiệm hệ thống**
  - [ ] Chạy unit tests cho auth module: `npm run test -- src/modules/auth/`
  - [ ] Chạy unit tests cho user module: `npm run test -- src/modules/user/`
  - [ ] Chạy build dự án đảm bảo 0 lỗi TypeScript: `pnpm run build` hoặc `npm run build` trong thư mục backend.

- [ ] **6. Bàn giao & Ghi log**
  - [ ] Viết tài liệu `03_be_walkthrough.md` trong thư mục context.
  - [ ] Cập nhật file `docs/STAX/06_CHANGELOG.md` ghi nhận các thay đổi.

---

Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
