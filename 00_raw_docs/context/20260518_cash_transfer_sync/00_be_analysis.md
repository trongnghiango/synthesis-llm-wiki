# Phân tích Nghiệp vụ & Kiến trúc: Đồng bộ chuyển tiền nội bộ (Internal Transfer Sync)

Đây là tài liệu phân tích nghiệp vụ và kiến trúc kỹ thuật cho luồng tự động đồng bộ hạch toán Nhật ký chung khi thực hiện Chuyển tiền nội bộ giữa các Sổ Quỹ (Cash Funds) trong hệ thống STAX.

---

## A. Phân loại Module & Phụ thuộc
*   **Phân lớp (Tier):** Phân hệ Kế toán (`accounting`) nằm ở **Tier 3 — Process Flow** vì nó chứa dòng chảy nghiệp vụ kế toán, dòng tiền và phụ thuộc trực tiếp vào các thực thể tổ chức (`organization`) ở Tier 2.
*   **Mối quan hệ:** Phụ thuộc vào `Organization` và `User` để cô lập dữ liệu (Multi-tenancy). Các aggregate con trong `accounting` (Sổ Quỹ - `CashFund` và Sổ Cái - `JournalEntry`) giao tiếp gián tiếp qua **Domain Event** để đảm bảo loose coupling tuyệt đối.

---

## B. Bounded Context & Ubiquitous Language

| Thuật ngữ nghiệp vụ | Thuật ngữ kỹ thuật trong code | Mô tả |
| :--- | :--- | :--- |
| **Sổ Quỹ (Tài khoản tiền)** | `CashFund` | Nơi lưu giữ tiền thực tế (Tiền mặt, Tài khoản Ngân hàng). |
| **Chuyển tiền nội bộ** | `transferMoney` | Hành động dịch chuyển tiền giữa 2 Sổ Quỹ của cùng một tổ chức. |
| **Giao dịch Sổ Quỹ** | `CashTransaction` | Nhật ký tăng giảm số dư của từng Sổ Quỹ (`IN` / `OUT`). |
| **Bút toán Nhật ký chung** | `JournalEntry` | Định khoản kế toán đối ứng Nợ/Có. |
| **Sự kiện Chuyển tiền** | `MoneyTransferredEvent` | Domain Event phát ra khi chuyển tiền thành công ở Sổ Quỹ. |
| **Bộ xử lý sự kiện** | `MoneyTransferredHandler` | Lắng nghe sự kiện để tự động sinh bút toán nháp trong Nhật ký chung. |

---

## C. Data Flow & API Design

### 1. Luồng dữ liệu (Data Flow)
```
[Frontend UI] 
      │ (POST /api/accounting/cash-funds/transfer)
      ▼
[CashFundController] 
      │ (TransferMoneyDto)
      ▼
[CashFundService.transferMoney] 
      │ (1. withdraw fromFund, 2. deposit toFund, 3. save)
      ├─► DB Write (cash_funds, cash_transactions)
      │
      ▼ (EventBus.publish)
[MoneyTransferredEvent]
      │ (Asynchronous Dispatch)
      ▼
[MoneyTransferredHandler]
      │ (Resolve Accounts: 1111 / 1121)
      ▼
[JournalService.createManualEntry]
      │ (Create DRAFT Journal Entry)
      ▼
   [DB Write] (journal_entries, journal_items)
```

### 2. Thiết kế API
*   **Endpoint chuyển tiền (Có sẵn):** `POST /api/accounting/cash-funds/transfer`
*   **Payload (Có sẵn):**
    ```json
    {
      "fromFundId": 1,
      "toFundId": 2,
      "amount": 1000000,
      "note": "Rút ngân hàng về két sắt"
    }
    ```
*   **API Bút toán Nhật ký chung (Có sẵn):** `GET /api/accounting/journal-entries` (Kế toán sẽ thấy bút toán DRAFT mới sinh tại đây).

---

## D. Sự phụ thuộc liên Module (Cross-module dependencies)
*   **Sự kiện phát ra:** `MoneyTransferredEvent` chứa các metadata nghiệp vụ (`fromFundId`, `toFundId`, `amount`, `orgId`, `note`).
*   **Giao tiếp:** `MoneyTransferredHandler` sử dụng `ICashFundRepository` và `IAccountRepository` để phân giải thực thể và tài khoản kế toán phù hợp, sau đó tương tác với `JournalService` để ghi nhận bút toán.

---

## E. Cô lập Dữ liệu (Multi-tenancy)
*   Tất cả các truy vấn dữ liệu từ Sổ Quỹ, Tài khoản kế toán đến việc ghi Bút toán đều được lọc và bọc chặt chẽ theo thuộc tính `organizationId` lấy từ JWT/Session của người dùng đăng nhập. Tuyệt đối không nhận `organizationId` tùy tiện từ query params client.

---

## F. Bảo mật & Trạng thái UI (Server-Driven UI)
*   Bút toán kế toán được sinh tự động sẽ mang trạng thái **`DRAFT` (Nháp)**.
*   Nút bấm **"Ghi sổ"** (`POSTED`) chỉ được hiển thị hoặc kích hoạt đối với người dùng có Role phù hợp (Kế toán viên hoặc Kế toán trưởng) thông qua mảng hành động được cho phép `_actions.allowed` trả về từ API.
