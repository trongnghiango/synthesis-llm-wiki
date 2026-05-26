# Context Handoff — Thiết kế Rate Limiter

## Handoff Summary
- **Skill vừa hoàn thành:** `stax-think` (Thiết kế kiến trúc)
- **Skill tiếp theo:** `stax-backend` (Phát triển backend nghiệp vụ)

## Decisions đã lock (KHÔNG được reopen)
- **[D1] Kiến trúc:** Sử dụng **Port/Adapter Pattern** kết hợp **Controller HTTP Guard** (Approach A).
  - Domain và Application hoàn toàn độc lập, không bị ảnh hưởng bởi framework/decorator.
  - Chặn request sớm tại HTTP layer trước khi chạy Use Case/DTO Validation.
- **[D2] Storage Adapter:** Lưu trữ phân tán sử dụng **Redis Sorted Set (ZSET) với thuật toán Sliding Window**.
  - Đảm bảo phân tán (distributed), hỗ trợ scale out nhiều server.
  - Tốc độ đọc ghi <2ms, dọn dẹp các request hết hạn theo thời gian thực.
- **[D3] Strategy Mặc định:** `COMBINED` (Phối hợp `organizationId` từ ALS + `userId` + `clientIp`).
  - Đảm bảo an toàn **Tenant Isolation**, không để hành vi spam của Tenant A ảnh hưởng đến tài nguyên của Tenant B.

## Assumptions đã document
- **[A1]:** Tốc độ Redis cluster hoạt động ổn định và có sẵn kết nối client thông qua `cache-manager`.
- **[A2]:** AsyncLocalStorage (ALS) đã được setup và inject đầy đủ ở tầng global để luôn có `organizationId` và `userId` trong context.

## Open questions (skill tiếp theo phải giải quyết)
- **[Q1]:** Cơ chế fallback khi Redis tạm thời mất kết nối (có nên chuyển tạm thời sang In-memory rate limiting không hay trả về bypass/cho phép qua)?
- **[Q2]:** Các Endpoint nào cần được áp dụng Decorator `@RateLimit()` ngay trong đợt đầu (gợi ý: CRM Lead Intake, Auth Login, Reset Password)?

## Files đã tạo
- Không có file production nào được tạo trong session này (tuân thủ nguyên tắc `@stax-think` chỉ thiết kế).
- Đã cập nhật file task dự án: `docs/tasks_phase1_stax_v2 - tasks_phase1_stax_v2.csv` (Thêm task Rate Limiter vào Sprint 06).
