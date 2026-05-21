---
id: dom-domain-hardening
title: Đóng gói Domain Finote và Chuẩn hóa Kiến trúc
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Đóng gói trạng thái thực thể Finote, loại bỏ magic strings và sửa lỗi vi phạm Clean Architecture."
tags: [domain-driven-design, encapsulation, refactoring, security, clean-architecture]
---

### 1. Đóng gói Thực thể `Finote` (`[[dom-accounting-finote]]`)
- **Ẩn thuộc tính nhạy cảm:** Chuyển `status` và `reviewerId` thành private fields (`_status`, `_reviewerId`) và chỉ truy cập qua getters.
- **Kiểm soát đột biến trạng thái (State Mutation):** Tích hợp logic nghiệp vụ chuyển đổi trạng thái trực tiếp vào thực thể `Finote` qua các phương thức:
  - `approve(reviewerId: string): void`
  - `reject(reviewerId: string, reason: string): void`
  - *Ràng buộc:* Chỉ cho phép chuyển đổi từ trạng thái `PENDING`, ném ngoại lệ nếu vi phạm.
- **Tách biệt tầng Service:** Cập nhật `FinoteService` để ủy quyền thay đổi trạng thái thông qua thực thể thay vì gán trực tiếp.

### 2. Tối ưu hóa Mapping (`EmployeeMapper`)
- Loại bỏ kiểm tra điều kiện lồng nhau dư thừa (ví dụ: `raw.userId ? Number(raw.userId) : ...`).
- Chuẩn hóa sang cơ chế ánh xạ thuộc tính trực tiếp.

### 3. Loại bỏ Magic Strings & Bảo mật Hóa
- Loại bỏ mật khẩu mặc định dạng plain-text (`'Company@2026'`, `'Stax@123'`) khỏi:
  - `company-import.service.ts`
  - `stax-legacy-migration.service.ts`
  - `database.seeder.ts`
- Chuyển sang cấu hình động qua biến môi trường: `process.env.SEED_DEFAULT_PASSWORD`.

### 4. Khắc phục Logic Cứng & Lỗi Adapter
- Cập nhật cơ chế mock tại `BootstrapService` để đồng bộ quyền duyệt với vai trò `superadmin` của giao diện Frontend.
- Sửa lỗi định dạng logger tại Kafka Event Bus adapter: Chuyển đổi nhãn tiền tố từ `[RabbitMQ]` thành `[Kafka]`.