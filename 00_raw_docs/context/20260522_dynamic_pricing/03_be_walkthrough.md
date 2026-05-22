# Refactoring Backend STAX Dynamic Pricing Architecture - Walkthrough

Chúng ta đã hoàn thành việc triển khai tầng Backend cho kiến trúc biểu phí động linh hoạt trong quy trình Lead-to-Contract (Close WON) của STAX.

## 1. Thay đổi đã thực hiện

### A. Shared Contracts
- **[crm.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/core/shared/contracts/crm.ts)**:
  - Cập nhật `closeWonSchema` để hỗ trợ các thuộc tính biểu phí động: `pricingModel` (enum) và `pricingConfig` (JSONB).
  - Cho phép `feeAmount` mang giá trị trống/optional đối với các trường hợp không có đơn giá cố định.
  - Cập nhật `ContractItem` và `createContractSchema` để đồng bộ thuộc tính.

### B. Database Schema & Migrations
- **[services.schema.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/database/schema/crm/services.schema.ts)**:
  - Thêm `pricingModelEnum` (`FIXED`, `MANUAL_AGREEMENT`, `TIERED_REVENUE`).
  - Cập nhật bảng `services`: thêm cột `pricingModel` và `pricingConfig` (JSONB), đồng thời đặt `basePrice` thành nullable.
- **[contract-items.schema.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/database/schema/crm/contract-items.schema.ts)**:
  - Thêm `pricingModel` và `pricingConfig` (JSONB) vào bảng `contract_items`.
  - Chuyển `unitPrice` và `amount` thành nullable.
- **Migration**: Tạo thành công file migration `database/migrations/0010_adorable_magneto.sql`.

### C. Domain & Infrastructure Mappers
- **Domain Entities ([service.entity.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/domain/entities/service.entity.ts), [contract.entity.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/domain/entities/contract.entity.ts))**:
  - Hỗ trợ các thuộc tính giá động, đảm bảo tương thích ngược và cho phép giá trị null an toàn.
- **Mappers ([service.mapper.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/infrastructure/mappers/service.mapper.ts), [contract.mapper.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/infrastructure/mappers/contract.mapper.ts))**:
  - Ánh xạ chính xác các thuộc tính giá động giữa thực thể Domain và Database.
- **Repository ([drizzle-contract.repository.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/infrastructure/persistence/drizzle-contract.repository.ts))**:
  - Lưu cấu hình giá động khi lưu hợp đồng mới.

### D. DTO, Service & Controller
- **DTOs ([close-lead.request.dto.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/infrastructure/dtos/close-lead.request.dto.ts), [close-lead.dto.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/application/dtos/close-lead.dto.ts))**:
  - Hỗ trợ validator NestJS cho `pricingModel`, `pricingConfig` và các trường cọc/Finote (`createFinote`, `finoteAmount`, `finoteDate`, `finoteDescription`).
- **LeadWorkflowService ([lead-workflow.service.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/application/services/lead-workflow.service.ts))**:
  - Cập nhật logic `closeLeadAsWon` để kế thừa `pricingModel` và `pricingConfig` khi sinh hợp đồng trực tiếp hoặc kế thừa từ báo giá.
  - Đóng gói dữ liệu cọc ban đầu vào `ContractCreatedEvent`.
- **Event Listener ([contract-created.listener.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/listeners/contract-created.listener.ts))**:
  - Lắng nghe `ContractCreatedEvent` từ module CRM.
  - Nếu `createFinote: true`, gọi `FinoteService.createFinote` để tự động tạo phiếu thu cọc ban đầu trong phân hệ Kế toán.

---

## 2. Kết quả Kiểm thử & Build

### A. Unit Tests
Cả hai suite kiểm thử chính đều chạy thành công 100%:
- **LeadWorkflowService unit tests**:
  `backend/src/modules/crm/application/services/lead-workflow.service.spec.ts` -> **PASS**
- **ContractCreatedListener unit tests**:
  `backend/src/modules/accounting/application/listeners/contract-created.listener.spec.ts` -> **PASS**

### B. Build Verification
- Build thành công toàn bộ hệ thống backend:
  `npm run build` -> **Compiled successfully**
