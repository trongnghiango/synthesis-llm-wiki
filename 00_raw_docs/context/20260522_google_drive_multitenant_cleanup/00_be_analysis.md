# 00. Phân tích Nghiệp vụ & Kiến trúc: Google Drive Multi-Tenant Cleanup

**Ngày:** 2026-05-22 | **Tier:** 1 — Foundation | **Scope:** Core Infrastructure / Storage

---

## A. Phân loại module
- **Phân loại:** Tier 1 — Foundation (Dịch vụ lưu trữ thuộc phân hệ `system` module). Không chứa logic nghiệp vụ, cung cấp cổng giao tiếp `IFileStoragePort` cho toàn bộ các module nghiệp vụ của hệ thống.
- **Quan hệ phụ thuộc:**
  - **Phụ thuộc vào:**
    - `ConfigModule` để lấy các biến môi trường cấu hình OAuth Google Drive.
    - `DRIZZLE` Database provider để thực hiện lưu trữ/truy vấn bộ đệm (cache) đường dẫn thư mục ảo.
  - **Được phụ thuộc bởi:**
    - `AttachmentService` (Tier 1) dùng để upload/delete file nghiệp vụ Polymorphic.
    - Các controller nghiệp vụ (Leads, Contracts, Quotes, Organizations) thông qua `AttachmentService`.

---

## B. Bounded Context & Ubiquitous Language

| Nghiệp vụ (Business Term) | Kỹ thuật (Technical Term) | Mô tả |
| :--- | :--- | :--- |
| File đính kèm | `Attachment` | File tài liệu được tải lên gán với một thực thể bất kỳ |
| Thư mục gốc dùng chung | `Root Folder` | Thư mục cha trên Google Drive, chứa toàn bộ dữ liệu của STAX |
| Thư mục của công ty | `Tenant Folder` | Thư mục riêng biệt của từng Organization |
| Thư mục nghiệp vụ | `Module Folder` | Thư mục phân loại theo nghiệp vụ (ví dụ: `crm-leads`, `accounting-finotes`) |
| Thư mục theo kỳ thời gian | `Period Folder` | Thư mục phân loại theo năm-tháng dạng `YYYY-MM` |
| Bộ đệm đường dẫn | `googleDriveFolders` | Bảng CSDL cache lại ID thư mục vật lý của Google Drive |

---

## C. Data Flow & API Design

### 1. Luồng dữ liệu (Data Flow)
```text
Client (FormData with File) 
   ➔ Controller (LeadController/ContractController) [Nhận file qua Multer]
   ➔ AttachmentService.uploadForEntity() [Xác thực kích thước, MIME type]
   ➔ GoogleDriveService.uploadFile() [Gọi resolveFolder() tìm/tạo thư mục]
   ➔ GoogleDriveService.resolveFolder() [Truy vấn bảng google_drive_folders]
   ➔ Google Drive API [Tạo thư mục vật lý nếu cache miss]
   ➔ CSDL (attachments table) [Lưu metadata file]
   ➔ Trả về Attachment Entity ➔ Client
```

### 2. Thiết kế API / Hợp đồng
Các Endpoint nghiệp vụ hiện tại vẫn giữ nguyên, nhưng sẽ được tối ưu hóa ở phần xử lý bên dưới. API Attachment Controller chính:
- `GET /attachments`: Lấy danh sách attachments của tenant/thực thể, phân loại dạng Server-Driven Grouping.
- `DELETE /attachments/:id`: Xóa tài liệu khỏi Drive vật lý và CSDL.

---

## D. Cross-module dependencies
- `GoogleDriveService` cần truy xuất bảng `organizations` để lấy tên doanh nghiệp (`organizationName`) nhằm đặt tên cho thư mục Tenant Root dạng chữ không dấu sạch sẽ.
- Khi upload file thành công, `AttachmentService` sẽ phát hành Audit Log sự kiện dạng fire-and-forget qua `IAuditLogService`.

---

## E. Multi-tenancy
- **Cô lập dữ liệu tuyệt đối:** Mỗi Organization chỉ được phép upload và xem file trong thư mục Google Drive mang tên chính Organization đó.
- Bảng cache `google_drive_folders` bắt buộc phải có cột `organizationId` và có index duy nhất kết hợp `(organization_id, path)` để đảm bảo không xảy ra rò rỉ dữ liệu giữa các doanh nghiệp (Tenant Isolation).
- Toàn bộ các câu query CSDL trong `DrizzleAttachmentRepository` đều phải tự động áp dụng bộ lọc `organizationId` hoặc thông qua Base Repository.

---

## F. Security & _actions (Server-Driven UI)
- Toàn bộ API upload/delete file đính kèm được bảo vệ nghiêm ngặt bởi `JwtAuthGuard` và `PermissionGuard` để phân quyền cụ thể theo chức năng của từng module (ví dụ: `lead:edit` để tải file cho Lead).
- Khi trả về danh sách Attachment, các hành động cho phép (`_actions.allowed`) như `DELETE` sẽ được quyết định dựa trên việc người dùng hiện tại có phải là người sở hữu file đó (`uploadedById === currentUser.id`) hoặc có quyền `Admin` hệ thống.

---

Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết.
