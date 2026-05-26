---
id: arch-rate-limiting
title: Kiến trúc Rate Limiter (Redis + Clean Architecture)
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
  - "[[hb-drizzle-base-repo]]"
summary: "Thiết kế hệ thống Rate Limiter dạng Port/Adapter tích hợp HTTP Guard và Redis Sliding Window đảm bảo Tenant Isolation tuyệt đối."
tags: [architecture, rate-limiter, redis, multi-tenancy, clean-architecture]
---

# Kiến trúc Rate Limiter (Redis + Clean Architecture)

## 1. Tầm nhìn & Ranh giới (Clean Boundaries)
Hệ thống Rate Limiter được xây dựng theo chuẩn **Port/Adapter** để giữ cho Domain và Application Layer hoàn toàn độc lập với framework NestJS hay công nghệ Redis.

- **Port (`IRateLimiterPort`):** Định nghĩa ở tầng Application Core (`core/shared/application/ports/`). Chỉ chứa pure TypeScript interface.
- **Adapter (`RedisRateLimiterAdapter`):** Định nghĩa ở tầng Infrastructure (`core/shared/infrastructure/adapters/`), phụ thuộc vào framework, thư viện và driver ngoài (Redis/cache-manager).
- **HTTP Presentation Guard (`RateLimitGuard`):** Chặn các request spam sớm tại HTTP layer trước khi NestJS thực hiện parse DTO Validation hay khởi chạy Use Case, bảo vệ hiệu năng CPU và RAM.

## 2. Thuật toán Sorted Set (ZSET) Sliding Window
Sử dụng cấu trúc dữ liệu **Sorted Set (ZSET)** của Redis để hiện thực cửa sổ trượt (Sliding Window) với độ chính xác mili giây, khắc phục lỗi tràn cụm của thuật toán Fixed Window.

### Nguyên lý hoạt động (Redis Multi/Exec):
1. **Dọn dẹp:** Xóa toàn bộ phần tử có timestamp cũ hơn khoảng thời gian hiện tại trừ đi TTL (`zRemRangeByScore`).
2. **Kiểm tra:** Đếm số lượng request hiện tại trong cửa sổ (`zCard`).
3. **Ghi nhận:** Nếu số lượng dưới giới hạn (`limit`), thêm request mới vào set với score là timestamp hiện tại (`zAdd`) và gia hạn thời gian sống cho key (`pExpire`).
4. **Từ chối:** Nếu vượt ngưỡng, ném exception và roll back member vừa thêm.

## 3. Siết chặt Tenant Isolation (ALS Integration)
Để đảm bảo an toàn đa thuê, Rate Limiter tích hợp sâu với **AsyncLocalStorage (ALS)** qua `RequestContextService`:
- Key định danh Redis luôn được phân tách theo `organizationId` lấy từ ALS (chỉ số session JWT an toàn).
- **Combined Strategy (Mặc định):** `rl:org:{organizationId}:user:{userId}:ip:{ip}` cô lập hoàn toàn lưu lượng của từng Tenant/User, triệt tiêu rủi ro Tenant A spam làm ảnh hưởng đến Tenant B.

## 4. Cơ chế Resilient Fallback (Bản lĩnh Hệ thống)
Nếu Redis Cluster bị mất kết nối hoặc sập:
- `RedisRateLimiterAdapter` tự động chuyển sang sử dụng bộ nhớ cục bộ `fallbackMemoryStore` (In-memory Map có cơ chế tự dọn dẹp theo cửa sổ TTL).
- Log cảnh báo `warn` hệ thống nhưng **không crash** và **không chặn** tất cả request một cách oan uổng.

## 5. Liên kết tri thức
- Lọc đa thuê tự động: [[arch-als-tenant-isolation]]
- Quản lý giao dịch: [[arch-als-transactions]]
