# Implementation Plan — UI Components Standardization (Phase 3)

Chuẩn hóa hệ thống giao diện (UI System) để đảm bảo tính đồng nhất, thẩm mỹ cao cấp và tốc độ phát triển cho toàn bộ dự án.

## 1. Tại sao cần thực hiện Phase này? (Rationale)

- **Tính đồng nhất (Consistency)**: Hiện tại các trang như Dashboard, Leads, Settings đang sử dụng các cách tổ chức UI khác nhau (ví dụ: Page Header mỗi nơi viết một kiểu, Table Skeleton chưa thống nhất).
- **Thẩm mỹ cao cấp (Visual Excellence)**: Hiến pháp dự án yêu cầu trải nghiệm "Wow". Việc tập trung vào một bộ thành phần dùng chung (Shared Components) giúp ta dễ dàng thêm các hiệu ứng Micro-animations, Glassmorphism và Shadow tinh tế vào một nơi nhưng tác động đến toàn bộ ứng dụng.
- **Tốc độ phát triển (Velocity)**: Khi có bộ `DataGrid`, `StatsCard`, `PageHeader` chuẩn, việc tạo một module mới (ví dụ: HRM hay Accounting) sẽ nhanh gấp 3 lần vì chỉ cần lắp ghép các "khối Lego" đã có sẵn.
- **Dễ bảo trì (Maintainability)**: Nếu muốn thay đổi phong cách nút bấm (Button) hoặc bảng màu (Color Palette), ta chỉ cần sửa tại một tệp thay vì rà soát hàng chục Page.

## 2. Các thành phần sẽ được chuẩn hóa

### A. Layout Components (`client/src/components/layout/`)
- **MainLayout**: Khung chuẩn bao gồm Sidebar (Nav) và Topbar (User info, Breadcrumbs).
- **AuthLayout**: Khung cho các trang đăng nhập/đăng ký.

### B. Business Components (`client/src/components/common/`)
- **PageHeader**: Bao gồm Tiêu đề, Mô tả, Breadcrumbs và cụm Nút hành động (Primary/Secondary).
- **StatsCard**: Thẻ hiển thị chỉ số (Số lượng, Doanh thu, Xu hướng % tăng/giảm).
- **DataGrid**: Bảng dữ liệu thông minh hỗ trợ sẵn Phân trang, Sắp xếp và trạng thái Loading.
- **EmptyState**: Hiển thị khi không có dữ liệu (kèm minh họa chuyên nghiệp).

### C. Form Components (`client/src/components/forms/`)
- **FormSection**: Nhóm các trường nhập liệu theo nhóm logic (ví dụ: Thông tin cá nhân, Cấu hình bảo mật).
- **SmartInput**: Input tích hợp sẵn icon và validation feedback.

## 3. Kế hoạch thực hiện (Steps)

1. **Giai đoạn 1 (Foundation)**: Xây dựng bộ `PageHeader` và `StatsCard` tại `client/src/components/common/`.
2. **Giai đoạn 2 (Data Layer)**: Xây dựng `DataGrid` tích hợp từ các thành phần bảng của Shadcn.
3. **Giai đoạn 3 (Refactoring)**: 
    - Cập nhật `Dashboard` sử dụng `StatsCard` và `PageHeader` mới.
    - Cập nhật `Leads` sử dụng `DataGrid` và `PageHeader` mới.
4. **Giai đoạn 4 (Polishing)**: Thêm hiệu ứng Framer Motion cho các transition của Page và Card.

## 4. Kiểm chứng (Verification)
- Kiểm tra giao diện trên nhiều độ phân giải (Responsive).
- Đảm bảo các Page cũ không bị vỡ giao diện sau khi refactor.
- `npm run check` để đảm bảo type-safety cho các props của component mới.
