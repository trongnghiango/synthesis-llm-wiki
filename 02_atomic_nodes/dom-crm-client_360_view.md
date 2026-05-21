---
id: dom-crm-client_360_view
title: Chi tiết khách hàng CRM 360°
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
summary: "Trang chi tiết khách hàng CRM 360° tích hợp theo dõi tuân thủ thuế, hợp đồng, và dòng thời gian tương tác thời gian thực."
tags: [crm, client-360, tax-compliance, react, ui-ux]
---

## 1. Định tuyến & Tích hợp Luồng
- **Route đăng ký**: `/admin/crm/clients/:id` (định nghĩa tại `router/index.tsx`).
- **Luồng chuyển hướng**: Tích hợp sự kiện click dòng tại danh sách khách hàng (`clients.tsx`) điều hướng trực tiếp sang trang chi tiết (`client-detail.tsx`).

## 2. Kiến trúc Trang Chi tiết (client-detail.tsx)
- **Giao diện**: Thiết kế Glassmorphism (`backdrop-blur`, `border-white/20`, bóng đổ), hỗ trợ Responsive Mobile & Desktop.
- **Chỉ số Top Metrics**: 4 thẻ KPI động (Tuân thủ Thuế, Doanh thu YTD, Việc cần làm, Sức khỏe mối quan hệ).
- **Cấu trúc Tabs**:
  - **Overview**: Biểu đồ doanh thu trực quan + Danh sách nhân sự chủ chốt (Key Contacts).
  - **Compliance Tracking**: Bảng trạng thái tiến độ nộp tờ khai thuế (VAT, TNDN, TNCN) theo màu sắc.
  - **Contracts**: Quản lý danh sách hợp đồng dịch vụ thông qua component `DataGrid`.
- **Dòng thời gian tương tác (Timeline)**: Liên kết trực tiếp hệ thống Activity Feed, phân loại log theo màu sắc (Emerald: Create, Blue: Update) kế thừa cơ chế từ `[[hb-delta-logging]]`.

## 3. Tích hợp Dữ liệu & API
- **API Client**: `crm.api.ts` bổ sung các hàm call API lấy thông tin chi tiết Client, danh sách hợp đồng và trạng thái tuân thủ.
- **UX**: Tích hợp trạng thái Loading Skeleton mượt mà trong quá trình nạp dữ liệu từ client API.