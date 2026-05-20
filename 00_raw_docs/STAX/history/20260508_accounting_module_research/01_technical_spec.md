# Technical Spec: Accounting Foundation Implementation

Dựa trên API Documentation từ Backend ngày 2026-05-08.

## 1. Data Contracts (Interfaces)

```typescript
export enum AccountType {
  ASSET = 'ASSET',
  LIABILITY = 'LIABILITY',
  EQUITY = 'EQUITY',
  REVENUE = 'REVENUE',
  EXPENSE = 'EXPENSE'
}

export enum JournalEntryStatus {
  DRAFT = 'DRAFT',
  POSTED = 'POSTED',
  CANCELLED = 'CANCELLED'
}

export interface Account {
  id: number;
  code: string;
  name: string;
  type: AccountType;
  parentId: number | null;
  path: string;
  isSystem: boolean;
  isActive: boolean;
}

export interface JournalEntry {
  id: number;
  description: string;
  transactionDate: string;
  status: JournalEntryStatus;
  items: JournalEntryItem[];
}
```

## 2. API Services Layer
- **Endpoint mapping**:
    - `GET /api/accounting/accounts`
    - `POST /api/accounting/accounts`
    - `POST /api/accounting/journal-entries`
    - `PATCH /api/accounting/journal-entries/:id/post`

## 3. UI Key Features
- **Account Tree Navigation**: Tái sử dụng logic Tree từ Org Structure.
- **Double-Entry Form**: Form nhập liệu Nợ/Có đối xứng, validate "Balance" tại Client-side trước khi submit.
- **Finote Sync Indicator**: Hiển thị nguồn gốc của bút toán (nếu sinh ra từ Phiếu thu/chi).
