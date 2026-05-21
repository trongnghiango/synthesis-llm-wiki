---
id: dom-manual-accounting-entries
title: Nghiệp vụ Lập Phiếu Thu/Chi Thủ công & Bút toán Nhật ký
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Tích hợp giao diện và DTO hỗ trợ lập phiếu thu/chi thủ công và định khoản trực tiếp trong phân hệ kế toán STAX."
tags: [accounting, journal-entry, finote, dto, backend, frontend]
---

## 1. Luồng Nghiệp vụ & Kiến trúc Tích hợp
* **Luồng 1 (Phiếu thu/chi thủ công):** Khởi tạo -> Phê duyệt -> Ghi nhận Sổ Quỹ -> Tự động sinh bút toán Nhật ký chung (`[[dom-accounting-finote]]`).
* **Luồng 2 (Bút toán thủ công):** Định khoản tay trực tiếp qua `JournalEntryForm` -> Gọi mutation tạo bút toán -> Tự động kích hoạt cơ chế refetch bảng dữ liệu.

## 2. Thay đổi Kỹ thuật & API Contracts

### Backend DTOs & Validation
* **Đường dẫn tệp:**
  * `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/dtos/create-finote.dto.ts`
  * `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/infrastructure/dtos/create-finote.request.dto.ts`
* **Cập nhật:**
  * Bổ sung trường `partyName?: string` vào DTO để class-validator cho phép nhận thông tin tên đối tác/khách hàng đối với phiếu thu/chi thủ công.
  * Chuẩn hóa giá trị mặc định của trường `category` từ client truyền lên thành `"OTHER"` để khớp chính xác với Enum `FinoteCategory` ở Backend.

### Frontend Components
* `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/components/create-finote-dialog.tsx`: Thiết kế Bento gradient, tự động thay đổi giao diện theo loại Phiếu.
* `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/finotes.tsx`: Loại bỏ nút tĩnh, tích hợp `CreateFinoteDialog` để kích hoạt luồng nghiệp vụ thực tế.
* `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/journal-entries.tsx`: Kết nối nút "Thêm Bút toán mới" với Dialog chứa `JournalEntryForm` và cấu hình tự động refetch.