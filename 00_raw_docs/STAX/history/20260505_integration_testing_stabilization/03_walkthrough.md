# Walkthrough: Chiến dịch Phủ Test Toàn Diện - Phase 1 & 2

## Kết quả tổng quan

```
Test Suites: 10 passed, 10 total
Tests:       43 passed, 43 total
Time:        ~13s
Exit code:   0
```

---

## Phase 1: Foundation Services ✅ (23 tests)

### Thắt chặt Kiến trúc (Architectural Hardening)
Trước khi viết test, rà soát và loại bỏ toàn bộ **Framework Leak** trong Application Layer:
- Thay `NotFoundException` → `EntityNotFoundException`
- Thay `BadRequestException` → `BusinessRuleValidationException`
- Thay `ForbiddenException` → `BusinessRuleValidationException` hoặc `UnauthorizedException`

Các file đã được làm sạch: `AuthService`, `UserService`, `OrgStructureService`, `ContractService`, `LeadQueryService`, `RbacManageService`, `RoleService`, `QuoteService`.

### Các Service đã phủ test

| Service | Tests | Highlights |
|---|---|---|
| `UserService` | 7 | Tạo user, deactivate, validateCredentials |
| `AuthenticationService` | 8 | Login, Refresh Token Rotation, Logout |
| `OrgStructureService` | 5 | Path-based Tree, tạo Root/Child unit |
| `PermissionService` | 3 | Super Admin Bypass, Redis Cache, Grouped Permissions |

### Các vấn đề đã fix
- Mock JWT synchronous (`sign`/`verify`) thay vì async
- Mock `ConfigService` đúng giá trị TTL cho session
- Mock `createOrgUnit`/`updateOrgUnit` thay cho generic `save`
- Exception messages phải khớp chính xác với tiếng Việt trong domain

---

## Phase 2: CRM & Accounting Services ✅ (20 tests)

### Các Service đã phủ test

| Service | Tests | Highlights |
|---|---|---|
| `LeadQueryService` | 5 | Multi-tenant isolation, `_actions` logic (edit/close_won) |
| `OrganizationQueryService` | 2 | Phân trang, `_actions` edit chỉ cho Admin |
| `ContractService` | 3 | findById, getContracts, EntityNotFoundException |
| `QuoteService` | 4 | Tạo Quote từ Lead, tính thuế tự động, state machine |
| `FinoteService` | 4 | Approve/Reject, createFinote với Money VO |
| `FinoteDocumentService` | 2 | Generate PDF, attach, EntityNotFoundException |

### Các vấn đề đã fix
- `LeadStage.OPEN` không tồn tại → đổi sang `LeadStage.NEW`
- Mock `save` trả spread object làm mất getters của entity → trả về chính instance
- Thiếu required props (`title`, `deadlineAt`) trong Finote constructor
- `QuoteService` còn sót `ForbiddenException`/`BadRequestException` → refactor sang Domain Exceptions

---

## Kiến trúc tuân thủ

Sau 2 Phase, Application Layer đã hoàn toàn **Framework Agnostic**:
- ✅ Không còn `import { NotFoundException } from '@nestjs/common'` trong bất kỳ service nào
- ✅ Domain Exception được dùng nhất quán (`@core/shared/domain/exceptions/base.exceptions`)
- ✅ Tất cả mock tuân theo Repository Interface (Port), không mock triển khai Drizzle cụ thể

---

---

## Phase 3: Repository Integration Tests ✅ (18 tests)

### Bước ngoặt Kiến trúc: Thay thế `pg-mem` bằng `PGLite`
Quá trình tích hợp vấp phải các giới hạn nghiêm trọng của `pg-mem` khi chạy Drizzle ORM:
1. **Lỗi getTypeParser**: `pg-mem` không hỗ trợ cấu hình type parser của `pg`. Đã xử lý bằng Monkey Patch.
2. **Lỗi rowMode**: Drizzle yêu cầu `rowMode: 'array'` cho Prepared Statements. Đã xử lý bằng Monkey Patch map kết quả sang mảng.
3. **Lỗi LEFT JOIN LATERAL**: Các truy vấn quan hệ (`db.query.findFirst({ with: ... })`) tạo ra SQL dùng `LEFT JOIN LATERAL`. `pg-mem` có bug scoping không nhận diện được alias của bảng ngoài cùng. 

**Quyết định:** Thay vì viết lại query phá vỡ kiến trúc, chúng ta đã thay thế `pg-mem` bằng **`@electric-sql/pglite`**.
- PGLite chạy một engine PostgreSQL thực thụ biên dịch sang WebAssembly.
- Tương thích 100% với Drizzle ORM (không cần Monkey Patch).
- Cấu hình Jest chạy với `--experimental-vm-modules` để hỗ trợ WASM dynamic import.

### Các Repository đã phủ test

| Repository | Tests | Thời gian | Highlights |
|---|---|---|---|
| `DrizzleUserRepository` | 7 | ~37s | test `insert...returning`, `findByUsername`, nested relations (metadata, roles) |
| `DrizzleOrganizationRepository` | 6 | ~34s | test CRUD, seed data |
| `DrizzleLeadRepository` | 5 | ~35s | test `findAll` với filter `organizationId` |

> [!NOTE]
> Thời gian chạy chậm hơn unit test vì PGLite khởi tạo WASM PostgreSQL engine in-memory cho mỗi test suite, nhưng đổi lại tính đúng đắn (correctness) tuyệt đối giống hệt môi trường Production.

### Các vấn đề đã fix
- Sửa lỗi import thừa `LeadSource` trong `drizzle-lead.repository.spec.ts`.
- Cập nhật schema `contacts` trong `test-db.helper.ts` để đồng bộ với production (thêm `userId`, `address`, `jobTitle`, `isPrimary`).

---

## Bước tiếp theo
Chuyển sang thử nghiệm e2e test, API Controller layer, hoặc bắt tay vào frontend.
