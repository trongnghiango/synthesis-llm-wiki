# Kế hoạch Kiến trúc Chi tiết Backend: Cash Book (Sổ Quỹ)

## A. Database Schema (Drizzle ORM)

### 1. Tạo bảng `cash_funds`
- File mới: [cash-funds.schema.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/backend/src/database/schema/accounting/cash-funds.schema.ts)
```typescript
import { pgTable, serial, varchar, numeric, timestamp, boolean, pgEnum, bigint, index } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { organizations } from '../crm/organizations.schema';
import { cashTransactions } from './finotes.schema';

export const cashFundTypeEnum = pgEnum('cash_fund_type', ['CASH', 'BANK', 'E_WALLET']);

export const cashFunds = pgTable('cash_funds', {
    id: serial('id').primaryKey(),
    organizationId: bigint('organization_id', { mode: 'number' })
        .notNull()
        .references(() => organizations.id, { onDelete: 'cascade' }),
    name: varchar('name', { length: 255 }).notNull(),
    type: cashFundTypeEnum('type').default('CASH').notNull(),
    accountNumber: varchar('account_number', { length: 100 }),
    currentBalance: numeric('current_balance', { precision: 15, scale: 2 }).default('0').notNull(),
    isDefault: boolean('is_default').default(false).notNull(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
    updatedAt: timestamp('updated_at').defaultNow().notNull(),
}, (table) => ({
    org_idx: index('idx_cash_funds_org').on(table.organizationId),
}));

export const cashFundsRelations = relations(cashFunds, ({ one, many }) => ({
    organization: one(organizations, { fields: [cashFunds.organizationId], references: [organizations.id] }),
    transactions: many(cashTransactions),
}));
```

### 2. Sửa đổi bảng `cash_transactions` trong `finotes.schema.ts`
- Thêm trường:
```typescript
    fundId: integer('fund_id').references(() => cashFunds.id, { onDelete: 'set null' }),
```
- Thêm relations:
```typescript
export const cashTransactionsRelations = relations(cashTransactions, ({ one, many }) => ({
    mappings: many(finotePayments),
    fund: one(cashFunds, { fields: [cashTransactions.fundId], references: [cashFunds.id] }),
}));
```

### 3. Đăng ký Schema vào `src/database/schema/index.ts`
```typescript
export * from './accounting/cash-funds.schema';
```

## B. Domain Layer

### 1. Thực thể `CashFund` (Domain Entity)
- File mới: `src/modules/accounting/domain/entities/cash-fund.entity.ts`
- Chứa các nghiệp vụ:
  - `deposit(amount: Money)`: Nạp tiền vào quỹ.
  - `withdraw(amount: Money)`: Rút tiền khỏi quỹ (nếu là rút lố thì kiểm tra âm quỹ tùy nghiệp vụ).
  - `setDefault()`: Đặt làm mặc định.

### 2. Port: `ICashFundRepository`
- File mới: `src/modules/accounting/domain/repositories/cash-fund.repository.ts`
```typescript
export const ICashFundRepository = Symbol('ICashFundRepository');
export interface ICashFundRepository {
    findById(id: number, orgId: number): Promise<CashFund | null>;
    findDefault(orgId: number): Promise<CashFund | null>;
    findAll(orgId: number): Promise<CashFund[]>;
    save(fund: CashFund, tx?: any): Promise<CashFund>;
}
```

## C. Infrastructure Layer

### 1. Mapper `CashFundMapper`
- Chuyển đổi giữa `CashFund` Domain Entity và Drizzle Record.

### 2. Drizzle Repository `DrizzleCashFundRepository`
- Implement `ICashFundRepository`.

## D. Application Layer (`CashFundService`)
- File mới: `src/modules/accounting/application/services/cash-fund.service.ts`
- Các Use Cases:
  - `createFund(dto: CreateFundDto, orgId: number)`
  - `getFunds(orgId: number)`: Trả về danh sách quỹ kèm `_actions`.
  - `transferMoney(dto: TransferMoneyDto, orgId: number)`:
    - Bọc trong `txManager.runInTransaction`.
    - Rút tiền từ `fromFundId`, cộng tiền vào `toFundId`.
    - Tạo 2 bản ghi `cash_transactions` (1 giao dịch OUT cho quỹ nguồn, 1 giao dịch IN cho quỹ đích).
    - Commit.

## E. Presentation Layer (HTTP / Contracts / DTOs)

### 1. Shared Contracts
- Thêm Zod schemas vào `@shared/contracts/accounting`:
  - `CreateCashFundSchema`, `TransferCashFundSchema`, `CashFundResponseSchema`.

### 2. Controllers & DTOs
- `CashFundController`:
  - `GET /api/accounting/cash-funds`
  - `POST /api/accounting/cash-funds`
  - `POST /api/accounting/cash-funds/transfer`
- `CashTransactionController` (hoặc tích hợp vào `FinoteController`):
  - `GET /api/accounting/cash-transactions`: Trả về toàn bộ giao dịch dòng tiền kèm filter và phân trang.

## F. Module Wiring & Migration
- Khởi tạo 1 Seeder hoặc Migration script để tự động tạo `CashFund` mặc định (ví dụ: "Tiền mặt") cho các Organization hiện có, đồng thời link toàn bộ `cash_transactions` lịch sử vào quỹ này.

---
Vui lòng gõ **'OK'** để tôi tiến hành xuất Checklist thực thi chi tiết.
