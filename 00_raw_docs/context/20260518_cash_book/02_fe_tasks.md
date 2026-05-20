# STAX Sổ Quỹ (Cash Book) — Frontend Tasks Checklist (Bước 3️⃣)

- **Date:** 2026-05-18
- **Workflow Phase:** Bước 3️⃣: Checklist Thực thi (HOÀN THÀNH 100%)

---

## 📋 FE Checklist Thực thi

### 1. Đồng bộ Giao kèo & API Client (Contracts & Client Layer)
- [x] Cập nhật `frontend/client/src/modules/accounting/api/accounting.api.ts`:
  - [x] Bổ sung `cashFunds` và `cashTransactions` vào `accountingQueryKeys`.
  - [x] Thêm method `getCashFunds` (`GET /accounting/cash-funds`).
  - [x] Thêm method `createCashFund` (`POST /accounting/cash-funds`).
  - [x] Thêm method `setDefaultCashFund` (`POST /accounting/cash-funds/:id/default`).
  - [x] Thêm method `transferMoney` (`POST /accounting/cash-funds/transfer`).
  - [x] Thêm method `getCashTransactions` (`GET /accounting/cash-funds/transactions`).

### 2. Tích hợp Dialog Ghi nhận Thanh toán (Record Payment Dialog Integration)
- [x] Chỉnh sửa `frontend/client/src/pages/admin/accounting/components/record-payment-dialog.tsx`:
  - [x] Import `useQuery` và gọi `accountingApi.getCashFunds` để lấy danh sách Sổ quỹ.
  - [x] Bọc form bằng Zod resolver tương ứng (đã bổ sung `fundId` optional).
  - [x] Thêm FormField `fundId` dạng `Select` để chọn Sổ quỹ. Tự động hiển thị Sổ quỹ mặc định (`isDefault = true`) làm tùy chọn mặc định hoặc gợi ý nổi bật ở đầu danh sách.

### 3. Xây dựng các Dialog Nghiệp vụ Sổ Quỹ (Cash Book Dialogs)
- [x] Tạo file `frontend/client/src/pages/admin/accounting/components/create-fund-dialog.tsx`:
  - [x] Form sử dụng `react-hook-form` + `zodResolver` của Zod contract.
  - [x] Input: Tên quỹ (`name`), Loại quỹ (`type` - `CASH`/`BANK`).
  - [x] Hiển thị động ô nhập số tài khoản (`accountNumber`) chỉ khi chọn loại `BANK`.
  - [x] Tích hợp mutation `createCashFund` + Toast thông báo + Invalidate `cashFunds`.
- [x] Tạo file `frontend/client/src/pages/admin/accounting/components/transfer-money-dialog.tsx`:
  - [x] Form chuyển khoản nội bộ. Dropdown chọn quỹ gửi (`fromFundId`) và quỹ nhận (`toFundId`).
  - [x] Ô nhập số tiền (`amount`), validate: `amount > 0` và `amount <= currentBalance` của quỹ gửi được chọn.
  - [x] Tích hợp mutation `transferMoney` + Toast thông báo + Invalidate cả `cashFunds` và `cashTransactions`.

### 4. Xây dựng Trang Sổ Quỹ chính (Main Cash Book Page)
- [x] Tạo file `frontend/client/src/pages/admin/accounting/cash-book.tsx`:
  - [x] Thiết kế Header với badge tổng tiền và 2 nút Action nhanh mở dialog.
  - [x] Cấu trúc Tabs:
    - [x] **Modern Tab (Bento Grid):**
      - [x] Biểu đồ Donut hoặc thanh phần trăm trực quan hóa cơ cấu phân bổ quỹ.
      - [x] Danh sách Card Quỹ (Glassmorphism layout) với số dư, số tài khoản, các action nhanh như `Đặt mặc định` (chỉ hiển thị nếu quỹ chưa mặc định và `canManage` = true).
    - [x] **Classic Tab (Ledger Book):**
      - [x] Bộ lọc `fundId` (Select), `startDate` và `endDate` (Date Range Picker).
      - [x] Bảng giao dịch dòng tiền sử dụng `DataGrid` cuộn ngang an toàn trên Mobile.
      - [x] Hiển thị cột số dư lũy tiến (running balance) và định dạng tiền tệ chuyên nghiệp.

### 5. Đăng ký Route & Sidebar (Navigation & Routing)
- [x] Cập nhật `frontend/client/src/app/router/routes/accounting-routes.tsx`:
  - [x] Thêm route `cashBookRoute` trỏ tới `pages/admin/accounting/cash-book.tsx`.
- [x] Cập nhật `frontend/client/src/app/router/index.tsx`:
  - [x] Đăng ký `cashBookRoute` vào danh sách routes con của `adminRoute`.
- [x] Cập nhật `frontend/client/src/config/admin-menu.ts`:
  - [x] Thêm mục "Sổ Quỹ (Cash Book)" vào danh sách con của "Accounting".

### 6. Kiểm định & Đóng gói (Testing & Validation)
- [x] Kiểm tra lỗi biên dịch TypeScript toàn dự án (`npm run check` hoặc `pnpm build` ở FE).
- [x] Xác nhận giao diện co giãn hoàn hảo (Responsive) trên Mobile và Desktop.
- [x] Đảm bảo không có lỗi render hay cảnh báo console rác.
