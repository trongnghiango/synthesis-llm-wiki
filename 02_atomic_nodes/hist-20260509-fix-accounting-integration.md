---
id: hist-20260509-fix-accounting-integration
title: Sửa lỗi tích hợp luồng Phiếu Thu Chi (Finote)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
  - "[[arch-tenant-isolation]]"
summary: "Chuẩn hóa luồng tạo Finote: Đồng bộ Employee ID, tự động gán Organization ID và hỗ trợ tương thích ngược DTO."
tags: [accounting, finote, tenant-isolation, resolution, backwards-compatibility]
---

### 1. Cơ chế Đồng bộ & Bảo mật (Resolution & Isolation)
* **Tra cứu Employee ID**: `FinoteService` tự động phân giải `userId` từ session sang `employeeId` tương ứng. Chặn xử lý (ném ngoại lệ chặn) nếu tài khoản chưa được thiết lập hồ sơ nhân sự.
* **Cô lập Tenant**: Tự động inject `organizationId` lấy trực tiếp từ `UserSession` vào payload của `Finote` trước khi persist, loại bỏ lỗi mồ côi (null company). Chi tiết cơ chế tại `[[arch-tenant-isolation]]`.

### 2. Tương thích ngược DTO (Backward Compatibility)
Sử dụng class-transformer (`@Transform`) tại `CreateFinoteDto` để tự động ánh xạ dữ liệu cũ từ Frontend sang cấu trúc Schema mới:
* `transactionDate` $\rightarrow$ `deadlineAt`
* `RECEIPT` $\rightarrow$ `INCOME` (Loại giao dịch)

### 3. Cấu trúc Tệp tin Thay đổi
* `src/modules/accounting/domain/entities/finote.entity.ts`: Bổ sung luật validation miền giá trị.
* `src/modules/accounting/application/services/finote.service.ts`: Xử lý phân giải `employeeId` và áp đặt `organizationId`.
* `src/modules/accounting/application/dtos/create-finote.dto.ts`: Khai báo alias transformer cho API tương thích ngược.
* `src/modules/accounting/infrastructure/controllers/finote.controller.ts`: Refactor API controller để tiếp nhận payload chuẩn hóa.

### 4. Xác minh Kiểm thử (Verification)
* **Unit Test (`finote.service.spec.ts`)**: Đạt 100% coverage với các kịch bản: Hợp lệ, Thiếu Employee, và Thiếu Org.
* **Integration Test (`finote.repository.spec.ts`)**: Thực thi thành công trên môi trường PGLite, đảm bảo tính toàn vẹn của các ràng buộc khóa ngoại (Foreign Key constraints).