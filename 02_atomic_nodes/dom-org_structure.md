---
id: dom-org_structure
title: Sơ đồ Cấu trúc Tổ chức Trực quan
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
summary: "Thiết kế và triển khai sơ đồ tổ chức trực quan (Org Chart) tương tác cao sử dụng Framer Motion, xử lý dữ liệu đệ quy và tối ưu hiển thị."
tags: [org-chart, framer-motion, tailwind, recursive-data]
---

## 1. Thiết kế Hệ thống & Khớp dữ liệu (Data Binding)
- **Cấu trúc Dữ liệu**: Cây phân cấp lồng nhau (Nested Tree Structure) biểu diễn sơ đồ tổ chức, phòng ban và vị trí nhân sự.
- **Xử lý API**: Cơ chế trích xuất payload thích ứng linh hoạt với các cấu trúc phản hồi khác nhau (Axios response wrapper vs raw JSON body). Đảm bảo cô lập dữ liệu đa nhân hộ thông qua `[[arch-als-tenant-isolation]]`.

## 2. Giải pháp Giao diện (UI/UX)
- **Engine kết xuất**: Framer Motion kết hợp SVG/HTML Canvas, tối ưu hóa hiệu năng render vector, chống nhòe hình (blur) khi thực hiện zoom/pan.
- **Khắc phục Clipping**: Loại bỏ hoàn toàn ràng buộc `min-height` cố định tại các container cha để tối ưu hóa hiển thị responsive trên các viewport nhỏ.
- **Style System**: Tích hợp hiệu ứng Glassmorphism và Dark Mode đồng bộ qua Tailwind CSS.

## 3. Kế hoạch Phát triển Tiếp theo
- **Search & Focus**: Tính toán ma trận tọa độ vector để tự động dịch chuyển và căn giữa (center) node mục tiêu trên canvas khi tìm kiếm.
- **Interactive Drag & Drop**: Triển khai logic Re-parenting để thay đổi cấp bậc trực quan, tự động gọi API cập nhật cấu trúc DB.
- **High-res Export**: Hỗ trợ kết xuất đồ họa chất lượng cao sang định dạng PNG/PDF.