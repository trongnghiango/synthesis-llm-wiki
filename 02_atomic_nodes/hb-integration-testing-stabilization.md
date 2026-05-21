---
id: hb-integration-testing-stabilization
title: Tối ưu và Ổn định hóa Integration Test với PGLite
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[arch-als-tenant-isolation]]"
summary: "Thắt chặt Application Layer (loại bỏ Framework Leak) và chuyển đổi test database engine từ pg-mem sang PGLite để tương thích hoàn toàn với Drizzle ORM."
tags: [testing, pglite, drizzle, exceptions, architecture]
---

## 1. Thắt chặt Kiến trúc & Loại bỏ Framework Leak
- **Nguyên tắc**: Cô lập hoàn toàn Application Layer khỏi NestJS (Framework Agnostic).
- **Refactor Exception**: Thay thế NestJS Exceptions bằng Domain Exceptions (`@core/shared/domain/exceptions/base.exceptions`):
  - `NotFoundException` $\rightarrow$ `EntityNotFoundException`
  - `BadRequestException` / `ForbiddenException` $\rightarrow$ `BusinessRuleValidationException` hoặc `UnauthorizedException`
- **Mocking**: Tất cả mock phải tuân theo Repository Interface (Port), tuyệt đối không mock trực tiếp triển khai Drizzle cụ thể.

## 2. Di cư Test Engine: `pg-mem` $\rightarrow$ `PGLite`
- **Vấn đề của `pg-mem`**: Lỗi `getTypeParser`, thiếu hỗ trợ `rowMode: 'array'` cho Prepared Statements, và không phân tích được `LEFT JOIN LATERAL` sinh ra từ Drizzle relation queries.
- **Giải pháp**: Thay thế bằng `@electric-sql/pglite` (Chạy Postgres thực thụ qua WebAssembly).
  - *Ưu điểm*: Tương thích 100% với Drizzle ORM, loại bỏ hoàn toàn Monkey Patch.
  - *Cấu hình*: Khởi chạy Jest với flag `--experimental-vm-modules` để hỗ trợ WASM dynamic import.

## 3. Các Điểm hiệu chỉnh Domain & Schema quan trọng
- **Domain Align**: Đổi `LeadStage.OPEN` $\rightarrow$ `LeadStage.NEW`. Mock `save` phải trả về chính entity instance thay vì spread object nhằm bảo toàn getters.
- **Schema Align**: Cập nhật schema `contacts` trong `test-db.helper.ts` (thêm `userId`, `address`, `jobTitle`, `isPrimary`).
- **Finote**: Khởi tạo Finote bắt buộc cung cấp `title`, `deadlineAt` và sử dụng Money Value Object (VO).