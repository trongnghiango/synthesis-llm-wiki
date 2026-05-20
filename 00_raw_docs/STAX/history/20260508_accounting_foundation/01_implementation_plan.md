# Implementation Plan: Accounting Foundation (Phase 1)

Bản kế hoạch triển khai nền tảng kế toán ghi sổ kép cho STAX ERP.

## A. Database & Schema Changes (`src/database/schema/accounting/`)

### 1. `accounts.schema.ts` [NEW]
Quản lý hệ thống tài khoản (COA).
- `id`: serial primary key.
- `organizationId`: bigint (FK -> organizations).
- `parentId`: integer (FK -> self.id) - Hỗ trợ cây tài khoản.
- `code`: varchar(20) - Mã tài khoản (VD: 111, 1121).
- `name`: varchar(255) - Tên tài khoản.
- `type`: pgEnum ('ASSET', 'LIABILITY', 'EQUITY', 'REVENUE', 'EXPENSE').
- `isSystem`: boolean - Tài khoản mặc định không được xóa.
- `isActive`: boolean - Trạng thái hoạt động.
- `path`: text - Hỗ trợ Materialized Path để truy vấn cây nhanh.

### 2. `ledger.schema.ts` [NEW]
Quản lý Nhật ký chung và Sổ cái.
- **Table `journal_entries`**:
    - `id`: serial primary key.
    - `organizationId`: bigint (FK -> organizations).
    - `transactionDate`: timestamp - Ngày hạch toán.
    - `description`: text - Diễn giải nội dung.
    - `referenceType`: varchar(50) (FINOTE, INVOICE, MANUAL).
    - `referenceId`: integer.
    - `status`: pgEnum ('DRAFT', 'POSTED', 'CANCELLED').
    - `createdBy`: integer (FK -> employees).
- **Table `journal_items`**:
    - `id`: serial primary key.
    - `journalEntryId`: integer (FK -> journal_entries.id).
    - `accountId`: integer (FK -> accounts.id).
    - `debit`: numeric(15, 2) - Số tiền Nợ.
    - `credit`: numeric(15, 2) - Số tiền Có.

---

## B. Domain Layer & Core Logic

### 1. Entities
- **Account**: Quản lý thông tin tài khoản, kiểm tra tính hợp lệ của mã code.
- **JournalEntry**: 
    - Chứa danh sách `JournalItem`.
    - **Invariants**: 
        - `validateBalance()`: Tổng Nợ - Tổng Có = 0.
        - `post()`: Chuyển trạng thái sang `POSTED` (không cho phép sửa sau khi đã Post).

### 2. Domain Exceptions
- `UnbalancedJournalEntryException`: Ném ra khi hạch toán không cân.
- `AccountNotFoundException`: Tài khoản không tồn tại.
- `SystemAccountModificationException`: Cố ý xóa tài khoản hệ thống.

---

## C. Application Layer

### 1. AccountService
- `initializeDefaultCOA(orgId)`: Khởi tạo bộ tài khoản mẫu cho công ty mới (Dựa trên Thông tư 200/133).
- `getTree(orgId)`: Lấy danh sách tài khoản dạng cây.

### 2. JournalService
- `createDraft(dto)`: Tạo bút toán nháp.
- `postEntry(id)`: Ghi sổ chính thức.
- `handleFinotePaidEvent(event)`: 
    - Lắng nghe sự kiện `FinoteStatusChangedEvent`.
    - Tự động sinh bút toán DRAFT tương ứng (Mapping tài khoản dựa trên loại Finote: Thu -> 111/112, Chi -> 642/331...).

---

## D. API Contracts

### 1. Chart of Accounts (COA)
- `GET /api/accounting/accounts`: Danh sách tài khoản.
- `POST /api/accounting/accounts`: Thêm tài khoản con.

### 2. General Ledger
- `GET /api/accounting/journal-entries`: Danh sách bút toán.
- `POST /api/accounting/journal-entries`: Tạo bút toán thủ công.
- `PATCH /api/accounting/journal-entries/:id/post`: Ghi sổ.

---
**Trạng thái**: Chờ thực hiện Bước 3 (Task List).
