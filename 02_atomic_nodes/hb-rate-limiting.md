---
id: hb-rate-limiting
title: Hướng dẫn triển khai @RateLimit Decorator
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[arch-rate-limiting]]"
summary: "Hướng dẫn cấu hình và sử dụng Decorator `@RateLimit()` trên backend NestJS STAX với các Strategy (IP, USER, TENANT, COMBINED)."
tags: [handbook, rate-limiter, api, decorator, security, redis]
---

# Hướng dẫn triển khai @RateLimit Decorator

## 1. Khai báo Decorator trên Controller (Cách dùng)
Không cần cấu hình thêm. Dev chỉ việc thêm decorator lên handler và chỉ định cấu hình:

```typescript
@Controller('leads')
export class LeadController {

  @Post()
  @RateLimit({ limit: 5, ttl: 60, strategy: 'TENANT' })
  // ^ Cho phép tối đa 5 request/phút cho mỗi Tenant (organizationId từ ALS)
  async createLead(@Body() dto: CreateLeadDto) { ... }

  @Get()
  @RateLimit({ limit: 30, ttl: 60, strategy: 'USER' })
  // ^ 30 request/phút cho mỗi User
  async findAll() { ... }
}
```

## 2. Các tham số cấu hình

| Parameter | Type | Default | Mô tả |
|-----------|------|---------|-------|
| `limit` | `number` | `60` | Số request tối đa cho phép trong khoảng thời gian `ttl` |
| `ttl` | `number` (giây) | `60` | Cửa sổ thời gian trước khi reset |
| `strategy` | `enum` | `COMBINED` | Cách tạo key định danh: `IP` (theo client ip), `USER` (theo userId), `TENANT` (theo orgId), `COMBINED` (orgId + userId + ip) |

## 3. Cơ chế hoạt động
Khi một request đến:
1. `RateLimitGuard` đọc metadata `RATE_LIMIT_KEY` từ `@RateLimit()` decorator thông qua `Reflector`.
2. Guard lấy context ALS (chứa `organizationId`, `userId`) của request hiện tại.
3. Dựa trên `strategy` được cấu hình, guard tạo một `key` Redis duy nhất.
4. `RedisRateLimiterAdapter` sử dụng Redis sorted set (ZSET) với **Sliding Window** để kiểm tra giới hạn.
5. Nếu bị chặn: ném `RateLimitExceededException` → Filter map → HTTP 429 `TOO_MANY_REQUESTS`.
6. Nếu hợp lệ: tiếp tục luồng xử lý bình thường.

## 4. Response Headers
Mỗi request đi qua `@RateLimit()` đều có header dạng:
- `X-RateLimit-Limit: 10`
- `X-RateLimit-Remaining: 3`
- `X-RateLimit-Reset: 1779728373`
- `Retry-After: 60`

## 5. Vị trí các files (dành cho AI Agent / Developer đọc code)

| File | Vai trò |
|------|---------|
| `backend/src/core/decorators/rate-limit.decorator.ts` | Định nghĩa Decorator `@RateLimit` |
| `backend/src/core/shared/infrastructure/guards/rate-limiter.guard.ts` | Guard chặn request spam, gọi Port |
| `backend/src/core/shared/infrastructure/adapters/redis-rate-limiter.adapter.ts` | Redis Adapter dùng Sliding Window (ZSET) |
| `backend/src/core/shared/application/ports/rate-limiter.port.ts` | Port interface `IRateLimiterPort` |
| `backend/src/core/shared/contracts/common.ts` | Zod schema `RateLimitOptionSchema` |

## 6. Liên kết
- Kiến trúc tổng thể: [[arch-rate-limiting]]
