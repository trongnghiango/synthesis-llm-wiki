# Bước 3: Checklist Thực thi — Module Service Catalog

## 🏗️ Cơ sở hạ tầng & Database
- [ ] 1. Khai báo Schema `services.schema.ts` (id, name, type, status, basePrice).
- [ ] 2. Khai báo Schema `contract-items.schema.ts` liên kết với `contracts`.
- [ ] 3. Cập nhật `quotes.schema.ts` thêm cột `serviceId` vào `quoteItems`.
- [ ] 4. Export các schema mới trong `src/database/schema/index.ts`.
- [ ] 5. Chạy migration để cập nhật database.

## 🧬 Domain Layer
- [ ] 6. Định nghĩa Domain Entity `Service` (`src/modules/crm/domain/entities/service.entity.ts`).
- [ ] 7. Định nghĩa Repository Interface `IServiceRepository` và `Symbol` DI token.
- [ ] 8. Cập nhật Entity `Contract` để hỗ trợ danh sách `items`.

## 🔌 Infrastructure Layer
- [ ] 9. Viết `ServiceMapper` (toDomain/toPersistence).
- [ ] 10. Triển khai `DrizzleServiceRepository` kế thừa `DrizzleBaseRepository`.
- [ ] 11. Bổ sung `DrizzleContractItemRepository` nếu cần hoặc gộp vào `ContractRepository`.

## ⚙️ Application Layer
- [ ] 12. Triển khai `ServiceCatalogService` (CRUD dịch vụ).
- [ ] 13. Cập nhật `LeadWorkflowService`: Logic chuyển đổi Quote Items sang Contract Items khi Won.

## 🚀 Presentation Layer & Wiring
- [ ] 14. Viết `ServiceController` với các đầu API đã thiết kế.
- [ ] 15. Khai báo Request/Response DTOs cho Service.
- [ ] 16. Wiring trong `CRMModule` (providers, exports).

## 🧪 Testing & Validation
- [ ] 17. `npm run build` kiểm tra lỗi TypeScript.
- [ ] 18. Viết Unit Test cơ bản cho `ServiceCatalogService`.
- [ ] 19. Test thủ công qua Swagger các API mới.

---
Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
