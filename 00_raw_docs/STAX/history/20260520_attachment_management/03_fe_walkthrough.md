# Hướng dẫn Bàn giao Frontend - Hệ thống Quản lý Tài liệu đính kèm (Attachments)

> Context Folder: `docs/context/20260520_attachment_management/`
> Tệp bàn giao: `03_fe_walkthrough.md`

## 1. Các Tệp tin Đã thay đổi & Tạo mới (Files Created & Modified)

### A. API & Hooks
- **[MODIFY]** [system.api.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/system/api/system.api.ts): Bổ sung 3 phương thức API: `getAttachments`, `uploadAttachment` (Polymorphic), và `deleteAttachment`.
- **[NEW]** [useAttachments.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/system/hooks/useAttachments.ts): Thiết lập Custom Hooks cho React Query (`useAttachments`, `useUploadAttachment`, `useDeleteAttachment`) để quản lý cache, tự động invalidation và hiển thị Toast phản hồi.

### B. Shared UI Component
- **[NEW]** [AttachmentBoard.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/components/common/AttachmentBoard.tsx): Component bọc ngoài kết hợp kéo thả file (Drag & Drop), thanh tiến trình (Progress Bar), phân biệt định dạng file bằng Icon, phân loại danh mục, gán nhãn tags, và kiểm tra phân quyền xóa file (uploadedById vs currentUser.id / ADMIN).

### C. Tích hợp Trang (Page Integrations)
- **[MODIFY]** [client-detail.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/client-detail.tsx): Thay thế tab "Tài liệu" cũ bằng `<AttachmentBoard entityType="client" ... />`.
- **[MODIFY]** [contract-detail.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/contract-detail.tsx): Đổi tên tab "Xem File PDF" thành "Tài liệu đính kèm" và render `<AttachmentBoard entityType="contract" ... />`.
- **[MODIFY]** [lead-detail.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/lead-detail.tsx): Chuyển đổi layout từ 3 tabs sang 4 tabs, thêm tab "Tài liệu" render `<AttachmentBoard entityType="lead" ... />`.

---

## 2. Kết quả Kiểm thử & Chất lượng (Quality & Validation Results)

### A. Biên dịch TypeScript
Chúng ta đã chạy `npm run check` (thực thi `tsc`) trên toàn bộ dự án Frontend:
- **Kết quả**: **Thành công 100% với Code 0**. Không phát sinh bất kỳ lỗi kiểu dữ liệu (Type errors) hay import sai đường dẫn nào trong toàn bộ mã nguồn.

### B. Responsive & UX Quality Checklist
- **Mobile Friendly**: Sử dụng Flexbox tự động quấn dòng trên màn hình hẹp, các Action Buttons (`Xem Drive`, `Xoá`) tự động co giãn và căn chỉnh hợp lý.
- **Drag & Drop Animation**: Bo viền nét đứt (dashed), đổi background mượt mà khi hover hoặc kéo file đè lên uploader.
- **Progress bar**: Hoạt động mượt mà khi tải tệp lên Google Drive.
- **Toast Notifications**: Hiển thị Toast lục sắc khi thành công, đỏ rực rỡ khi thất bại (ví dụ: upload tệp quá 20MB hoặc không đúng định dạng whitelist).

---

Giao diện đã sẵn sàng hoạt động cùng với Backend polymorph! Hệ thống đã hoàn thiện cả 2 phân hệ BE và FE.
