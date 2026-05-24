### [2026-05-23] - Chuẩn hóa Bảo mật Đa thuê (Tenant Isolation) & Khắc phục Lỗi Casing Role
- **Module:** `user`, `crm`, `accounting`, `hrm`, `system`
- **Loại:** `Auditor-Fix`
- **Thay đổi:**
  - Khắc phục lỗi so sánh casing vai trò người dùng trong `VisibilityResolverService`.
  - Loại bỏ fallback `|| 1` không an toàn ở các CRM Controllers, siết chặt kiểm tra và ném `ForbiddenException` cho các tài khoản ngoài thiếu `organizationId`.
  - Nâng cấp `applyTenantIsolation` ở lớp cha `DrizzleBaseRepository` để hỗ trợ lọc tự động cả bảng Organizations (`table.id`), bảng Finotes (`table.tenantId`), và các bảng dữ liệu con khác (`table.organizationId`).
  - CRM Module: Tích hợp `applyTenantIsolation` vào các hàm query của `DrizzleOrganizationRepository`, `DrizzleLeadRepository`, `DrizzleQuoteRepository`, `DrizzleContactRepository`, và `DrizzleServiceAssignmentRepository`.
  - HRM/Employee Module: Tích hợp `applyTenantIsolation` vào các truy vấn trong `DrizzleEmployeeRepository`, `DrizzleEmployeeTaskRepository`, và `DrizzleOrgStructureRepository` (bao gồm locations, grades, jobTitles, orgUnits, positions).
  - Accounting Module: Tích hợp `applyTenantIsolation` vào các truy vấn trong `DrizzleFinoteRepository`, `DrizzleCashFundRepository`, `DrizzleAccountRepository`, `DrizzleJournalRepository`, và `DrizzleFinotePaymentRepository`.
  - System Module: Tích hợp `applyTenantIsolation` vào các truy vấn trong `DrizzleAttachmentRepository`.
  - Xác thực thành công: Backend build thành công không lỗi TypeScript, tất cả 234 test cases đều vượt qua hoàn hảo.
# STAX V2 Changelog

Lưu trữ lịch sử các thay đổi nhỏ, sửa lỗi, và micro-features trong hệ thống STAX.

### [2026-05-21] - Chuyển Google Drive Storage từ Service Account sang OAuth 2.0

- **Module:** `system`
- **Thay đổi:**
  - Thêm mới `google-oauth.service.ts`: Xử lý OAuth 2.0 Authorization Code Flow và tự động refresh `access_token` bằng `refresh_token` lưu trong `.env`.
  - Rewrite `google-drive.service.ts`: Loại bỏ hoàn toàn dependency `googleapis` SDK, thay bằng Google Drive REST API v3 gọi qua `fetch()` + `GoogleOAuthService`. `IFileStoragePort` interface giữ nguyên → `AttachmentService` không bị ảnh hưởng.
  - Thêm mới `google-drive.controller.ts`: 2 endpoint setup 1-time (`GET /api/google/authorize` cần quyền `system:admin`, `GET /api/google/callback` là `@Public()`).
  - Cập nhật `google-drive.config.ts`: Thay `serviceAccountJsonPath` bằng các OAuth2 fields (`clientId`, `clientSecret`, `redirectUri`, `refreshToken`).
  - Cập nhật `system.module.ts`: Đăng ký `GoogleOAuthService` provider và `GoogleDriveController`.
  - Cập nhật `.env.development`: Thay section Service Account bằng section OAuth 2.0 với hướng dẫn lấy `refresh_token`.

### [2026-05-20] - Sửa lỗi pgEnum Mismatch khi Cập nhật Trạng thái Lead


- **Module:** `crm`
- **Thay đổi:**
  - Cập nhật `LeadMapper` (`backend/src/modules/crm/infrastructure/mappers/lead.mapper.ts`) để ánh xạ chính xác giữa Domain enum `LeadStage` (`CONSULTING`, `NEGOTIATING`) và Database pgEnum `lead_status` (`CONTACTED`, `NEGOTIATION`).
  - Đã khắc phục lỗi `500 INTERNAL_SERVER_ERROR` khi kéo thả hoặc cập nhật trạng thái Lead.
  - Cập nhật hiển thị thời gian ở góc dưới trái thẻ Kanban từ `createdAt` (ngày hệ thống) sang `acquiredAt` (ngày tiếp nhận nghiệp vụ thực tế) để thông tin hiển thị chính xác hơn đối với dữ liệu import/seed.
  - Sửa lỗi API: Bổ sung trường `acquiredAt` vào `LeadResponseDto` và ánh xạ đầy đủ trong `LeadQueryService.mapToResponse` để Frontend nhận được giá trị `acquiredAt` thực tế từ cơ sở dữ liệu thay vì `undefined`.

