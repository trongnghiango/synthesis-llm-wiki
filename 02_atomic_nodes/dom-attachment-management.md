---
id: dom-attachment-management
title: Tích hợp Frontend Quản lý Tài liệu đính kèm
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-polymorphic-attachments]]"
summary: "Tích hợp UI Component AttachmentBoard đa hình, React Query Hooks và quản lý tài liệu trên Client, Contract, Lead."
tags: [frontend, attachment, react-query, polymorphic, uploader]
---

### 1. API & Hooks Client
- **API (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/system/api/system.api.ts`)**:
  - `getAttachments(entityType, entityId)`
  - `uploadAttachment(entityType, entityId, file)` (Polymorphic API)
  - `deleteAttachment(id)`
- **Hooks (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/system/hooks/useAttachments.ts`)**:
  - `useAttachments`, `useUploadAttachment`, `useDeleteAttachment` (React Query).
  - Tự động invalidate cache khi upload/delete thành công.

### 2. Component Chung: `AttachmentBoard`
- **Đường dẫn**: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/components/common/AttachmentBoard.tsx`
- **Tính năng & Nghiệp vụ**:
  - Drag & Drop UI (Bo viền dashed, transition mượt mà).
  - Tích hợp thanh tiến trình (Progress bar) đồng bộ tải tệp lên Google Drive.
  - Phân quyền xóa: `uploadedById === currentUser.id` hoặc người dùng có vai trò `ADMIN`.
  - Phân loại tài liệu theo danh mục và gán tags động.

### 3. Tích hợp Trang (CRM Pages)
Nhúng `<AttachmentBoard entityType="..." entityId="..." />` vào các luồng nghiệp vụ:
- **Client Detail** (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/client-detail.tsx`): Thay thế tab "Tài liệu" cũ.
- **Contract Detail** (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/contract-detail.tsx`): Thay thế tab "Xem File PDF".
- **Lead Detail** (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/lead-detail.tsx`): Nâng cấp lên layout 4 tabs, thêm tab "Tài liệu".

### 4. Chất lượng kỹ thuật (Quality Checklist)
- **TypeScript**: `npm run check` (thực thi `tsc`) đạt **Code 0** (không lỗi Type/Import).
- **UX & RWD**: Hỗ trợ Flexbox tự động co giãn trên Mobile, kiểm soát upload tệp tin tối đa 20MB theo whitelist, Toast cảnh báo trực quan.