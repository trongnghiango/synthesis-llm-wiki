---
id: dom-accounting-module-research
title: Thiết kế Phân hệ Kế toán STAX Phase 1
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Thiết kế nghiệp vụ Phân hệ Kế toán STAX gồm Chart of Accounts, General Ledger, và luồng tích hợp Lead-Contract-Finote."
tags: [accounting, general-ledger, double-entry, finote, lead-to-contract]
---
### 1. Kiến trúc Nghiệp vụ & Luồng Dữ liệu
- **Hệ thống tài khoản (CoA):** Tổ chức dạng cây phân cấp (Hierarchy). Khởi tạo nhanh theo Thông tư 200/133. Phân loại theo loại tài khoản: `ASSET`, `LIABILITY`, `EQUITY`, `REVENUE`, `EXPENSE`.
- **Nhật ký chung (GL):** Cơ chế bút toán kép (Double-entry ledger).
  - Trạng thái: `Draft` (Nháp) và `Posted` (Đã ghi sổ - Khóa sửa/xóa).
  - Ràng buộc cân đối (Balance Scale): Kiểm tra tổng Nợ (Debit) = Tổng Có (Credit) trước khi lưu. Ngăn chặn ghi sổ nếu lệch balance.
- **Tích hợp Lead-to-Contract-to-Finote:**
  - Luồng: `Lead` -> `Contract` -> Kích hoạt tạo tự động `Finote` (Phiếu thu `[[dom-accounting-finote]]`).
  - Thừa kế dữ liệu: Tự động map giá trị từ Báo giá (`Quote`) sang `Finote` và liên kết trực tiếp `Contract ID` để truy vết dòng tiền.

### 2. Thiết kế Kỹ thuật & API
- **API Modular (`accounting.api.ts`):** Quản lý endpoints độc lập cho CoA, GL Transactions, và Finote Integration.
- **Routing & State:**
  - Định tuyến tập trung qua TanStack Router (`accounting-routes.tsx`).
  - Trạng thái UI (Bento stats, GL active form) quản lý qua Zustand kết hợp Persistence nhằm tối ưu UX.
- **DB Schema Design:** Yêu cầu các bảng `accounting_accounts` (self-referencing parent_id), `accounting_journal_entries`, `accounting_journal_lines` (nhiều dòng Nợ/Có, liên kết khóa ngoại với `contracts` và `finotes`).