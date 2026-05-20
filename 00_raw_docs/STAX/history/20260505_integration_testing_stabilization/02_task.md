# Chiến dịch Phủ Test Toàn Diện - Phase 1

## Giai đoạn 1: Foundation Services (Tier 1)
- `[x]` Viết Unit Test cho `UserService` (`user.service.spec.ts`)
  - Test case: createUser (Thành công, Lỗi trùng user, Lỗi mật khẩu yếu)
  - Test case: validateCredentials
  - Test case: getUserById, updateUserProfile, deactivateUser
- `[x]` Viết Unit Test cho `AuthenticationService` (`authentication.service.spec.ts`)
  - Test case: login (Thành công, Lỗi sai thông tin, Lỗi tài khoản bị khóa)
  - Test case: generateTokenPair, getNewTokens
  - Test case: logout, validateUser
- `[x]` Viết Unit Test cho `OrgStructureService` (`org-structure.service.spec.ts`)
  - Test case: createOrgUnit (Thành công, Lỗi không tìm thấy cha)
  - Test case: moveOrgUnit (Thành công, Lỗi chu trình)
  - Test case: buildTree
- `[x]` Viết Unit Test cho `PermissionService` (`permission.service.spec.ts`)
  - Test case: checkPermission (Global Admin, Có quyền trực tiếp, Có quyền gián tiếp)
  - Test case: getGroupedPermissions

## Cột mốc hoàn thành Phase 1 ✅
- [x] Chạy `npm run test` đảm bảo 100% test pass.
- [x] Chạy `npm run test:cov` để kiểm tra độ phủ (Coverage) của Tier 1.

# Chiến dịch Phủ Test Toàn Diện - Phase 2 (CRM & Accounting)

## Giai đoạn 2: Nghiệp vụ CRM & Kế toán (Tier 2) ✅
- [x] Viết Unit Test cho `LeadQueryService` & `OrganizationQueryService`
- [x] Viết Unit Test cho `ContractService` & `QuoteService`
- [x] Viết Unit Test cho `FinoteService` (Thanh toán & Thu chi)
- [x] Viết Unit Test cho `FinoteDocumentService` (PDF & Tài liệu)

## Giai đoạn 3: Phủ Test Repository (Integration Test) ✅
- `[x]` Chuyển đổi hạ tầng In-Memory DB sang `@electric-sql/pglite` để hỗ trợ hoàn toàn Drizzle ORM (bao gồm `rowMode` và `LEFT JOIN LATERAL`).
- `[x]` Cấu hình Jest hỗ trợ `PGLite` WASM qua Node flag `--experimental-vm-modules`.
- `[x]` Cập nhật `test-db.helper.ts` tích hợp toàn bộ Schema Core và CRM.
- `[x]` Phủ test thành công cho `DrizzleUserRepository` (7/7 pass).
- `[x]` Phủ test thành công cho `DrizzleOrganizationRepository` (6/6 pass).
- `[x]` Phủ test thành công cho `DrizzleLeadRepository` (5/5 pass).
