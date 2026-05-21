---
id: dom-attachment-management
title: Tích hợp Frontend Hệ thống Quản lý Tài liệu đính kèm (Attachments)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on: []
summary: "Tích hợp React Query Hooks và Component AttachmentBoard polymorph để quản lý tài liệu đính kèm của Client, Contract, Lead."
tags: [frontend, react-query, attachment, drag-drop, polymorphic]
---

### 1. API & React Query Hooks
- **API (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/system/api/system.api.ts`)**: 
  - Bổ sung `getAttachments`, `uploadAttachment` (Polymorphic), và `deleteAttachment`.
- **Hooks (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/system/hooks/useAttachments.ts`)**:
  - `useAttachments`, `useUploadAttachment`, `useDeleteAttachment`: Quản lý state/cache qua React Query, tự động invalidation và trigger Toast.

### 2. UI Component & Tích hợp Trang
- **Shared Component (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/components/common/AttachmentBoard.tsx`)**:
  - Hỗ trợ Drag & Drop (bo viền dashed hover), hiển thị Progress Bar (Google Drive upload), phân loại tag, phân biệt icon theo định dạng.
  - Phân quyền xóa: chỉ cho phép khi `uploadedById === currentUser.id` hoặc user là `ADMIN`.
- **Tích hợp CRM Pages**:
  - **Client (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/client-detail.tsx`)**: Render `<AttachmentBoard entityType="client" />` tại tab "Tài liệu".
  - **Contract (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/contract-detail.tsx`)**: Thay tab "Xem File PDF" bằng `<AttachmentBoard entityType="contract" />`.
  - **Lead (`/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/lead-detail.tsx`)**: Nâng cấp lên 4 tabs, thêm tab "Tài liệu" render `<AttachmentBoard entityType="lead" />`.

### 3. Tiêu chuẩn Kỹ thuật & UX
- **TypeScript**: Biên dịch thành công 100% (`npm run check` trả về Code 0).
- **UX/Responsive**: Tự động co giãn (Flexbox wrap), giới hạn file upload tối đa 20MB kèm whitelist định dạng, hiển thị toast phản hồi trạng thái chi tiết.