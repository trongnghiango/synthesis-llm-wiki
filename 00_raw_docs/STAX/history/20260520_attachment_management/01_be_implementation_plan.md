# 01 — Kế hoạch Kiến trúc Chi tiết
# Feature: STAX Attachment / Document Management System
> Context folder: `docs/context/20260520_attachment_management/`

---

## A. Database Schema (Drizzle ORM)
**File:** `backend/src/database/schema/system/attachments.schema.ts`

**Thay đổi Schema `attachments` (Migration cần thiết):**
- **Thêm cột:** `organizationId: bigint('organization_id', { mode: 'number' }).notNull()`
- **Foreign Key:** Trỏ tới bảng `organizations.id` (onDelete: 'cascade')
- **Thêm Index:** `org_idx: index('idx_attachments_org').on(table.organizationId)`
- **Sửa type Helpers:** Cập nhật `AttachmentInsert` và `AttachmentSelect`

**Migration Strategy:** Chạy `drizzle-kit generate` để tạo file SQL migration.

---

## B. Domain Layer

**Entity:** `Attachment` (`backend/src/modules/system/domain/entities/attachment.entity.ts`)
- **Sửa Props:** Thêm `organizationId: number;`
- **Sửa Constructor:** Bind `_organizationId`
- **Thêm Getter:** `get organizationId()`

**Port (Interface):**
1. **Repository:** `IAttachmentRepository` (`system/domain/repositories/attachment.repository.ts`)
   - Cập nhật/Thêm: `findByOrganization(orgId: number): Promise<Attachment[]>`
   - Đảm bảo `findByEntity` hoạt động đúng.
2. **Storage Port:** `IFileStoragePort` (`system/application/ports/file-storage.port.ts`) - sẽ thay thế `IGoogleDriveService` hiện tại.
   - `upload(fileName: string, buffer: Buffer, mimeType: string): Promise<{ fileId: string; webViewLink: string; downloadLink: string }>`
   - `delete(fileId: string): Promise<void>`

---

## C. Infrastructure Layer

**1. Mapper:** `AttachmentMapper` (`system/infrastructure/persistence/mappers/attachment.mapper.ts`)
- Cập nhật `toDomain()` và `toPersistence()` để include `organizationId`.

**2. Repository Implementation:** `DrizzleAttachmentRepository` (`system/infrastructure/persistence/drizzle-attachment.repository.ts`)
- Implement `findByOrganization` với điều kiện `eq(attachments.organizationId, orgId)`.
- Đảm bảo tuân thủ `mapToUpdate()`.

**3. Storage Service Adapter:** `GoogleDriveAdapter` (`system/infrastructure/services/google-drive.service.ts`)
- Đổi tên class `GoogleDriveService` thành `GoogleDriveAdapter` và implements `IFileStoragePort`.
- Thêm error handling nếu `SERVICE_ACCOUNT_JSON_PATH` không tồn tại.

---

## D. Application Layer

**Service:** `AttachmentService` (`system/application/services/attachment.service.ts`)
- **Dependencies:** `IAttachmentRepository`, `IFileStoragePort` (abstract, không bind cứng Google Drive).
- **Methods:**
  - `uploadForEntity(orgId: number, entityType: string, entityId: number, file: Express.Multer.File, category: AttachmentCategory, tags?: string, currentUser?: any): Promise<Attachment>`
    - Flow: Gọi `fileStoragePort.upload()` -> Tạo `Attachment` entity -> `repo.save()` -> Catch error: Nếu `repo.save()` lỗi thì gọi `fileStoragePort.delete()` để rollback.
  - `listByOrganization(orgId: number): Promise<Attachment[]>`
  - `listByEntity(entityType: string, entityId: number): Promise<Attachment[]>`
  - `delete(id: number, currentUser: any): Promise<void>`
    - Flow: Gọi `repo.findById` -> Kiểm tra quyền (chỉ người upload hoặc admin được xóa) -> Gọi `fileStoragePort.delete()` (bỏ qua lỗi nếu file không tồn tại trên Drive) -> Gọi `repo.delete()`.

---

## E. Presentation Layer & Contracts

**1. Shared Contracts (Zod):** `shared/contracts/system/attachment.contract.ts`
- Định nghĩa Schema cho File, Response DTO (`AttachmentDto`).
- `AttachmentListResponse`: `{ items: AttachmentDto[], groupedByCategory: Record<string, AttachmentDto[]> }`

**2. Controller - Upload (CRM Domain):**
- `OrganizationController` (`crm/infrastructure/controllers/organization.controller.ts`)
  - `POST /:id/attachments` (Use `FileInterceptor`)
- `ContractController` (`crm/infrastructure/controllers/contract.controller.ts`)
  - `POST /:id/attachments` (Thay thế endpoint upload PDF cũ)
- `QuoteController` (`crm/infrastructure/controllers/quote.controller.ts`)
  - `POST /:id/attachments`
- **Flow Controller:** Validate quyền -> Gọi `AttachmentService.uploadForEntity`.

**3. Controller - System (System Domain):**
- `AttachmentController` (`system/infrastructure/controllers/attachment.controller.ts`)
  - `GET /` (Query Params: `organizationId`, `entityType`, `entityId`)
  - `DELETE /:id`

---

## F. Module Wiring

**SystemModule** (`system/system.module.ts`):
- Đổi DI binding từ `IGoogleDriveService` sang `IFileStoragePort`:
  `{ provide: IFileStoragePort, useClass: GoogleDriveAdapter }`
- Thêm `AttachmentService`, `AttachmentController`.
- Cập nhật `exports` để expose `AttachmentService` và `IFileStoragePort`.

**CrmModule** (`crm/crm.module.ts`):
- Import `SystemModule` (nếu chưa có).
- Bổ sung các routes upload trong các Controllers tương ứng.

---

Vui lòng gõ **'OK'** để tôi xuất Checklist thực thi (Bước 3).
