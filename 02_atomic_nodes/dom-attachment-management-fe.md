---
id: dom-attachment-management-fe
title: Tích hợp Frontend Quản lý Tài liệu đính kèm Polymorphic
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-attachment-management-be]]"
summary: "Tích hợp UI Component AttachmentBoard polymorphic vào các thực thể CRM (Lead, Client, Contract) qua React Query."
tags: [frontend, attachment, polymorphic, react-query, crm]
---

### 1. API & React Query Hooks
* **API Methods** (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/system/api/system.api.ts`):
  * `getAttachments(entityType, entityId)`
  * `uploadAttachment(entityType, entityId, file)` (Hỗ trợ polymorphic binding)
  * `deleteAttachment(id)`
* **React Query Hooks** (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/system/hooks/useAttachments.ts`):
  * Cung cấp: `useAttachments`, `useUploadAttachment`, `useDeleteAttachment`.
  * Cơ chế: Tự động invalidate cache và tích hợp thông báo Toast trạng thái.

### 2. Shared Component & Phân quyền
* **Component** `<AttachmentBoard>` (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/components/common/AttachmentBoard.tsx`):
  * Giao diện: Hỗ trợ Drag & Drop, thanh tiến trình (Progress Bar) đồng bộ Google Drive, phân loại tag/danh mục.
  * Phân quyền (Authorization): Chỉ cho phép `ADMIN` hoặc chủ sở hữu (`uploadedById === currentUser.id`) thực hiện xóa tài liệu.

### 3. Tích hợp Trang (Page Integrations)
* **Client Detail** (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/client-detail.tsx`): Thay thế tab tài liệu cũ bằng `<AttachmentBoard entityType="client" />`.
* **Contract Detail** (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/contract-detail.tsx`): Tích hợp `<AttachmentBoard entityType="contract" />`.
* **Lead Detail** (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/lead-detail.tsx`): Bổ sung tab thứ 4 tích hợp `<AttachmentBoard entityType="lead" />`.