---
id: "hb-integration-testing-stabilization"
title: "Chuẩn hóa Kiến trúc và Tích hợp Cơ sở dữ liệu thử nghiệm PGLite"
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Loại bỏ triệt để NestJS Framework Leak khỏi Application Layer và chuyển đổi giải pháp in-memory DB từ pg-mem sang PGLite để tương thích hoàn toàn với Drizzle ORM."
tags: [testing, architecture-hardening, pglite, drizzle-orm, domain-exceptions]
---

## 1. Khử Framework Leak & Chuẩn hóa Domain Exception
* **Loại bỏ NestJS HTTP Exceptions:** Loại bỏ hoàn toàn `@nestjs/common` imports tại Application Layer (Service layer). 
* **Ánh xạ Exception thống nhất:**
  * `NotFoundException` $\rightarrow$ `EntityNotFoundException`
  * `BadRequestException` / `ForbiddenException` $\rightarrow$ `BusinessRuleValidationException` hoặc `UnauthorizedException`
* **Áp dụng nhất quán trên các Service:** `AuthService`, `UserService`, `LeadQueryService`, `QuoteService`, `FinoteService` (`[[dom-accounting-finote]]`).

## 2. Di chuyển từ pg-mem sang PGLite
* **Hạn chế của pg-mem:** Lỗi cấu hình `getTypeParser`, không hỗ trợ `rowMode: 'array'` cho Prepared Statements, và lỗi scoping phân tích câu lệnh `LEFT JOIN LATERAL` của Drizzle ORM.
* **Giải pháp PGLite:** Thay thế bằng `@electric-sql/pglite` (Engine Postgres thực thi qua WebAssembly) chạy in-memory cho môi trường Jest.
* **Cấu hình:** Bổ sung `--experimental-vm-modules` vào cấu hình khởi chạy Jest để kích hoạt nạp động WASM của PGLite. Đảm bảo tương thích 100% với Drizzle Repositories (`[[hb-drizzle-base-repo]]`).

## 3. Khắc phục lỗi nghiệp vụ & Đồng bộ Schema
* **State Machine & Value Objects:** Thay thế trạng thái `LeadStage.OPEN` không tồn tại bằng `LeadStage.NEW`. Ràng buộc các tham số bắt buộc (`title`, `deadlineAt`) khi khởi tạo `Finote`.
* **Mocking Rule:** Cấm trả về spread object khi mock `save` của Repository để tránh làm mất các getters của Entity; bắt buộc trả về chính instance.
* **Đồng bộ Test Schema:** Cập nhật helper khởi tạo DB test (`test-db.helper.ts`), bổ sung các trường thiếu cho bảng `contacts` (`userId`, `address`, `jobTitle`, `isPrimary`) khớp với cấu hình production.