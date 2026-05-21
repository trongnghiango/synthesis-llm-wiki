---
id: hb-integration-testing-stabilization
title: "Chuẩn hóa Kiến trúc Dịch vụ và Hạ tầng Integration Test với PGLite"
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Tách biệt Application Layer khỏi HTTP Framework và chuyển đổi công nghệ database testing từ pg-mem sang PGLite hỗ trợ Drizzle ORM."
tags: [testing, pglite, drizzle-orm, architectural-hardening, domain-exceptions]
---

### 1. Thắt chặt Kiến trúc (Architectural Hardening)
- **Framework Agnostic:** Loại bỏ hoàn toàn NestJS exceptions khỏi Application Layer.
  - Thay `NotFoundException` $\rightarrow$ `EntityNotFoundException`.
  - Thay `BadRequestException` / `ForbiddenException` $\rightarrow$ `BusinessRuleValidationException` hoặc `UnauthorizedException`.
  - Toàn bộ exception kế thừa từ `@core/shared/domain/exceptions/base.exceptions`.
- **Unit/Service Test Rules:**
  - Mock Repository qua Interface (Port), tuyệt đối không mock triển khai Drizzle cụ thể.
  - Mock `save` phải trả về chính entity instance (không dùng spread object để tránh mất getters).

### 2. Hạ tầng Integration Test: Chuyển đổi sang `PGLite`
- **Vấn đề của `pg-mem`:**
  1. Không hỗ trợ cấu hình type parser của `pg`.
  2. Không hỗ trợ `rowMode: 'array'` cho Prepared Statements của Drizzle.
  3. Lỗi cú pháp với truy vấn quan hệ phức tạp sinh ra `LEFT JOIN LATERAL` (`db.query.findFirst`).
- **Giải pháp PGLite (`@electric-sql/pglite`):**
  - Chạy engine PostgreSQL biên dịch sang WebAssembly (WASM) in-memory, đảm bảo tương thích 100% SQL chuẩn của Drizzle.
  - Cấu hình Jest chạy với tag `--experimental-vm-modules` để nạp dynamic WASM.
  - Đồng bộ Schema Helper: Cập nhật bảng `contacts` trong `test-db.helper.ts` (thêm `userId`, `address`, `jobTitle`, `isPrimary`) để khớp hoàn toàn với Production.