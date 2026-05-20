# 02 — Checklist Thực thi
# Feature: STAX Attachment / Document Management System
> Context folder: `docs/context/20260520_attachment_management/`

---

## Trình tự Thực thi BẮT BUỘC

- [x] **1. Shared Contracts (Zod tại shared/contracts/)**
  - Tạo `shared/contracts/system/attachment.contract.ts` (AttachmentDto, ListResponse, UploadSchema).
- [x] **2. Database Schema (schema file + index export)**
  - Cập nhật `backend/src/database/schema/system/attachments.schema.ts` (Thêm `organizationId`, relations, type helpers).
- [x] **3. pgEnum definitions**
  - Kiểm tra `attachmentCategoryEnum` (Đã có, không cần thay đổi).
- [x] **4. Run migration (drizzle-kit generate)**
  - Chạy `pnpm db:generate` và `pnpm db:push` (nếu dùng local) hoặc tạo script quick-fix.
- [x] **5. Domain Entity + Props interface**
  - Cập nhật `backend/src/modules/system/domain/entities/attachment.entity.ts`.
- [x] **6. Value Objects (nếu có)**
  - (Không có)
- [x] **7. Repository Interface (Port + DI Token)**
  - Cập nhật `backend/src/modules/system/domain/repositories/attachment.repository.ts`.
  - Sửa `IGoogleDriveService` thành `IFileStoragePort`.
- [x] **8. Domain Events (nếu có)**
  - (Không có)
- [x] **9. Mapper (toDomain + toPersistence)**
  - Cập nhật `backend/src/modules/system/infrastructure/persistence/mappers/attachment.mapper.ts`.
- [x] **10. Repository Implementation (DrizzleXxxRepository)**
  - Cập nhật `backend/src/modules/system/infrastructure/persistence/drizzle-attachment.repository.ts`.
  - Đổi tên & implement `GoogleDriveAdapter` từ `GoogleDriveService`.
- [x] **11. Application Service**
  - Viết `AttachmentService` đóng vai trò Orchestrator.
- [x] **12. Request/Response DTOs (trong module)**
  - Tái sử dụng `AttachmentDto`, `AttachmentUploadDto`, `AttachmentListDto` từ shared/contracts hoặc định nghĩa mới.
- [x] **13. Controller (Endpoints)**
  - Tái cấu trúc (hoặc tạo mới) các Endpoint:
    - `POST /crm/organizations/:id/attachments`
    - `POST /crm/contracts/:id/attachments` (thay vì `:id/pdf/upload`)
    - `POST /crm/quotes/:id/attachments` (CrmModule).
- [x] **14. Module Wiring + index.ts export**
  - Cập nhật `SystemModule` và `CrmModule`.
- [x] **15. Unit Test (Service — mock repositories)**
  - Viết Unit Test cho `AttachmentService`.
- [x] **16. Integration Test (Repository — PGLite)**
  - Viết Integration Test cho `DrizzleAttachmentRepository`.
- [x] **17. npm run build — 0 TypeScript error**
  - Build hệ thống.
- [x] **18. Manual API test via Swagger**
  - Kiểm tra API trên Swagger UI.
