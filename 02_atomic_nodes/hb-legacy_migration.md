---
id: hb-legacy_migration
title: Cẩm nang Di cư Dữ liệu CRM cũ sang STAX
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[dom-accounting-finote]]"
summary: "Quy trình thiết kế di cư dữ liệu legacy CRM sang STAX sử dụng mô hình Hybrid Storage JSONB và giải quyết các xung đột Schema/ORM."
tags: [data-migration, hybrid-storage, jsonb, drizzle-orm, crm]
---

# Thiết kế Di cư Legacy CRM -> STAX

## 1. Pipeline di cư (Ràng buộc Khóa ngoại)
Luồng dữ liệu bắt buộc đảm bảo toàn vẹn tham chiếu:
`Employees` (HR) -> `Organizations` + `Contacts` (Clients) -> `Leads` -> `Contracts` (tổng hợp từ Metadata) -> `Finotes` + `FinoteItems`.

## 2. Kiến trúc Hybrid Storage (JSONB)
Tránh ô nhiễm schema quan hệ chính bằng cách lưu thông tin phi cấu trúc legacy vào cột `metadata JSONB`:
- `organizations.metadata`: Lưu `contractNo`, `feeType`, `expectedFee`, `suspendDeadline`, `serviceDesc`, `original_status`.
- `contacts.metadata`: Lưu `legal_representative`.
- `leads.metadata`: Lưu `legacy_date`, `original_status`, `original_consultant`, `raw_phone`.
- `contracts.metadata`: Lưu `legacy_sign_date`, `source`, `suspend_deadline`.

## 3. Khắc phục lỗi Drizzle ORM & TypeScript
*   **Ép kiểu dữ liệu JSONB:** Tránh lỗi `TS2339 (unknown)` bằng cách ép kiểu tường minh:
    ```typescript
    const meta = org.metadata as { contractNo?: string; expectedFee?: string };
    const orgId = org.id as number;
    ```
*   **Xử lý định dạng & làm sạch:**
    *   *Số điện thoại:* Chuẩn hóa bằng regex `phone.replace(/[^0-9]/g, '')`.
    *   *Số tiền thực tế:* Strip dấu phân cách hàng nghìn tiếng Việt trước khi parse.
    *   *Ngày tháng:* Parse chuỗi `DD/MM/YYYY` thủ công sang ISO `YYYY-MM-DD`.
*   **Group Multi-item (Finotes):** Gom nhóm dòng CSV theo mã phiếu `FN code` trước khi insert: 1 `finote` cha (Header) ứng với mảng `finote_items` con. Loại bỏ các item có `total <= 0`.
*   **Khớp nhân viên (Consultant):** Sử dụng cơ chế mapping 3 bước: Trùng full name -> Trùng nickname trong metadata -> Trùng họ tên cuối.

## 4. Runbook Production
1. **Schema Update:** `NODE_ENV=production npx drizzle-kit push` (Thêm cột `metadata` JSONB nếu thiếu).
2. **Dọn dẹp:** Tắt auto-seed, backup database đích bằng `pg_dump`.
3. **Thứ tự thực thi:** Chạy lần lượt các migration script tương ứng với Pipeline tại mục 1. Xử lý lỗi trùng lặp `contacts.email` qua `try/catch` độc lập để tránh rollback toàn bộ batch.