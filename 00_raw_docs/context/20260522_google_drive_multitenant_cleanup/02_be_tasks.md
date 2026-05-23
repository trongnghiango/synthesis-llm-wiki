# 02. Checklist Thực thi: Google Drive Multi-Tenant Cleanup

**Ngày:** 2026-05-22 | **Tier:** 1 — Foundation | **Scope:** Core Infrastructure / Storage

---

## Trình tự thực hiện bắt buộc:

- [ ] 1. Khai báo schema CSDL mới cho `google_drive_folders` tại `backend/src/database/schema/system/google-drive-folders.schema.ts`.
- [ ] 2. Đăng ký export schema mới vào `backend/src/database/schema/index.ts`.
- [ ] 3. Phát sinh file migration mới bằng Drizzle Kit: `pnpm --dir backend db:generate`.
- [ ] 4. Áp dụng schema mới lên cơ sở dữ liệu Dev: `pnpm --dir backend db:push` (hoặc chạy qua migration).
- [ ] 5. Cập nhật `IFileStoragePort` tại `backend/src/modules/system/application/ports/file-storage.port.ts` để hỗ trợ options truyền Tenant và Phân hệ nghiệp vụ.
- [ ] 6. Cập nhật `GoogleDriveService` tại `backend/src/modules/system/infrastructure/services/google-drive.service.ts`:
    - [ ] Thêm hàm sanitizeFilename xử lý Tiếng Việt chuẩn.
    - [ ] Inject `NodePgDatabase<typeof schema>` từ Drizzle.
    - [ ] Triển khai thuật toán resolveFolder 3 cấp (Tenant Root ➔ Phân hệ nghiệp vụ ➔ Năm-Tháng YYYY-MM) kèm cơ chế cache DB cục bộ.
    - [ ] Áp dụng chuẩn hóa tên file trên Drive.
- [ ] 7. Cập nhật `AttachmentService` tại `backend/src/modules/system/application/services/attachment.service.ts` để truyền đầy đủ tham số Tenant/Phân hệ khi upload file.
- [ ] 8. Kiểm tra biên dịch TypeScript toàn dự án: `pnpm --dir backend build` để đảm bảo 0 lỗi biên dịch.
- [ ] 9. Viết Unit / Integration Test hoặc chạy thử nghiệm trực tiếp thông qua Swagger/Client để xác thực chức năng.

---

Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
