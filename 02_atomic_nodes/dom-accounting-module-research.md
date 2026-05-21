---
id: dom-accounting-module-research
title: Phân hệ Kế toán Phase 1
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Đặc tả nghiệp vụ và kiến trúc kỹ thuật phân hệ Kế toán Phase 1: Hệ thống tài khoản, Nhật ký chung và tích hợp Lead-to-Contract-to-Finote."
tags: [accounting, chart-of-accounts, general-ledger, finote, lead-to-contract]
---

## 1. Nghiệp vụ & Thiết kế Luồng Dữ liệu
- **Hệ thống tài khoản (COA):** Cấu trúc cây phân tầng (Hierarchy). Phân loại chuẩn: `ASSET`, `LIABILITY`, `EQUITY`, `REVENUE`, `EXPENSE`. Hỗ trợ cơ chế seeding mẫu tài khoản theo Thông tư 200/133.
- **Nhật ký chung (GL):** Cơ chế bút toán kép (Double-entry).
  - Trạng thái: `Draft` (Nháp) và `Posted` (Đã ghi sổ).
  - **Ràng buộc cứng (Validation Constraint):** Hệ thống chỉ cho phép ghi sổ (`Posted`) khi tổng Nợ (Debit) = tổng Có (Credit). Ngăn chặn lưu lệch số liệu ở tầng Client và Server.
- **Tích hợp Lead-to-Contract-to-Finote:**
  - **Luồng đi:** Lead (Chốt) $\rightarrow$ Hợp đồng (Contract) $\rightarrow$ Tự động sinh đề xuất Phiếu thu (`[[dom-accounting-finote]]`) đợt 1.
  - **Dữ liệu kế thừa:** Trích xuất tự động `Amount`, `Content` từ Báo giá (`Quote`) và liên kết trực tiếp với `Contract ID` để đối soát dòng tiền.

## 2. Cấu trúc API & Frontend Routing
- **API Contracts (`accounting.api.ts`):**
  - `GET /api/v1/accounting/accounts/tree`: Lấy danh sách tài khoản dạng cây.
  - `POST /api/v1/accounting/accounts/seed`: Khởi tạo nhanh bộ tài khoản chuẩn (TT200/TT133).
  - `POST /api/v1/accounting/journal-entries`: Tạo mới/Cập nhật bút toán kép.
  - `POST /api/v1/accounting/journal-entries/{id}/post`: Chuyển trạng thái sang `Posted` (yêu cầu validate balance).
- **Routing & State (`accounting-routes.tsx`):**
  - Khai báo route modular hóa bằng **TanStack Router**.
  - Sử dụng **Zustand Persist** để ghi nhớ trạng thái bộ lọc và tab làm việc cuối cùng của Kế toán viên.