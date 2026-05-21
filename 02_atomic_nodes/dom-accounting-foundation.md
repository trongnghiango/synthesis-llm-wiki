---
id: dom-accounting-foundation
title: Nền tảng Kế toán Kép STAX
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
  - "[[hb-drizzle-base-repo]]"
summary: "Thiết kế hệ thống kế toán kép (Double-entry) gồm COA, Journal Entries, và tích hợp tự động hóa từ sự kiện Finote."
tags: [accounting, double-entry, coa, schema, journal-entry, integration]
---

### 1. Cấu trúc Cơ sở dữ liệu (Drizzle ORM)
*   **`accounts`**: Hệ thống tài khoản (COA). Hỗ trợ cấu trúc hình cây qua `parentId` và truy vấn nhanh bằng cơ chế *Materialized Path*.
*   **`journal_entries` & `journal_items`**: Lưu trữ bút toán nhật ký và chi tiết định khoản, đảm bảo tính toàn vẹn của sổ kép.

### 2. Ràng buộc Nghiệp vụ (Domain Invariants)
*   **Account Entity**: Định nghĩa loại tài khoản và tính chất số dư (Debit/Credit).
*   **JournalEntry Entity**: Kiểm soát quy trình Ghi sổ (Post). Ràng buộc nghiêm ngặt:
    *   Một bút toán phải có tối thiểu 2 dòng định khoản (`journal_items`).
    *   Phương trình kế toán bắt buộc: $\sum \text{Debit} = \sum \text{Credit}$.
    *   Chỉ cho phép chuyển trạng thái sang `POSTED` khi thỏa mãn các điều kiện trên.

### 3. Tích hợp Hệ thống (Integration)
*   **Khởi tạo**: `AccountService` hỗ trợ sinh tự động cây COA mẫu theo Thông tư 133/200.
*   **Tự động hóa**: Lắng nghe `PaymentAllocatedEvent` từ `[[dom-accounting-finote]]`. Khi Finote chuyển trạng thái sang `PAID`, hệ thống tự sinh bút toán `DRAFT` tương ứng.

### 4. API Contracts
*   `GET /api/accounting/accounts` - Lấy danh sách cây tài khoản hệ thống.
*   `POST /api/accounting/accounts/initialize` - Khởi tạo dữ liệu COA mẫu.
*   `POST /api/accounting/journal-entries` - Tạo bút toán thủ công (trạng thái `DRAFT`).
*   `PATCH /api/accounting/journal-entries/:id/post` - Kiểm tra và ghi sổ chính thức (chuyển sang `POSTED`).