# 00. Phân tích: Chuyển Google Drive từ Service Account → OAuth 2.0

**Ngày:** 2026-05-21 | **Tier:** 1 — Foundation | **Scope:** Infrastructure Refactor

## A. Phân loại module
- **Tier 1 — Foundation** (`system` module): Không chứa logic nghiệp vụ, cung cấp `IFileStoragePort` cho toàn hệ thống.
- Phụ thuộc vào: `ConfigModule` (lấy env vars OAuth).
- Được phụ thuộc bởi: `AttachmentService` (inject `IFileStoragePort`).

## B. Bounded Context
| Nghiệp vụ | Kỹ thuật |
|---|---|
| Kho lưu trữ file | `IFileStoragePort` |
| Xác thực với Google | `GoogleOAuthService` |
| Upload/Delete file | `GoogleDriveService` implements `IFileStoragePort` |
| Lấy authorization code 1 lần | `GoogleDriveController` (`/api/google/authorize`, `/api/google/callback`) |

## C. Lý do chuyển đổi
Google Workspace mặc định **chặn tạo Service Account key** theo chính sách tổ chức. OAuth 2.0 Authorization Code Flow với `refresh_token` là giải pháp thay thế:
- Admin chạy flow 1 lần → lấy `refresh_token` → lưu vào `.env`
- Runtime: `GoogleOAuthService.refreshAccessToken()` tự động renew `access_token`

## D. Thay đổi cụ thể
1. **Xóa dependency:** `googleapis` package (Service Account SDK)
2. **Thêm:** `GoogleOAuthService` (infrastructure service) — OAuth2 flow thuần `fetch`
3. **Rewrite:** `GoogleDriveService` — thay `google.drive(v3)` bằng Google Drive REST API v3 + OAuth token
4. **Thêm:** `GoogleDriveController` — 2 endpoint setup 1-time (cần `@Public()` cho callback, guard `/authorize`)
5. **Cập nhật:** `google-drive.config.ts` — thêm OAuth env vars
6. **Cập nhật:** `system.module.ts` — đăng ký providers và controller mới

## E. Multi-tenancy
Không áp dụng — đây là infrastructure layer, không lưu data theo `organizationId`.

## F. Security
- `GET /api/google/authorize` → Nên có `@JwtAuthGuard` (chỉ STAX Admin mới được khởi tạo OAuth)
- `GET /api/google/callback` → `@Public()` vì Google redirect về (không có Bearer token)
- `refresh_token` lưu trong `.env`, **không lưu DB**
