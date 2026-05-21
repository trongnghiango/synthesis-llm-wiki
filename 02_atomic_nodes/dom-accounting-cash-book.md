---
id: dom-accounting-cash-book
title: Thiết kế nghiệp vụ và hạ tầng Sổ Quỹ (Cash Book)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-adr-0002-implicit-transaction-propagation]]"
  - "[[hb-drizzle-base-repo]]"
  - "[[dom-accounting-finote]]"
summary: "Đặc tả nghiệp vụ chống âm quỹ, cơ chế chuyển khoản nội bộ nguyên tử và tích hợp thanh toán hóa đơn với Sổ Quỹ."
tags: [cash-book, accounting, transaction-propagation, domain-entity, drizzle-orm]
---

### 1. Nghiệp vụ Lõi (Domain & Rules)
- **`CashFund` Entity**: Quản lý số dư bất biến. Hàm rút tiền (`withdraw`) kiểm tra số dư trực tiếp tại domain để chống âm quỹ (`BusinessRuleValidationException`).
- **Chuyển khoản nội bộ (`transferMoney`)**: Thực thi trong transaction nguyên tử sử dụng `AsyncLocalStorage` (`[[arch-adr-0002-implicit-transaction-propagation]]`). Trừ quỹ gửi, cộng quỹ nhận và tạo 2 giao dịch đối ứng `IN` / `OUT` liên kết vật lý.

### 2. Hạ tầng & Cơ sở dữ liệu (Infrastructure & Schema)
- **Repository**: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/infrastructure/persistence/drizzle-cash-fund.repository.ts` kế thừa `[[hb-drizzle-base-repo]]`. Hỗ trợ phân trang, lọc nâng cao và truy vấn quỹ mặc định của tổ chức (`orgId`).
- **Shared Contracts**: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/core/shared/contracts/accounting.ts` đồng bộ hóa Drizzle Schemas & Zod contracts sang Frontend, phục vụ hai chế độ hiển thị: *Bento Grid Dashboard* (tỉ lệ quỹ, số dư tức thời) và *Ledger Table* (nhật ký chi tiết dòng tiền).
- **Idempotent Data Repair Seeder**: Tự động vá dữ liệu cũ trong `onModuleInit` (gán `fundId` mặc định cho giao dịch cũ và tính toán lại số dư khởi điểm chính xác).

### 3. Tích hợp Hệ thống (Integration & API)
- **Controller**: `/home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/modules/accounting/infrastructure/controllers/cash-fund.controller.ts` bảo vệ nghiêm ngặt qua `@Permissions('finote:read' | 'write')` và JWT Auth.
- **Tích hợp Finote Payment**: Khi ghi nhận thanh toán (`[[dom-accounting-finote]]`), hệ thống tự động nạp tiền (nếu là `INCOME`) hoặc rút tiền (nếu là `EXPENSE`) ra khỏi Sổ Quỹ tương ứng hoặc quỹ mặc định của tổ chức.