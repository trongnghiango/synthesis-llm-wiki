# Task List — UI Components Standardization

> Trạng thái: Completed
> Context: Phase 3 - Xây dựng hệ thống UI chuẩn.

### 1. Thành phần Nền tảng (Foundation)
- [x] Tạo `client/src/components/common/PageHeader.tsx`.
- [x] Tạo `client/src/components/common/StatsCard.tsx`.
- [x] Tạo `client/src/components/common/EmptyState.tsx`.

### 2. Thành phần Dữ liệu (Data Components)
- [x] Tạo `client/src/components/common/DataGrid.tsx` (Bọc xung quanh Shadcn Table).
- [x] Tạo `client/src/components/common/LoadingScreen.tsx`.

### 3. Di trú & Refactor (Migration)
- [x] Refactor `Dashboard` (sử dụng StatsCard chuẩn).
- [x] Refactor `Leads` (sử dụng DataGrid và PageHeader).
- [x] Refactor `Contracts` (sử dụng DataGrid và PageHeader).
- [x] Refactor `Clients` (sử dụng DataGrid và PageHeader).
- [x] Refactor `LeadDetail` (sử dụng PageHeader chuẩn).
- [x] Refactor `ContractDetail` (sử dụng PageHeader chuẩn).

### 4. Hoàn thiện (Polishing)
- [x] Thêm hiệu ứng Framer Motion cho Page Transitions.
- [x] Kiểm tra Responsive trên Mobile/Tablet.
- [x] Nâng cấp `PageHeader` hỗ trợ Detail Pages (Back button, Badge).
