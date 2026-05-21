---
id: dom-crm-client-360
title: Thiết kế Chi tiết Khách hàng CRM 360°
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-crm-activity-feed]]"
summary: "Đặc tả kỹ thuật trang Client 360° (ClientDetail) tích hợp trạng thái tuân thủ thuế, CRM API và dòng thời gian hoạt động."
tags: [crm, client-360, client-detail, tax-compliance, glassmorphism]
---

## 1. Cấu trúc Routing & Tệp tin (Absolute Paths)
- **Route:** `/admin/crm/clients/:id` mapping trực tiếp với component `ClientDetail`.
- **Tệp tin thay đổi:**
  - Trang chi tiết: `/home/ka/temps/DentalCarePortal/client/src/pages/admin/crm/client-detail.tsx`
  - Quản lý API: `/home/ka/temps/DentalCarePortal/client/src/modules/crm/api/crm.api.ts`
  - Định nghĩa Router: `/home/ka/temps/DentalCarePortal/client/src/app/router/index.tsx`
  - Danh sách khách hàng (Link trigger): `/home/ka/temps/DentalCarePortal/client/src/pages/admin/crm/clients.tsx`

## 2. API Contracts & Luồng dữ liệu (`crm.api.ts`)
Tích hợp các endpoints phục vụ hiển thị thông tin tổng hợp:
- `getClientById(id: string)`: Trả về Profile gốc, mã số thuế (MST) và trạng thái hoạt động.
- `getClientMetrics(id: string)`: Cung cấp 4 nhóm chỉ số thông minh: Tuân thủ Thuế, Doanh thu YTD, Việc cần làm, Sức khỏe quan hệ.
- `getClientContracts(id: string)`: Cung cấp danh sách hợp đồng cho `DataGrid`.
- `getClientActivities(id: string)`: Liên kết dòng thời gian thực với hệ thống `[[dom-crm-activity-feed]]`.

## 3. Kiến trúc UI & State Component
- **Mẫu thiết kế UI:** Áp dụng Glassmorphism (`backdrop-blur`, `border-white/20`, shadow).
- **Layout Grid 2 cột:**
  - *Identity Sidebar (Trái):* Thông tin định danh doanh nghiệp, MST, trạng thái tuân thủ thuế.
  - *Main Content (Phải):* 4 thẻ chỉ số nhanh ở phía trên và hệ thống Tabs phân vùng:
    - **Overview:** Biểu đồ doanh thu tháng & Danh sách nhân sự key của đối tác.
    - **Compliance Tracking:** Tiến độ nộp tờ khai (VAT, TNDN, TNCN).
    - **Contracts:** Bảng quản trị hợp đồng dịch vụ.
- **Interaction Timeline:** Phân loại hành động bằng mã màu trực quan (Emerald: Create, Blue: Update).