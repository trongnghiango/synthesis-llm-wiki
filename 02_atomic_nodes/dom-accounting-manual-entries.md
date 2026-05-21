---
id: dom-accounting-manual-entries
title: Tích hợp Lập Phiếu Thu/Chi & Bút Toán Thủ Công
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Triển khai UI lập phiếu thu/chi, định khoản thủ công và cập nhật DTO Backend (partyName, FinoteCategory)"
tags: [accounting, manual-entry, dto, frontend, backend]
---

## 1. Thay đổi Codebase (Absolute Paths)
*   `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/dtos/create-finote.dto.ts` & `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/infrastructure/dtos/create-finote.request.dto.ts`:
    *   Bổ sung trường `partyName?: string` vào DTO nhận diện tên đối tác/khách hàng đối với phiếu thủ công.
    *   Chuẩn hóa default `category` của Client sang `"OTHER"` để tương thích chính xác với enum `FinoteCategory` của Backend.
*   `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/components/create-finote-dialog.tsx`: Component Dialog UI Bento gradient, tự động thay đổi màu sắc chủ đạo theo loại Phiếu Thu hoặc Phiếu Chi.
*   `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/finotes.tsx`: Thay thế hoàn toàn các nút tĩnh (dead buttons) bằng trigger gọi `CreateFinoteDialog`.
*   `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/accounting/journal-entries.tsx`: Tích hợp `JournalEntryForm` vào Dialog lớn của nút "Thêm Bút toán mới", tự động refetch bảng dữ liệu sau khi mutation thành công.

## 2. Luồng Nghiệp vụ Nghiệm thu
*   **Luồng 1 (Gián tiếp qua Sổ quỹ)**: Tạo phiếu thu/chi thủ công $\rightarrow$ Phê duyệt $\rightarrow$ Ghi nhận Sổ quỹ $\rightarrow$ Tự động sinh bút toán Nhật ký chung (Journal Entries).
*   **Luồng 2 (Trực tiếp)**: Định khoản thủ công trực tiếp bằng tay thông qua giao diện Nhật ký chung.

## 3. Liên kết Hệ thống
*   Nghiệp vụ Quản lý Phiếu: `[[dom-accounting-finote]]`
*   Hệ thống Định khoản Nhật ký: `[[dom-accounting-journal]]`