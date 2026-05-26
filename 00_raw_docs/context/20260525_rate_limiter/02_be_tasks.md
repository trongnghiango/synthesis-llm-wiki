# Checklist Thực thi: Tích hợp Rate Limiter

Mọi bước dưới đây tuân thủ triệt để cấu trúc **Clean Architecture + DDD** và ranh giới bất khả xâm phạm.

## 📋 Checklist

```
[ ] 1.  Cập nhật Shared Contract Zod Schema (common.ts) ở cả frontend/shared/contracts/ và backend/src/core/shared/contracts/
[ ] 2.  Bổ sung RateLimitExceededException vào core/shared/domain/exceptions/base.exceptions.ts
[ ] 3.  Đăng ký mapping exception HTTP 429 TOO_MANY_REQUESTS trong DomainExceptionFilter
[ ] 4.  Tạo Port interface IRateLimiterPort tại core/shared/application/ports/rate-limiter.port.ts
[ ] 5.  Tạo RedisRateLimiterAdapter tại core/shared/infrastructure/adapters/redis-rate-limiter.adapter.ts (sử dụng Sliding Window)
[ ] 6.  Tạo RateLimitGuard tại core/shared/infrastructure/guards/rate-limiter.guard.ts (tự động nhận dạng organizationId qua ALS)
[ ] 7.  Tạo Decorator @RateLimit tại core/decorators/rate-limit.decorator.ts
[ ] 8.  Đăng ký Adapter và Guard trong core/shared/shared.module.ts
[ ] 9.  Tạo Unit/Integration Test cho RedisRateLimiterAdapter và Guard
[ ] 10. Chạy build kiểm tra: npm run build — 0 error
[ ] 11. Chạy test toàn hệ thống để đảm bảo không có regressions
```

---
Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
