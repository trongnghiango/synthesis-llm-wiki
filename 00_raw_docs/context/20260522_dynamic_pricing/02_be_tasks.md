# 02 Backend Tasks Checklist: Bieu phi dong & Doanh thu bac thang CRM - Billing

Checklist chi tiết cho quá trình thực thi code Backend để đảm bảo tuân thủ đầy đủ tiêu chuẩn Clean Architecture của STAX.

- [ ] 1. Shared Contracts: Cập nhật Zod schema `closeWonSchema` và `ContractItem` tại [crm.ts](backend/src/core/shared/contracts/crm.ts).
- [ ] 2. pgEnum definitions: Định nghĩa `pricingModelEnum` mới tại [services.schema.ts](backend/src/database/schema/crm/services.schema.ts).
- [ ] 3. Database Schema: Thêm cột `pricingModel` và `pricingConfig` tại [services.schema.ts](backend/src/database/schema/crm/services.schema.ts) và [contract-items.schema.ts](backend/src/database/schema/crm/contract-items.schema.ts). Đổi `basePrice`, `unitPrice`, `amount` thành nullable/default 0.
- [ ] 4. Run migration: Chạy lệnh generate migration của drizzle-kit.
- [ ] 5. Domain Entity + Props interface: Mở rộng `ServiceProps`, `Service` tại [service.entity.ts](backend/src/modules/crm/domain/entities/service.entity.ts) và `ContractItem` tại [contract.entity.ts](backend/src/modules/crm/domain/entities/contract.entity.ts).
- [ ] 6. Mapper: Ánh xạ thêm các trường giá động tại [service.mapper.ts](backend/src/modules/crm/infrastructure/mappers/service.mapper.ts) và [contract.mapper.ts](backend/src/modules/crm/infrastructure/mappers/contract.mapper.ts).
- [ ] 7. Request DTO: Cập nhật các trường validator mới tại [close-lead.request.dto.ts](backend/src/modules/crm/infrastructure/dtos/close-lead.request.dto.ts).
- [ ] 8. Application Service: Cập nhật logic `closeLeadAsWon` và logic sinh Finote cọc ban đầu tại [lead-workflow.service.ts](backend/src/modules/crm/application/services/lead-workflow.service.ts).
- [ ] 9. Controller: Đảm bảo route nhận đúng DTO tại [lead.controller.ts](backend/src/modules/crm/infrastructure/controllers/lead.controller.ts).
- [ ] 10. Module Wiring: Xác nhận module load đúng các schema và provider tại [crm.module.ts](backend/src/modules/crm/crm.module.ts).
- [ ] 11. Unit Test: Viết và chạy unit test cho logic chốt Won Lead giá động tại [lead-workflow.service.spec.ts](backend/src/modules/crm/application/services/lead-workflow.service.spec.ts).
- [ ] 12. Build check: Chạy lệnh `npm run build` ở backend để đảm bảo 0 lỗi biên dịch TypeScript.
