---
id: arch-gdrive-multitenant-cleanup
title: Tối ưu Lưu trữ Đa Tiến trình Google Drive và Cache Thư mục
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
summary: "Cơ chế cache cấu trúc thư mục Google Drive O(1) và chuẩn hóa tên file đa tenant qua IFileStoragePort."
tags: [storage, google-drive, multi-tenancy, cache, performance]
---

### 1. Kiến trúc Hệ thống & Port-Adapter
- **Dependency Inversion**: Domain/Application nghiệp vụ giao tiếp độc lập qua `IFileStoragePort`.
- **Infrastructure**: Triển khai thực tế tại `GoogleDriveService`, xử lý việc phân loại và dọn dẹp tên file.
- **Tenant Isolation**: Cách ly tuyệt đối thư mục và file dựa trên `organizationId` qua context `options: { organizationId, entityType, entityId }`.

### 2. Thiết kế Cơ sở Dữ liệu & Cấu trúc Thư mục
- **Bảng Cache**: `google_drive_folders` (lưu trữ và tra cứu nhanh `driveFolderId` ảo).
- **Hiệu năng**: Chuyển đổi thao tác tìm/tạo thư mục của Google API từ O(N) về **O(1)**.
- **Cấu trúc Thư mục 3 Cấp**:
  - **Cấp 1 (Root/Tenant)**: Tên Tenant dạng không dấu (e.g., `nha_khoa_kim_cuong`).
  - **Cấp 2 (Module)**: Phân hệ nghiệp vụ (e.g., `crm-leads`, `accounting-finotes`).
  - **Cấp 3 (Thời gian)**: Nhóm theo tháng năm (e.g., `2026-05`).

### 3. Quy chuẩn Đặt tên File & Xử lý Unicode
- **Quy tắc đặt tên file vật lý**: `[MODULE]_[ID]_[TIMESTAMP]_[sanitized_file_name.ext]`
  - *Ví dụ*: `LEAD_1179_1716382800_hop_dong_kieu_mau.pdf`
- **Xử lý Tiếng Việt**: Sử dụng bảng ánh xạ thủ công (Manual Map Table) xử lý các ký tự Unicode đặc biệt (đặc biệt là chữ "Đ/đ" và nguyên âm ghép dấu) trước khi áp dụng Regex loại bỏ dấu tiếng Việt để tránh mất ký tự.

### 4. Exit Verification
- **Domain Purity**: Không chứa tham chiếu NestJS / Drizzle bên trong `system/domain/`.
- **Unit Test**: Cập nhật mock object và signature trong `attachment.service.spec.ts` tương thích 100% với context options mới.