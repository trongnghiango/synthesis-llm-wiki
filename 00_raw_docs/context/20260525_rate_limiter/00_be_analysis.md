# Phân tích Nghiệp vụ & Kiến trúc: Tích hợp Rate Limiter vào STAX

## 1. Phân loại Module (Architectural Tier)
- **Tầng:** `Tier 1 — Foundation`
  - Đây là module nền tảng, hoàn toàn không chứa logic nghiệp vụ đặc thù (CRM/HRM/Accounting). Nó đóng vai trò là một cross-cutting concern của toàn bộ hệ thống giúp bảo vệ hạ tầng API.
- **Quan hệ phụ thuộc:**
  - `RateLimiter` được đăng ký và sử dụng toàn cục ở tầng HTTP Presentation. Nó được tích hợp vào `core/shared/` và không trực tiếp phụ thuộc vào các domain nghiệp vụ Tier 2 & Tier 3.
  - Các module nghiệp vụ (Tier 2 & 3) có thể tự do sử dụng Decorator `@RateLimit()` để cấu hình rate limit cho các API của mình.

## 2. Bounded Context & Ubiquitous Language
- **Domain Context:** Rate Limiter.
- **Thuật ngữ đồng bộ:**
  - *Rate Limit Request* (`RateLimitRequest`): Dữ liệu gửi đến bộ kiểm tra giới hạn (gồm Key, Limit, TTL).
  - *Rate Limit Result* (`RateLimitResult`): Kết quả phán quyết (Cho phép/Chặn, số request còn lại, thời điểm reset).
  - *Rate Limit Guard* (`RateLimiterGuard`): NestJS HTTP Guard đón chặn request sớm để kiểm tra.
  - *Rate Limit Decorator* (`@RateLimit()`): Custom Decorator khai báo cấu hình chặn ở Controller.
  - *Sliding Window Algorithm*: Thuật toán cửa sổ trượt sử dụng Redis Sorted Set (ZSET) đảm bảo độ chính xác tuyệt đối.

## 3. Data Flow & API Design
### Luồng xử lý request HTTP:
```
Client Request ──> NestJS Controller ──> Guard (RateLimiterGuard)
                                              │
                                              ├──> Đọc ALS (lấy tenant/user)
                                              ├──> Gọi IRateLimiterPort
                                              ├──> Redis Adapter (ZSET Multi/Exec)
                                              │
                    [Nếu Bị Chặn] <───────────┤ (BusinessRuleValidationException)
                                              │
                    [Nếu Cho Phép] <──────────┘
                               │
                       DTO Validation
                               │
                       Use Case Service
```

- **Metadata Configuration Zod Schema:** Định nghĩa schema cấu hình để validate options truyền vào Decorator.

## 4. Cross-module dependencies & Domain Events
- **Cross-module:**
  - Không có quan hệ coupling trực tiếp.
  - Phụ thuộc gián tiếp vào `AsyncLocalStorage` (ALS) để lấy context đa thuê (`organizationId`, `userId`).
- **Domain Events:**
  - Không phát Domain Event chuẩn nghiệp vụ, nhưng có thể log cảnh báo bảo mật khi phát hiện hành vi spam vượt hạn mức quá nhiều lần (tương lai sẽ log thông qua `IAuditLogService`).

## 5. Multi-tenancy (Tenant Isolation)
- **Bảo mật đa thuê:** Đây là điều kiện tiên quyết của STAX. 
- Ngăn ngừa tình trạng: Tenant A thực hiện brute-force hoặc spam API làm cạn kiệt tài nguyên của hệ thống chung, gián tiếp ảnh hưởng đến Tenant B.
- **Giải pháp:** Cấu trúc Key lưu vào Redis sẽ bắt buộc chứa `organizationId` được trích xuất an toàn từ AsyncLocalStorage (ALS), lấy từ session JWT/Session đã xác thực. Không tin tưởng `orgId` từ URL/Query string.
  - Đối với các API công khai chưa đăng nhập (như Login, Lead Intake): Sử dụng `PUBLIC` hoặc `ANONYMOUS` kết hợp với `clientIp` làm Key để cách ly.

## 6. Security & Exception Compliance
- Khi request vượt ngưỡng, Guard bắt buộc ném `BusinessRuleValidationException` định nghĩa trong `@core/shared/domain/exceptions/business-rule-validation.exception.ts` (không ném các framework exception của NestJS như `HttpException` trực tiếp ở tầng lõi).
- Tầng HTTP Filter chung sẽ tự động bắt exception này và map thành mã HTTP `429 Too Many Requests` trả về cho Client.

---
Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết.
