---
id: dom-accounting-foundation
title: Nền tảng Kế toán Sổ kép STAX
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Thiết lập hệ thống kế toán kép (COA, Journal Entries, Ledger) và cơ chế tự động hóa bút toán từ Finote."
tags: [accounting, double-entry, coa, ledger, journal-entry]
---

### 1. Cấu trúc Database (Drizzle Schema)
- `accounts`: Cây danh mục tài khoản (COA), sử dụng `parentId` kết hợp Materialized Path để truy vấn phả hệ nhanh.
- `journal_entries` & `journal_items`: Lưu trữ bút toán Nhật ký chung và Sổ cái, thiết lập quan hệ 1-N đảm bảo nguyên tắc sổ kép.

### 2. Ràng buộc Nghiệp vụ (Domain Invariants)
- **Quy tắc ghi sổ**: Một `JournalEntry` hợp lệ phải chứa $\ge 2$ dòng định khoản `JournalItem`.
- **Nguyên tắc cân bằng**: Tổng Nợ (Total Debit) phải bằng Tổng Có (Total Credit).
- **Vòng đời trạng thái**: Chuyển đổi tuyến tính `DRAFT` $\rightarrow$ `POSTED`. Cấm tuyệt đối chỉnh sửa dữ liệu sau khi đã ghi sổ (`POSTED`).

### 3. API Contracts
- `GET /api/accounting/accounts`: Lấy danh sách cây tài khoản hệ thống.
- `POST /api/accounting/accounts/initialize`: Khởi tạo nhanh bộ dữ liệu COA mẫu theo Thông tư 133/200.
- `POST /api/accounting/journal-entries`: Khởi tạo bút toán thủ công dạng `DRAFT`.
- `PATCH /api/accounting/journal-entries/:id/post`: Xác thực ràng buộc và tiến hành ghi sổ chính thức.

### 4. Tích hợp Hệ thống
- Lắng nghe `PaymentAllocatedEvent` từ module `[[dom-accounting-finote]]`.
- Khi trạng thái Finote chuyển dịch thành `PAID` $\rightarrow$ Tự động kích hoạt `JournalService` sinh bút toán `DRAFT` đối ứng để kế toán duyệt.