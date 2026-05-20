# Checklist Thực thi Frontend - Hệ thống Quản lý Tài liệu đính kèm (Attachments)

> Context Folder: `docs/context/20260520_attachment_management/`
> Tệp checklist: `02_fe_tasks.md`

## Trình tự Thực thi BẮT BUỘC

- [x] **1. Xác minh Contracts (Verify Contracts)**
  - Xác nhận Zod schema và Type definitions đã tồn tại tại `frontend/shared/contracts/system.ts`.
- [x] **2. Tích hợp API Client (`system.api.ts`)**
  - Cập nhật `/frontend/client/src/modules/system/api/system.api.ts` để thêm 3 endpoint: `getAttachments`, `uploadAttachment`, và `deleteAttachment`.
- [x] **3. Viết React Query Custom Hooks (`useAttachments.ts`)**
  - Tạo file `/frontend/client/src/modules/system/hooks/useAttachments.ts` chứa các hook: `useAttachments`, `useUploadAttachment`, và `useDeleteAttachment`.
  - Tích hợp Toast notification và cơ chế `queryClient.invalidateQueries` tự động sau mutations.
- [x] **4. Xây dựng UI Components (`AttachmentBoard` và các component con)**
  - Tạo `/frontend/client/src/components/common/AttachmentBoard.tsx` làm giao diện bọc ngoài.
  - Tạo file kéo thả Premium Drag-and-Drop Uploader (tương thích form category và tags, hiển thị progress bar khi uploading).
  - Tạo danh sách hiển thị tài liệu phân loại (AttachmentList) hiển thị tên file, icon loại file, ngày tải lên, người tải, và phân quyền hiển thị nút Xóa.
- [x] **5. Tích hợp vào màn hình Client Detail (`client-detail.tsx`)**
  - Thay thế phần placeholder tại tab `documents` bằng `<AttachmentBoard entityType="client" entityId={orgId} organizationId={orgId} />`.
- [x] **6. Tích hợp vào màn hình Contract Detail (`contract-detail.tsx`)**
  - Thay thế phần placeholder tại tab `pdf` bằng `<AttachmentBoard entityType="contract" entityId={contractId} organizationId={contract.organizationId} />`.
- [x] **7. Tích hợp vào màn hình Lead Detail (`lead-detail.tsx`)**
  - Bổ sung tab Tài liệu đính kèm `<TabsTrigger value="attachments">Tài liệu</TabsTrigger>` và render `<AttachmentBoard entityType="lead" entityId={leadId} organizationId={lead.organizationId || 1} />`.
- [x] **8. TypeScript & Quality Verification (`npm run check`)**
  - Chạy kiểm tra TypeScript lỗi type trong toàn bộ dự án frontend.
  - Kiểm tra Responsive trên các thiết bị di động (Mobile layout) và đảm bảo không rò rỉ console error.
