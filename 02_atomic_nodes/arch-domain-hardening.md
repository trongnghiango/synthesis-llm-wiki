---
id: arch-domain-hardening
title: Tăng cường đóng gói Domain và Chuẩn hóa Kiến trúc
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Tái cấu trúc thực thể Finote để bảo vệ bất biến domain, chuẩn hóa Mapper và loại bỏ thông tin nhạy cảm."
tags: [domain-driven-design, clean-architecture, finote, refactor]
---

### 1. Đóng gói Domain Thực thể `[[dom-accounting-finote]]`
Bảo vệ bất biến domain (domain invariants) và ngăn chặn sửa đổi trạng thái tùy tiện từ Service layer:
- **Trường ẩn (Private fields):** Chuyển `status` và `reviewerId` thành `_status` và `_reviewerId` kèm getters tương ứng.
- **Nghiệp vụ chuyển đổi trạng thái tích hợp:**
  ```typescript
  class Finote {
    private _status: FinoteStatus;
    private _reviewerId?: string;

    public approve(reviewerId: string): void {
      if (this._status !== FinoteStatus.PENDING) throw new DomainError("Only PENDING finotes can be approved");
      this._status = FinoteStatus.APPROVED;
      this._reviewerId = reviewerId;
    }

    public reject(reviewerId: string, reason: string): void {
      if (this._status !== FinoteStatus.PENDING) throw new DomainError("Only PENDING finotes can be rejected");
      this._status = FinoteStatus.REJECTED;
      this._reviewerId = reviewerId;
    }
  }
  ```
- **Tác động:** `FinoteService` chuyển đổi hoàn toàn từ việc gán thuộc tính trực tiếp sang gọi phương thức nghiệp vụ tuần tự trên Entity.

### 2. Tối ưu hóa Mapper & Cấu hình Hệ thống
- **`EmployeeMapper`:** Loại bỏ logic gán thuộc tính lồng nhau phức tạp, đơn giản hóa cấu trúc mapping trực tiếp.
- **Bảo mật cấu hình:** Loại bỏ hoàn toàn plaintext password mặc định trong code nguồn (`company-import.service.ts`, `database.seeder.ts`). Thay thế bằng biến môi trường `process.env.SEED_DEFAULT_PASSWORD`.
- **Chuẩn hóa Logging:** Chuyển đổi nhãn log hệ thống tại Kafka Event Bus adapter từ `[RabbitMQ]` sang đúng định dạng `[Kafka]`.