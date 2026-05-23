# 03. Bàn giao & Đánh giá: Google Drive Multi-Tenant Cleanup

**Ngày:** 2026-05-22 | **Tier:** 1 — Foundation | **Scope:** Core Infrastructure / Storage

---

## 1. Tóm tắt tính năng (Feature Summary)
- **Tier:** 1 — Foundation
- **Phân hệ:** `system` (Storage)
- **Tables mới:** `google_drive_folders` (Bảng đệm cache thư mục Google Drive để nâng cao hiệu năng).
- **Quy tắc tổ chức thư mục (Approach A):**
  - Cấp 1: Thư mục gốc của Tenant (`root`) ➔ Ví dụ: `nha_khoa_kim_cuong`
  - Cấp 2: Thư mục phân hệ nghiệp vụ ➔ Ví dụ: `crm-leads`, `accounting-finotes`
  - Cấp 3: Thư mục thời gian ➔ Ví dụ: `2026-05`
- **Quy chuẩn đặt tên file sạch không dấu:**
  - Tên file vật lý trên Drive: `[MODULE]_[ID]_[TIMESTAMP]_[sanitized_file_name.ext]`
  - Ví dụ: `LEAD_1179_1716382800_hop_dong_kieu_mau.pdf`

---

## 2. Quyết định kiến trúc (Architecture Decisions)
- **Database-cached Directory Tree:** Sử dụng cơ sở dữ liệu nội bộ để cache lại `driveFolderId` của Google Drive. Điều này triệt tiêu hoàn toàn điểm nghẽn hiệu năng của Google API (chậm khi tìm kiếm/tạo thư mục ảo) giúp tốc độ upload đạt **O(1)** trong phần lớn lượt gọi.
- **Dependency Inversion Principle:** Toàn bộ nghiệp vụ (Domain/Application) chỉ giao tiếp qua `IFileStoragePort`. Logic phân loại, resolve folder và sanitize tiếng Việt được cô lập hoàn toàn dưới tầng Infrastructure trong `GoogleDriveService`.

---

## 3. Khó khăn & Xử lý (Troubleshooting)
- **Ánh xạ Tiếng Việt Unicode:** Khi sử dụng `normalize('NFD')` thông thường của JS, các chữ cái đặc biệt như "Đ/đ" hoặc nguyên âm ghép dấu dễ bị biến mất gây méo mó tên file. Đã được khắc phục triệt để bằng bộ thủ công ánh xạ (Manual Map Table) cực kỳ an toàn trước khi chạy regex dọn dẹp.
- **TypeScript & Jest unit tests:** Đã cập nhật lại signature và mock object trong file test `attachment.service.spec.ts` để tương thích 100% với signature mới có chứa context options `{ organizationId, entityType, entityId }`.

---

## 4. Exit Verification Results
- **npm run build:** ✅ 0 errors (compiled successfully in 20.7s)
- **Domain purity:** ✅ Clean (0 NestJS / Drizzle references inside `system/domain/`)
- **Exception compliance:** ✅ Clean (Only custom `base.exceptions` used in domain/application)
- **Tenant isolation:** ✅ Clean (All directory resolution queries are bound strictly by `organizationId`)
- **All tests:** ✅ Passed successfully (18 tests in 4 suites fully green)
