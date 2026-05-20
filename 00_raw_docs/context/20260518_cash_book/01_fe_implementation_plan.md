# STAX Sổ Quỹ (Cash Book) — Frontend Implementation Plan (Bước 2️⃣)

- **Date:** 2026-05-18
- **Workflow Phase:** Bước 2️⃣: Kế hoạch Kiến trúc FE

---

## A. Contract Sync (Đồng bộ Giao kèo)

Chúng ta sử dụng các contracts đã được khai báo vững chắc tại `backend/src/core/shared/contracts/accounting.ts` mà không định nghĩa lại:

1.  **`CashFund` Entity Schema & Types:**
    *   `CashFundData` (Infer từ Zod Schema): `id`, `name`, `type` (`CASH`/`BANK`), `accountNumber`, `currentBalance`, `isDefault`, `organizationId`, `_actions`.
2.  **DTOs Schemas:**
    *   `CreateCashFundSchema` -> `CreateCashFundData` (`name`, `type`, `accountNumber`).
    *   `TransferMoneySchema` -> `TransferMoneyData` (`fromFundId`, `toFundId`, `amount`, `note`).
    *   `RecordFinotePaymentSchema` -> `RecordFinotePaymentInput` (Đã được bổ sung `fundId` optional).

---

## B. API Client (Tích hợp React Query)

Chúng ta sẽ mở rộng `frontend/client/src/modules/accounting/api/accounting.api.ts` với các Query Keys và các lời gọi API tương ứng:

### 1. Bổ sung Query Keys:
```typescript
export const accountingQueryKeys = {
  // ... keys cũ
  cashFunds: ["accounting", "cash-funds"] as const,
  cashTransactions: (params?: Record<string, any>) => ["accounting", "cash-funds", "transactions", params] as const,
};
```

### 2. Bổ sung API Methods:
*   `getCashFunds()` -> `GET /accounting/cash-funds`
*   `createCashFund(data: CreateCashFundData)` -> `POST /accounting/cash-funds`
*   `setDefaultCashFund(id: number)` -> `POST /accounting/cash-funds/${id}/default`
*   `transferMoney(data: TransferMoneyData)` -> `POST /accounting/cash-funds/transfer`
*   `getCashTransactions(params?: Record<string, any>)` -> `GET /accounting/cash-funds/transactions`

---

## C. Component Tree (Cây Thành phần UI)

Cấu trúc thư mục UI sẽ tuân thủ nghiêm ngặt ranh giới domain của STAX:

```text
frontend/client/src/
├── pages/admin/accounting/
│   ├── cash-book.tsx                 <-- [NEW] Trang Sổ quỹ chính (Tabs Modern & Classic)
│   └── components/
│       ├── record-payment-dialog.tsx <-- [MODIFY] Tích hợp Combobox chọn Sổ quỹ
│       ├── create-fund-dialog.tsx    <-- [NEW] Form tạo quỹ mới
│       └── transfer-money-dialog.tsx <-- [NEW] Form chuyển tiền nội bộ (có validation số dư)
```

### 1. `CashBookPage` (Trang chính):
*   **Header:** Tiêu đề "Sổ Quỹ (Cash Book)" + Badge tổng số dư. Cung cấp các nút Action: "Chuyển tiền nội bộ", "Tạo quỹ mới".
*   **Tabs Switcher:**
    *   `Tab Modern`: Chứa Bento Grid đẹp mắt:
        *   Tổng quan số dư dưới dạng biểu đồ tròn tỉ lệ.
        *   Danh sách quỹ dạng Card (Thẻ tín dụng tối giản) có các nút nhanh: "Đặt mặc định" (nếu chưa mặc định), hiển thị Badge `Mặc định` lấp lánh cho quỹ active.
    *   `Tab Classic`: Chứa bảng Sổ Nhật ký dòng tiền (`DataGrid`):
        *   Bộ lọc: Chọn quỹ (Combobox), Khoảng ngày (DateRangePicker).
        *   Bảng dòng tiền hiển thị: Ngày, Sổ quỹ, Loại (`IN`/`OUT`), Mã GD/Ghi chú, Số tiền, và **Số dư lũy tiến (Running Balance)**.
        *   Hỗ trợ phân trang mượt mà.

### 2. `RecordPaymentDialog` (Tích hợp thêm Sổ quỹ):
*   Khi nhân viên kế toán thực hiện thanh toán Hóa đơn (Finote), một ô Combobox **"Sổ quỹ thanh toán"** sẽ hiển thị.
*   Tự động tải danh sách Sổ quỹ qua hook `useCashFunds()`, hiển thị gợi ý quỹ mặc định lên đầu.

### 3. `TransferMoneyDialog` (Chuyển tiền nội bộ):
*   Dropdown chọn Quỹ gửi (`fromFundId`) và Quỹ nhận (`toFundId`).
*   Ô nhập số tiền chuyển (`amount`) được validate thời gian thực: số tiền chuyển không được phép lớn hơn số dư hiện có của Quỹ gửi đã chọn.

### 4. `CreateFundDialog` (Tạo Sổ quỹ):
*   Form đơn giản nhập tên Sổ quỹ, loại (`CASH` hoặc `BANK`). Nếu chọn `BANK`, hiển thị thêm ô nhập số tài khoản ngân hàng (`accountNumber`).

---

## D. State Management (Quản lý Trạng thái & Cache)

*   Sử dụng `@tanstack/react-query` làm "Source of Truth" cho toàn bộ dữ liệu dòng tiền.
*   **Chiến lược Invalidation (Xóa cache thông minh):**
    *   Khi tạo quỹ thành công -> Invalidate `cashFunds`.
    *   Khi thiết lập quỹ mặc định thành công -> Invalidate `cashFunds`.
    *   Khi chuyển tiền nội bộ thành công -> Invalidate `cashFunds` và `cashTransactions`.
    *   Khi ghi nhận thanh toán Finote thành công -> Invalidate `finotes`, `cashFunds`, và `cashTransactions`.

---

Thiết kế này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
