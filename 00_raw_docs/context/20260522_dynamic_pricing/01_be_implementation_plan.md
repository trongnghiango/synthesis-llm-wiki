# 01 Backend Implementation Plan: Bieu phi dong & Doanh thu bac thang CRM - Billing

Kế hoạch chi tiết để tích hợp luồng biểu phí động từ Database Schema, Domain, Application Service đến API Presenter.

## A. Database Schema
Chúng ta sẽ bổ sung các cột mới vào các bảng Drizzle ORM có sẵn:

1.  **Bảng Services [services.schema.ts](backend/src/database/schema/crm/services.schema.ts)**:
    - Bổ sung `pricingModelEnum` kiểu `pgEnum('pricing_model', ['FIXED', 'MANUAL_AGREEMENT', 'TIERED_REVENUE'])`.
    - Thêm cột `pricingModel` sử dụng enum trên, mặc định là `'FIXED'`.
    - Thêm cột `pricingConfig` dạng `jsonb` để cấu hình biểu phí bậc thang hoặc thông tin động.
    - Cập nhật cột `basePrice` thành nullable.

2.  **Bảng Contract Items [contract-items.schema.ts](backend/src/database/schema/crm/contract-items.schema.ts)**:
    - Thêm cột `pricingModel` sử dụng `pricingModelEnum`.
    - Thêm cột `pricingConfig` dạng `jsonb`.
    - Cho phép cột `unitPrice` và `amount` là nullable hoặc có giá trị mặc định là 0.

3.  **Migration Strategy**:
    - Chạy lệnh `npx drizzle-kit generate` để sinh file migration.
    - Sử dụng migration script tự động hoặc migration chạy lúc khởi động ứng dụng để cập nhật PostgreSQL.

---

## B. Domain Layer

1.  **Service Entity [service.entity.ts](backend/src/modules/crm/domain/entities/service.entity.ts)**:
    - Mở rộng `ServiceProps` và thực thể `Service` để hỗ trợ `pricingModel` và `pricingConfig`.
    - Cập nhật hàm khởi tạo và cho phép `basePrice` nhận giá trị null/optional.

2.  **Contract Entity [contract.entity.ts](backend/src/modules/crm/domain/entities/contract.entity.ts)**:
    - Cập nhật interface `ContractItem` để thêm `pricingModel` (string/enum) và `pricingConfig` (any/record).

---

## C. Infrastructure Layer

1.  **Service Mapper [service.mapper.ts](backend/src/modules/crm/infrastructure/mappers/service.mapper.ts)**:
    - Cập nhật `toDomain()`, `toPersistence()`, `toResponse()` để ánh xạ đúng hai trường `pricingModel` và `pricingConfig`.

2.  **Contract Mapper [contract.mapper.ts](backend/src/modules/crm/infrastructure/mappers/contract.mapper.ts)**:
    - Đọc thêm cột `pricingModel` và `pricingConfig` từ thực thể persistence `contract_items` và ánh xạ vào danh sách `items` của thực thể Domain `Contract`.

---

## D. Application Layer

1.  **Lead Workflow Service [lead-workflow.service.ts](backend/src/modules/crm/application/services/lead-workflow.service.ts)**:
    - Chỉnh sửa hàm `closeLeadAsWon()` để tiếp nhận `pricingModel` và `pricingConfig` từ DTO.
    - Khi tạo Hợp đồng mới và các Hạng mục hợp đồng, hệ thống sẽ gán trực tiếp mô hình tính giá và biểu phí đã đàm phán vào từng Hạng mục hợp đồng.
    - Cập nhật logic sinh Finote ban đầu: Nếu hợp đồng là giá động và có bật `createFinote`, số tiền ghi nhận sẽ là tiền cọc (`finoteAmount`) thay vì mặc định lấy từ `feeAmount` (vì lúc này giá trị hợp đồng cố định bằng 0).

---

## E. Presentation Layer & Contracts

1.  **Zod Schema [crm.ts](backend/src/core/shared/contracts/crm.ts)**:
    - Cập nhật `closeWonSchema` của Zod để chấp nhận `pricingModel` và `pricingConfig` (Validate an object/array cấu hình bậc thang).
    - Đổi `feeAmount` thành optional.

2.  **Request DTO [close-lead.request.dto.ts](backend/src/modules/crm/infrastructure/dtos/close-lead.request.dto.ts)**:
    - Thêm các trường validator của NestJS (`class-validator` và Swagger annotations) cho `pricingModel` và `pricingConfig`.
    - Chuyển `feeAmount` từ `@IsNotEmpty()` thành `@IsOptional()`.

---

## F. Module Wiring
- Đảm bảo các Schema enum được export đầy đủ và đồng bộ. Không cần thay đổi đăng ký DI token do không tạo Class repository mới.
