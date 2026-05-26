---
id: dom-dynamic_pricing
title: Kiến trúc Biểu phí Động STAX
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Cấu trúc biểu phí động (pricingModel, pricingConfig) trong luồng Lead-to-Contract và liên kết tự động tạo Finote đặt cọc."
tags: [crm, dynamic-pricing, db-schema, lead-to-contract]
---

### 1. Thay đổi DB Schema (Drizzle)
- **Cột mới**: `pricingModel` (Enum: `FIXED`, `MANUAL_AGREEMENT`, `TIERED_REVENUE`), `pricingConfig` (JSONB - hoàn toàn nullable).
- **Nguyên tắc nghiệp vụ thép**: `pricingConfig` và các cột số tiền (`unitPrice`, `amount`) **bắt buộc phải nullable** ở Database, Domain Entity và Zod/DTO Validation. Điều này cho phép Kế toán xử lý các hợp đồng không phải one-off (như thu phí dịch vụ hàng tháng theo doanh thu thực tế bậc thang `TIERED_REVENUE` hoặc thỏa thuận riêng `MANUAL_AGREEMENT`), nơi công thức và doanh thu chỉ xác định được khi phát sinh nghiệp vụ thực tế.
- **File ảnh hưởng**:
  - `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/database/schema/crm/services.schema.ts` (đặt `basePrice` sang nullable).
  - `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/database/schema/crm/contract-items.schema.ts` (đặt `unitPrice`, `amount` sang nullable).
- **Migration**: `0010_adorable_magneto.sql`.

### 2. API Contract & Validation (Zod/NestJS)
- **Contract**: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/core/shared/contracts/crm.ts`
  - `closeWonSchema` & `createContractSchema` tích hợp `pricingModel`, `pricingConfig` (JSONB), và `feeAmount` (optional).
- **DTO**: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/infrastructure/dtos/close-lead.request.dto.ts` validator cho pricing & Finote (`createFinote`, `finoteAmount`, `finoteDate`, `finoteDescription`).

### 3. Luồng Nghiệp vụ & Tích hợp Liên Domain
- **Domain Entities & Mappers**: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/infrastructure/mappers/service.mapper.ts`, `contract.mapper.ts` (ánh xạ dữ liệu dynamic pricing tương thích ngược).
- **Workflow**: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/crm/application/services/lead-workflow.service.ts` kế thừa cấu hình biểu phí động khi close WON, phát `ContractCreatedEvent` kèm data cọc.
- **Tích hợp Kế toán (`[[dom-accounting-finote]]`)**:
  - `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/listeners/contract-created.listener.ts` bắt event, nếu `createFinote: true` tự động gọi `FinoteService.createFinote` để tạo phiếu thu cọc.