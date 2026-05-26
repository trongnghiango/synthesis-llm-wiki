# Kế hoạch Kiến trúc Chi tiết: Rate Limiter

## Tổng quan

Rate Limiter là cross-cutting concern ở cấp Foundation, được tích hợp hoàn toàn trong `core/shared/` mà không tạo module riêng biệt. Nó bảo vệ toàn bộ API thông qua Guard điều khiển bởi Decorator.

---

## A. Database Schema

Rate Limiter **không cần tạo bảng hay pgEnum nào**. Toàn bộ trạng thái rate-limit được lưu trong Redis qua Sorted Set (ZSET) — đây là kiểu lưu trữ dữ liệu tạm thời (transient), bản thân dữ liệu không cần migrate.

> **Không có cơ sở dữ liệu, không có table mới, không có enum mới, không có migration.**

---

## B. Domain Layer — Không phụ thuộc Framework

### RateLimitRequest Interface (TypeScript thuần)

```typescript
// core/shared/application/ports/rate-limiter.port.ts
export interface RateLimitRequest {
  key: string;
  limit: number;
  ttl: number; // seconds
}

export interface RateLimitResult {
  isAllowed: boolean;
  remaining: number;
  reset: number; // unix timestamp
}
```

### Domain Exception (bổ sung mapping)

Chúng ta cần thêm mã lỗi `TOO_MANY_REQUESTS` vào `DomainExceptionFilter` để map `BusinessRuleValidationException` → HTTP 429 khi rate limit bị vượt. Không cần tạo Exception class mới.

---

## C. Infrastructure Layer — Framework-aware

### 1. Decorator `@RateLimit`

**Đường dẫn:** `backend/src/core/decorators/rate-limit.decorator.ts`

```typescript
export const RATE_LIMIT_KEY = 'rate_limit_options';
export function RateLimit(options?: Partial<RateLimitOptions>): MethodDecorator;
```

Set metadata + `UseGuards(RateLimitGuard)` internally.

### 2. Guard `RateLimitGuard`

**Đường dẫn:** `backend/src/core/shared/infrastructure/guards/rate-limit.guard.ts`

- Inject `IRateLimiterPort` (Symbol DI token).
- Đọc `RateLimitOptions` từ `Reflector`.
- Tự động giải quyết key dựa vào ALS store (lấy `organizationId`, `userId`, `ip`).
- Nếu bị chặn → throw `BusinessRuleValidationException`.

### 3. Redis Adapter

**Đường dẫn:** `backend/src/core/shared/infrastructure/adapters/redis-rate-limiter.adapter.ts`

- Implement `IRateLimiterPort`.
- Sử dụng Redis Sorted Set (ZSET) + Lua script hoặc multi/exec cho sliding window.
- Tận dụng kết nối `CACHE_MANAGER` hiện có.

### 4. Module đăng ký

**Đường dẫn:** `backend/src/core/shared/infrastructure/rate-limiter.module.ts`

- Cung cấp `IRateLimiterPort` → `RedisRateLimiterAdapter`.
- Export guard + port.

---

## D. Application Layer — Orchestration only

Không có Service ở Application Layer cho Rate Limiter. Đây là cross-cutting concern infrastructure-only (`IRateLimiterPort` + Guard), không có Use Case hay Business Logic cần phối hợp.

Port interface `IRateLimiterPort` được đặt tại `core/shared/application/ports/` để tuân thủ Dependency Inversion, và sẵn sàng cho bất kỳ ai muốn inject dùng thủ công.

---

## E. Presentation Layer & Contracts

### Zod Schema Contract

**Đường dẫn:** `frontend/shared/contracts/common.ts` (thêm vào) & `backend/src/core/shared/contracts/common.ts` (đồng bộ)

```typescript
export const RateLimitOptionSchema = z.object({
  limit: z.number().int().positive().default(60),
  ttl: z.number().int().positive().default(60),
  strategy: z.enum(['IP', 'USER', 'TENANT', 'COMBINED']).default('COMBINED'),
});
```

### Controller (Ví dụ sử dụng — không implement ngay)

```typescript
@Post()
@RateLimit({ limit: 10, ttl: 60, strategy: 'TENANT' })
async createLead() { ... }
```

Không tạo Controller mới. Decorator sử dụng trên các Controller hiện tại.

---

## F. Module Wiring

Không tạo module riêng. Đăng ký trong `core/shared/shared.module.ts`:

```typescript
providers: [
  { provide: IRateLimiterPort, useClass: RedisRateLimiterAdapter },
  RateLimitGuard,
],
exports: [IRateLimiterPort, RateLimitGuard],
```

### Cập nhật DomainExceptionFilter

Thêm case `BusinessRuleValidationException` với từ khóa `TOO_MANY_REQUESTS` trong message để map lên HTTP 429:

```typescript
if (errorCode === 'TOO_MANY_REQUESTS') {
  status = HttpStatus.TOO_MANY_REQUESTS;
}
```

Hoặc dùng cơ chế kiểm tra message/subclass riêng. Nên tạo một rate-limit-exception riêng mở rộng `DomainException` để mapping chính xác.

### Exception riêng cho Rate Limit

**Đường dẫn:** `backend/src/core/shared/domain/exceptions/rate-limit.exception.ts`

```typescript
export class RateLimitExceededException extends DomainException {
    constructor(retryAfter: number) {
        super(`Quá tải yêu cầu. Vui lòng thử lại sau ${retryAfter} giây.`);
    }
}
```

Thêm mapping trong `DomainExceptionFilter`:
```typescript
} else if (exception instanceof RateLimitExceededException) {
    status = HttpStatus.TOO_MANY_REQUESTS;
    errorCode = 'TOO_MANY_REQUESTS';
}
```

---

Kế hoạch này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
