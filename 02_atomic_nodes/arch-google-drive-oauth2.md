---
id: arch-google-drive-oauth2
title: Chuyển đổi Google Drive sang OAuth 2.0
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on: []
summary: "Tái cấu trúc Google Drive Integration từ Service Account sang OAuth 2.0 qua REST API và Authorization Code Flow."
tags: [infrastructure, oauth2, google-drive, system-module]
---

## 1. Kiến trúc & Phụ thuộc
- **Module**: `system` (Tier 1 - Foundation). Cung cấp `IFileStoragePort` cho toàn hệ thống (e.g. `AttachmentService`).
- **Dependencies**: `ConfigModule` (đọc OAuth env vars).
- **Loại bỏ**: Package `googleapis` (chuyển sang HTTP `fetch` trực tiếp tới REST API v3 để tối ưu hóa bundle size).

## 2. API Contracts & Luồng Thiết lập (1-Time Setup)
- **Khởi tạo authorization code (Admin only)**:
  - `GET /api/google/authorize`: Yêu cầu `@JwtAuthGuard`. Redirect Admin tới Google Consent Screen.
  - `GET /api/google/callback`: `@Public()` (Google callback endpoint). Nhận `code` -> Exchange lấy `refresh_token` -> Hiển thị/Log để Admin cấu hình thủ công vào hệ thống `.env`.

## 3. Cơ chế Runtime & Bảo mật
- **Quản lý Token**: `GoogleOAuthService` chịu trách nhiệm renew `access_token` tự động từ `refresh_token` lưu ở `.env`.
- **Thực thi Storage**: `GoogleDriveService` implements `IFileStoragePort` thực hiện các tác vụ Upload/Delete file qua REST API v3 với header `Authorization: Bearer <access_token>`.
- **Bảo mật & Multi-tenancy**:
  - Không phân tách dữ liệu theo Tenant (`organizationId`) do đây là hạ tầng lưu trữ dùng chung của hệ thống STAX.
  - `refresh_token` được bảo vệ nghiêm ngặt trong biến môi trường cấp Server, không lưu trữ dưới Database.

## 4. Liên kết chéo
- Kiến trúc hệ thống và cổng Port-Adapter: `[[01_core_architecture]]`.
- Quản lý định dạng log khi gọi ngoại vi: `[[hb-delta-logging]]`.