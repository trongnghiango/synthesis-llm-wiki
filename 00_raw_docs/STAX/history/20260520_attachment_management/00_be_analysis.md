# 00 — Phân tích Nghiệp vụ & Kiến trúc
# Feature: STAX Attachment / Document Management System
> Context folder: `docs/context/20260520_attachment_management/`
> Base: Decision Log từ `@stax-think` session (2026-05-20)

---

## A. Phân loại Module

**Tier: 1 — Foundation** (SystemModule)

Lý do: Attachment/Document Management là **cross-cutting concern** — không thuộc riêng CRM, Accounting, hay HRM. Contract, Quote, Organization, Employee đều cần. Hạ tầng lưu trữ (Google Drive / Local / S3) là infrastructure thuần túy, không chứa business rule.

**Upload Controller lại nằm ở Tier 3 (CRM)**:
- `POST /organizations/:id/attachments` → OrganizationController (CRM)
- `POST /contracts/:id/attachments` → ContractController (CRM)
- `POST /quotes/:id/attachments` → QuoteController (CRM)
- Lý do: Domain controller validate entity tồn tại + user có quyền trước khi gọi AttachmentService

**Phụ thuộc:**
- SystemModule phụ thuộc: `ConfigService`, Google Drive SDK (`googleapis`)
- CRM phụ thuộc vào SystemModule (đã import): dùng `AttachmentService` qua DI

---

## B. Bounded Context & Ubiquitous Language

| Nghiệp vụ | Tên kỹ thuật |
|---|---|
| Tài liệu đính kèm | `Attachment` |
| Kho lưu trữ (Google Drive) | `IFileStoragePort` → `GoogleDriveAdapter` |
| Loại tài liệu | `AttachmentCategory` enum |
| Nhãn phân loại | `tags` (CSV string) |
| Entity chứa tài liệu | `entityType` + `entityId` (Polymorphic) |
| Tổ chức/Khách hàng | `organizationId` (denorm key để query tổng hợp) |
| Tab "Tài liệu" của khách | `listByOrganization` (tất cả file thuộc 1 org) |
| Section file của HĐ/BG | `listByEntity` (file của 1 entity cụ thể) |

---

## C. Data Flow & API Design

```
Upload (Domain-owned):
Client → OrganizationController.uploadAttachment()
       → validate org exists + user permission (CRM domain)
       → AttachmentService.uploadForEntity()
       → IFileStoragePort.upload() → Google Drive
       → IAttachmentRepository.save()
       → AttachmentDto response

List Org (System-owned):
Client → AttachmentController.listByOrg(?organizationId=5)
       → AttachmentService.listByOrganization(orgId)
       → IAttachmentRepository.findByOrganization(orgId)
       → AttachmentListDto { items, groupedByCategory }

List Entity (System-owned):
Client → AttachmentController.listByEntity(?entityType=contract&entityId=10)
       → AttachmentService.listByEntity(entityType, entityId)
       → IAttachmentRepository.findByEntity(entityType, entityId)

Delete (System-owned):
Client → AttachmentController.delete(:id)
       → AttachmentService.delete(id, currentUser)
       → verify uploader === currentUser OR admin
       → IFileStoragePort.delete(googleDriveId)  [soft-fail if Drive 404]
       → IAttachmentRepository.delete(id)
```

**Endpoints mới:**

| Method | Path | Module | Permission |
|---|---|---|---|
| POST | `/organizations/:id/attachments` | CRM | `lead:read` (org) |
| POST | `/contracts/:id/attachments` | CRM | `lead:read` (contract) |
| POST | `/quotes/:id/attachments` | CRM | `lead:read` (quote) |
| GET | `/attachments?organizationId=N` | System | `lead:read` |
| GET | `/attachments?entityType=X&entityId=N` | System | `lead:read` |
| DELETE | `/attachments/:id` | System | `lead:read` + ownership |

---

## D. Cross-module Dependencies

- `AttachmentService` (System) inject: `IFileStoragePort`, `IAttachmentRepository`
- `OrganizationController` (CRM) inject: `AttachmentService` ← export từ SystemModule
- `ContractController` (CRM) inject: `AttachmentService`
- `QuoteController` (CRM) inject: `AttachmentService`
- Không có Domain Event phát ra (upload/delete là I/O, không phải domain event)

---

## E. Multi-tenancy

- Mọi upload đều nhận `organizationId` từ entity được upload vào (Organization, Contract, Quote đều thuộc về 1 org)
- `organizationId` được lưu trực tiếp vào `attachments` table (denorm, không phải từ query string)
- List by org: filter `WHERE organization_id = ?` → tenant-safe
- Delete: check `uploaded_by_id = currentUser.id` OR role ADMIN

---

## F. Security (_actions / Server-Driven UI)

`Attachment` không cần `_actions` phức tạp. Response DTO đơn giản:
```typescript
{
  _actions: {
    delete: { allowed: boolean; reason?: string }
    // allowed = true nếu: uploader === currentUser OR currentUser.isAdmin
  }
}
```

---

## G. Hiện trạng Codebase (đã có)

| Component | Trạng thái |
|---|---|
| `GoogleDriveService` (upload/delete) | ✅ Có — cần refactor thành Adapter |
| `IGoogleDriveService` Port | ✅ Có — sẽ thay bằng `IFileStoragePort` |
| `Attachment` Entity | ✅ Có — thiếu `organizationId` |
| `attachments` schema | ✅ Có — thiếu `organizationId` column |
| `DrizzleAttachmentRepository` (save, findByEntity) | ✅ Có — cần thêm `findByOrganization` |
| `SystemModule` wiring | ✅ Có |
| `AttachmentService` | ❌ Không có |
| `AttachmentController` | ❌ Không có |
| Upload endpoints (Org/Contract/Quote) | ❌ Không có (chỉ có `/contracts/:id/pdf/upload` cũ) |
| `IFileStoragePort` (abstract storage) | ❌ Không có (chỉ có Google-specific port) |

---

## H. Những gì KHÔNG làm trong sprint này

- Không tự động tạo folder structure trên Drive (`/{clientId}/Contracts`)
- Không preview file trong app (chỉ `webViewLink` mở Google Docs)
- Không version control cho file
- Không bulk upload (1 file/request)
- Không FE component (sẽ làm trong `@stax-frontend` session riêng)

---

Vui lòng gõ **'OK'** để tôi tiến hành thiết kế kiến trúc chi tiết.
