# Task List: Accounting Foundation (Phase 1)

## Phase 1: Foundation & Ledger

### 1. Database & Schema
- [ ] Tạo file `src/database/schema/accounting/accounts.schema.ts`.
- [ ] Tạo file `src/database/schema/accounting/ledger.schema.ts`.
- [ ] Export schema mới trong `src/database/schema/index.ts`.
- [ ] Run migration để cập nhật Database.

### 2. Domain Layer
- [ ] Định nghĩa `Account` Entity và `AccountType` Enum.
- [ ] Định nghĩa `JournalEntry` và `JournalItem` Entity.
- [ ] Viết Logic kiểm tra cân bằng (Debit/Credit) trong `JournalEntry`.

### 3. Infrastructure Layer (Repositories)
- [ ] Triển khai `DrizzleAccountRepository` (CRUD + Tree Path).
- [ ] Triển khai `DrizzleJournalRepository` (Lưu JE và JI trong cùng 1 transaction).

### 4. Application Layer
- [ ] Triển khai `AccountService`: Hỗ trợ khởi tạo COA mẫu.
- [ ] Triển khai `JournalService`:
    - Logic tạo Bút toán thủ công.
    - Logic "Post" (Chốt sổ).
- [ ] Tích hợp Event: Lắng nghe `FinoteStatusChangedEvent` để sinh Bút toán tự động.

### 5. API & Integration
- [ ] `AccountingController`: Export các Endpoint quản lý COA và Nhật ký chung.
- [ ] Đăng ký Module trong `AppModule`.

### 6. Testing & Validation
- [ ] Viết Unit Test cho Logic cân bằng bút toán.
- [ ] Kiểm tra luồng Finote -> Journal Entry (End-to-End).

---
**Trạng thái**: Sẵn sàng bắt đầu Coding.
