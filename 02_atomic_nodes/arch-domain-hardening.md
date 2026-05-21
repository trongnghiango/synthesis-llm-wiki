---
id: arch-domain-hardening
title: Tái cấu trúc và Đóng gói Domain Model Finote
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Đóng gói thuộc tính nhạy cảm của Finote, chuyển dịch logic nghiệp vụ vào thực thể và loại bỏ cấu hình cứng."
tags: [clean-architecture, domain-driven-design, finote, encapsulation, refactoring]
---

### 1. Đóng gói Domain & State Mutation (`Finote` Entity)
- **Encapsulation**: Ẩn thuộc tính `status` và `reviewerId` phía sau các trường private `_status` và `_reviewerId` kèm getters tương ứng.
- **Nghiệp vụ tại Entity**: Chuyển trực tiếp logic kiểm soát trạng thái vào thực thể qua 2 phương thức:
  - `approve(reviewerId)`: Chỉ cho phép duyệt nếu trạng thái hiện tại là `PENDING`.
  - `reject(reviewerId, reason)`: Chỉ cho phép từ chối nếu trạng thái hiện tại là `PENDING`.
- **Refactor Service**: `FinoteService` tuyệt đối không thay đổi trực tiếp trạng thái mà phải ủy quyền thông qua hành vi của Domain Model.

### 2. Tối ưu hóa Mapper & Bảo mật Credential
- **EmployeeMapper**: Loại bỏ các kiểm tra ternary dư thừa (`raw.userId ? Number(raw.userId) : ...`), chuẩn hóa về cơ chế gán thuộc tính trực tiếp gọn nhẹ.
- **Secret Management**: Trích xuất toàn bộ mật khẩu mặc định ghi cứng (`Company@2026`, `Stax@123`, `K@2026`) tại `company-import.service.ts`, `stax-legacy-migration.service.ts`, và `database.seeder.ts` ra biến môi trường `process.env.SEED_DEFAULT_PASSWORD`.

### 3. Sửa lỗi Adapter & Logic Đặc thù
- **BootstrapService**: Điều chỉnh cơ chế mock duyệt tài khoản chỉ giới hạn cho `superadmin` nhằm khớp với giao diện Frontend mà không làm ảnh hưởng đến tính toàn vẹn của Domain.
- **Kafka Event Bus**: Khắc phục lỗi hiển thị log của Adapter, chuyển tiền tố log từ `[RabbitMQ]` thành `[Kafka]` chính xác.