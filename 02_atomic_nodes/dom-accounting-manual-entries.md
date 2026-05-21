---
id: dom-accounting-manual-entries
title: Luồng nghiệp vụ lập phiếu thu chi và bút toán thủ công
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Tích hợp giao diện và DTO Backend cho luồng lập phiếu thu/chi thủ công (Finote) và định khoản bút toán tay (Journal Entry)."
tags: [accounting, finote, journal-entry, dto, frontend]
---

## 1. Luồng Nghiệp vụ Cốt lõi (Core Business Flows)
* **Luồng 1 (Phiếu thủ công):** Lập phiếu thu/chi -> Phê duyệt -> Sổ Quỹ -> Tự động sinh bút toán Nhật ký chung. Chi tiết thực thể xem tại `[[dom-accounting-finote]]`.
* **Luồng 2 (Bút toán thủ công):** Định khoản tay trực tiếp trên giao diện Nhật ký chung.

## 2. API Contract & Thay đổi Backend
Tệp tin sửa đổi:
* `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/application/dtos/create-finote.dto.ts`
* `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/infrastructure/dtos/create-finote.request.dto.ts`

**Thay đổi chính:**
* Bổ sung trường `partyName` (string, optional) vào DTO để class-validator cho phép nhận thông tin tên đối tác/khách hàng đối với phiếu thu/chi thủ công.
* Đồng bộ mặc định trường `category` từ client gửi lên thành `"OTHER"` để khớp chính xác với Enum `FinoteCategory` ở Backend.

## 3. Cấu trúc Giao diện & Tương tác Frontend
Tệp tin sửa đổi/tạo mới:
* `create-finote-dialog.tsx`: Component Dialog Bento UI hỗ trợ đổi màu linh hoạt theo Loại phiếu (Thu/Chi).
* `finotes.tsx`: Loại bỏ các nút cũ, tích hợp `CreateFinoteDialog` để kích hoạt luồng tạo phiếu thu/chi thực tế.
* `journal-entries.tsx`: Kết nối nút bấm `"Thêm Bút toán mới"` với Dialog chứa `JournalEntryForm`, tích hợp mutation tạo bút toán thủ công và tự động refetch bảng dữ liệu sau khi thành công.