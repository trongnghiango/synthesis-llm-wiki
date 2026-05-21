---
id: dom-finote-detail-page
title: Chi tiết Phiếu Thu Chi Finote
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Thiết kế và triển khai trang chi tiết Phiếu Thu/Chi (finote-detail) sử dụng TanStack Router, Bento Grid, và cơ chế Server-Driven Actions."
tags: [accounting, finote, frontend, tanstack-router, bento-grid]
---

### 1. Luồng nghiệp vụ & API Contract
* **Routing**: `/admin/accounting/finotes/$id` (Type-safe params qua TanStack Router).
* **API Endpoint**: Tích hợp `getFinoteById(id)` trong `accounting.api.ts`.
* **Server-Driven Actions**: Quyền hiển thị và thực thi hành động (Duyệt/Từ chối) được quyết định động bởi cờ `_actions` trả về từ API payload, tối ưu tính bảo mật và nhất quán trạng thái.

### 2. Giải pháp Thiết kế Giao diện (UI/UX Pattern)
* **Bento Grid**: Tổ chức thông tin trực quan, tách biệt rõ ràng thông tin tài chính cốt lõi và dữ liệu đối tượng liên quan.
* **PDF Preview**: Nhúng trực tiếp tài liệu qua `iframe`. Tự động chuẩn hóa `pdfUrl` với Backend Base URL. Hỗ trợ chế độ xem nhanh (Thumbnail) và phóng to (Fullscreen Dialog).
* **Hiệu ứng & Trải nghiệm**: Sử dụng Glassmorphism (backdrop-blur + gradient) kết hợp Framer Motion để tối ưu hóa hiệu ứng chuyển cảnh; đồng bộ trạng thái tải dữ liệu bằng Skeleton UI.

### 3. Tác động Hệ thống (Impacted Files)
* `client/src/modules/accounting/api/accounting.api.ts`: Thêm `getFinoteById`.
* `client/src/app/router/routes/accounting-routes.tsx` & `index.tsx`: Đăng ký route và cập nhật Route Tree.
* `client/src/pages/admin/accounting/finotes.tsx`: Liên kết chuyển trang thông qua TanStack `Link`.
* `client/src/pages/admin/accounting/finote-detail.tsx` [NEW]: Thành phần giao diện chính.