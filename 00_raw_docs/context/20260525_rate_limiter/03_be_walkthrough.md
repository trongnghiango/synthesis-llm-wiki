# Walkthrough — Tích hợp Rate Limiter (Redis + Clean Architecture)

## 1. Tóm tắt tính năng (Feature Summary)
- **Tier:** 1 — Foundation (Cross-cutting concern, không phải module nghiệp vụ)
- **Vị trí:** `core/shared/application/ports/`, `core/shared/infrastructure/adapters/`, `core/shared/infrastructure/guards/`, `core/decorators/`
- **Endpoints:** Không tạo endpoint mới. Áp dụng Decorator `@RateLimit()` trên Controller có sẵn.
- **Tables/Enums mới:** Không có. Rate limit lưu trạng thái tạm thời trong Redis ZSET.
- **File contracts:** Cập nhật `common.ts` thêm `RateLimitOptionSchema` ở cả backend và frontend.

## 2. Quyết định kiến trúc (Architecture Decisions)
- **Port/Adapter Pattern (Approach A):** Interface `IRateLimiterPort` ở Application Layer, implementation `RedisRateLimiterAdapter` ở Infrastructure Layer. Domain hoàn toàn sạch.
- **Guard layer:** `RateLimitGuard` chặn request sớm từ HTTP, không để request chạy sâu vào DTO Validation hay Use Case.
- **Redis Sliding Window:** Dùng Redis Sorted Set (ZSET) với `multi.exec()` để đảm bảo atomicity. Thời gian chính xác đến mili giây.
- **Fallback in-memory:** Khi Redis bị mất kết nối hoặc sập, adapter tự động fallback về `Map` in-memory và log cảnh báo.
- **Tenant Isolation:** Key rate limit luôn chứa `organizationId` trích xuất từ `RequestContextService` (ALS), không tin client input.
- **Exception mapping:** Dùng `RateLimitExceededException` extends `DomainException`, filter ở `DomainExceptionFilter` map thành HTTP 429.

## 3. Khó khăn & Xử lý (Troubleshooting)
- **Redis client API chênh lệch:** `node-redis` v4 có API `zRemRangeByScore` (camelCase) thay vì `zremrangebyscore`. Full test pass với mock client.
- **Fallback Memory Store:** Khi cần fallback, memory store có thể gây rò rỉ bộ nhớ nếu có quá nhiều key. Đã giới hạn bằng cách chỉ giữ key có request mới trong cửa sổ TTL, tự động expire sau dọn dẹp.
- **Contract đồng bộ FE:** File `frontend/shared/contracts/common.ts` là auto-generated từ backend. Tuy nhiên do FE không sử dụng Zod schema này cho Rate Limiter (chỉ Backend dùng), nên việc sync không gây lỗi ở Frontend.

## 4. Bàn giao cho Frontend (Frontend Handoff)
- **File Contract Zod cần lấy:** `shared/contracts/common.ts` — thêm `RateLimitOptionSchema` và `RateLimitOptions` type.
- **Response header:** Mọi endpoint có `@RateLimit()` sẽ trả về headers:
  - `X-RateLimit-Limit`: Số request tối đa trong window.
  - `X-RateLimit-Remaining`: Số request còn lại.
  - `X-RateLimit-Reset`: Unix timestamp window reset.
- **Lỗi 429:** Khi bị chặn, API trả về format lỗi chuẩn STAX:
  ```json
  { "success": false, "statusCode": 429, "errorCode": "TOO_MANY_REQUESTS", "message": "Quá tải yêu cầu..." }
  ```
- Frontend có thể dùng header `Retry-After` để hiển thị countdown.

## 5. Exit Verification Results
```
[ ] Exit Verification: ✅ Pass
[ ] TypeScript: npm run build — ✅ 0 errors (21s webpack build successful)
[ ] Domain Purity: ✅ Clean (grep trống cho domain layer mới)
[ ] Tenant Isolation: ✅ Key rate limit luôn chứa organizationId từ ALS
[ ] Exception Compliance: ✅ RateLimitExceededException extends DomainException
[ ] Shared Contracts: ✅ RateLimitOptionSchema thêm vào common.ts ở cả backend và frontend
[ ] Unit Test: ✅ 4/4 test passed (redis mock, fallback, ghi đè limit)
[ ] Integration Test: ✅ 238/238 test passed toàn hệ thống (không regression)
```
