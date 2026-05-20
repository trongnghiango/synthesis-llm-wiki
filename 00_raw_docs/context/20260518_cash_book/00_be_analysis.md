# Phân tích Nghiệp vụ & Kiến trúc Backend: Cash Book (Sổ Quỹ)

**Context Check:** Tính năng này được khởi tạo dựa trên Decision Log từ phiên tư vấn `@stax-think`. Mục tiêu là tách bạch dòng tiền thành các `CashFund` riêng biệt để đối soát và cung cấp API phục vụ giao diện Dual View (Modern Bento Grid + Classic Table) cho Kế toán và Giám đốc.

## A. Phân loại Module
- **Tier:** Tier 3 — Process Flow (Thuộc nhánh Accounting Module).
- **Tính chất:** Quản lý dòng tiền thực tế chạy trong tổ chức.
- **Phụ thuộc:** Phụ thuộc vào Tier 1 (AuditLog) và Tier 2 (Organization, Employee). Các module khác (như Finote Payment) sẽ bắt đầu phụ thuộc vào CashFund để lưu `fundId`.

## B. Bounded Context & Ubiquitous Language
- **Domain:** Accounting / Treasury Management
- **Thực thể (Entities):**
  - `CashFund` (Sổ quỹ/Ví tiền): Nơi lưu trữ tiền thực tế (VD: Tiền mặt, TK Vietcombank).
  - `CashTransaction` (Giao dịch dòng tiền): Mọi luồng tiền IN/OUT phải map vào 1 `fundId`.
- **Nghiệp vụ cốt lõi:** Quản lý số dư, chuyển tiền nội bộ (Transfer).

## C. Data Flow & API Design
*Client → Controller (CashFundController) → Use Case (CashFundService) → Domain (CashFund) → Repository → DB*

**APIs dự kiến:**
1. `GET /api/accounting/cash-funds`: Lấy danh sách ví kèm balance hiện tại. (Permission: `finote:read`)
2. `GET /api/accounting/cash-transactions`: Lấy biến động dòng tiền (của 1 ví hoặc tất cả). (Permission: `finote:read`)
3. `POST /api/accounting/cash-funds`: Tạo ví/quỹ mới. (Permission: `finote:approve`)
4. `POST /api/accounting/cash-funds/transfer`: Chuyển tiền nội bộ (VD: Ngân hàng -> Két sắt). (Permission: `finote:approve`)

## D. Cross-module dependencies
- `FinotePaymentService`: Hiện tại đang tạo `CashTransaction` nhưng chưa truyền `fundId`. Sẽ phải gọi Port của `ICashFundRepository` để lấy Quỹ mặc định, hoặc bắt UI chọn quỹ khi ghi nhận thanh toán.
- **Domain Event:**
  - `CashTransferredEvent` (Khi chuyển tiền nội bộ).
  - `CashFundCreatedEvent`.

## E. Multi-tenancy
- Lọc triệt để theo `organizationId` lấy từ JWT context. KHÔNG truyền `orgId` từ URL.
- Quỹ của công ty A tuyệt đối không được rò rỉ sang công ty B.

## F. Security & Server-Driven UI
- Bảng `cash_funds` sẽ chứa các hành động (`_actions`): `edit`, `deactivate`, `transfer`.
- Các hành động này chỉ `allowed` khi `canManage` (có quyền Quản lý/Kế toán) là `true`.
- Các quỹ mặc định (`isDefault = true`) có thể không được phép `deactivate`.
