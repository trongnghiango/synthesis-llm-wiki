---
id: dom-accounting-foundation
title: Nền tảng Kế toán Kép STAX
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
  - "[[hb-drizzle-base-repo]]"
summary: "Thiết kế hệ thống kế toán kép ERP STAX hỗ trợ quản lý cây tài khoản hệ thống (COA) và hạch toán tự động từ sự kiện Finote."
tags: [accounting, double-entry, coa, journal-entry, integration]
---

### 1. Cấu trúc Database Schema (Drizzle)
- `accounts`: Quản lý danh mục tài khoản (COA), sử dụng cấu trúc cây qua `parentId` và cơ chế truy vấn Materialized Path.
- `journal_entries`: Đầu mục bút toán kế toán (Trạng thái: `DRAFT`, `POSTED`).
- `journal_items`: Chi tiết dòng định khoản Nợ (Debit) / Có (Credit) liên kết chặt chẽ với `journal_entries`.

### 2. Ràng buộc Nghiệp vụ (Domain Invariants)
- **Quy tắc số kép**: Một bút toán (`JournalEntry`) phải có tối thiểu 2 dòng định khoản (`JournalItem`).
- **Ràng buộc cân bằng**: Bút toán chỉ được phép chuyển sang trạng thái `POSTED` khi và chỉ khi $\sum \text{Debit} = \sum \text{Credit}$.
- **Tính bất biến (Immutability)**: Bút toán đã ghi sổ (`POSTED`) nghiêm cấm mọi hành vi chỉnh sửa hoặc xóa trực tiếp.

### 3. API Contracts
- `GET /api/accounting/accounts`: Truy xuất toàn bộ cây tài khoản (COA).
- `POST /api/accounting/accounts/initialize`: Khởi tạo dữ liệu tài khoản mẫu (Thông tư 133/200).
- `POST /api/accounting/journal-entries`: Tạo mới bút toán thủ công (mặc định `DRAFT`).
- `PATCH /api/accounting/journal-entries/:id/post`: Thực hiện phê duyệt và ghi sổ chính thức.

### 4. Tích hợp Hệ thống
- Tích hợp lỏng thông qua Event-driven: Lắng nghe `PaymentAllocatedEvent` từ module `[[dom-accounting-finote]]`.
- Tự động tạo bút toán `DRAFT` tương ứng khi một thực thể Finote chuyển đổi trạng thái thành hoàn thành (`PAID`).