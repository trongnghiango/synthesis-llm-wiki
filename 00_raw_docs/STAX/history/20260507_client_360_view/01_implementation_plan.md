# Implementation Plan — Client 360° View

Xây dựng trang quản lý chi tiết khách hàng chuyên nghiệp, hiện đại dành riêng cho lĩnh vực tư vấn Thuế & Kế toán.

## 1. Mục tiêu thiết kế
- **Thẩm mỹ**: Sử dụng phong cách Glassmorphism, layout thoáng đãng, Typography cao cấp (Inter).
- **Trải nghiệm**: Cung cấp cái nhìn toàn diện (360 độ) về khách hàng mà không gây quá tải thông tin.
- **Tính năng**: Quản lý thông tin tổ chức, hợp đồng, tình trạng tuân thủ thuế và lịch sử tương tác.

## 2. Cấu trúc Giao diện (Layout)

Trang sẽ chia thành 3 khu vực chính:

### A. Sidebar Thông tin (25%)
- Hiển thị Logo/Photo khách hàng.
- Thông tin định danh: Mã số thuế, Địa chỉ, Email chính, SĐT.
- Các nút hành động nhanh: Gửi Email, Tạo Zalo chat, Chỉnh sửa hồ sơ.

### B. Dashboard Trung tâm (50%)
- **Top Metrics Bar**: Các thẻ chỉ số (Compliance Score, YTD Revenue, Pending Tasks).
- **Tabbed Interface**:
    - **Overview**: Biểu đồ doanh thu năm, Danh sách người liên hệ chủ chốt (Key Contacts).
    - **Compliance (Tuân thủ)**: Bảng theo dõi các kỳ báo cáo thuế, tình trạng nộp tờ khai.
    - **Contracts**: Danh sách hợp đồng dịch vụ đang thực thi.
    - **Documents**: Kho lưu trữ file pháp lý (Gia hạn, GPKD, BCTC).

### C. Activity Timeline (25%)
- Luồng hoạt động ghi lại mọi tương tác theo thời gian thực.
- Hỗ trợ bộ lọc theo loại tương tác (Cuộc gọi, Họp, Email, Hệ thống).

## 3. Các thành phần cần xây dựng [NEW]

- `client/src/pages/admin/crm/client-detail.tsx`: Trang chính.
- `client/src/components/crm/ComplianceStatus.tsx`: Component hiển thị trạng thái tuân thủ thuế.
- `client/src/components/crm/InteractionTimeline.tsx`: Component dòng thời gian.
- `client/src/components/crm/ContactCard.tsx`: Card hiển thị danh sách người liên hệ.

## 4. Kế hoạch triển khai

### Bước 1: Khởi tạo Frame & Header
- Thiết lập Route `/admin/crm/clients/:id`.
- Sử dụng `PageHeader` nâng cấp để hiển thị tên công ty và trạng thái chung.

### Bước 2: Xây dựng Layout Grid
- Chia khung trang theo tỷ lệ 1:2:1 (Sidebar : Main : Timeline).
- Áp dụng các style Glassmorphism (bg-white/80, backdrop-blur, border-white/20).

### Bước 3: Triển khai các Tabs nghiệp vụ
- Xây dựng giao diện Tab Compliance (đặc thù mảng thuế).
- Tích hợp DataGrid cho danh sách Hợp đồng.

### Bước 4: Tích hợp dữ liệu
- Gọi API `getOrganizationById` kèm theo các quan hệ (Contracts, Contacts).
- Aggregate dữ liệu để hiển thị lên Dashboard.

## 5. Câu hỏi / Thảo luận
- **Compliance Tracking**: Bạn có muốn quản lý chi tiết từng loại tờ khai thuế (VAT, PIT, CIT) cụ thể hay chỉ cần trạng thái chung?
- **Accounting Data**: Hiện tại đã có module Kế toán chưa để chúng ta kéo dữ liệu hóa đơn/công nợ sang trang này?
