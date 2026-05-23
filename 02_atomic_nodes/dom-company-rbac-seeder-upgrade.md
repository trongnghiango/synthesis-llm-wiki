---
id: dom-company-rbac-seeder-upgrade
title: Nâng cấp Seeder Doanh nghiệp & RBAC
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-tenant-isolation]]"
summary: "Nâng cấp cơ chế seeding cây phòng ban đa tầng, thuật toán fuzzy matching đồng bộ nhân sự và tự động hóa tài khoản RBAC bảo toàn bảo mật."
tags: [seeder, rbac, tenant-isolation, fuzzy-matching, organization-tree]
---

### 1. Thiết kế Cây Tổ chức & Cô lập Tenant
- **Cấu trúc Cây Phòng Ban**: Tổ chức cây phân cấp B-Tree thông qua trường `path` chuyên biệt. Nút gốc `BOD` độc lập, nút cha `DIV_CS` (Dịch vụ Khách hàng) tự động quét và ánh xạ các nút con `TEAM 01` đến `TEAM 04`.
- **Cô lập Tenant**: Ràng buộc toàn bộ thực thể và quan hệ được khởi tạo dưới `organizationId = 1` (STAX Enterprise) tuân thủ nghiêm ngặt [[arch-tenant-isolation]].

### 2. Thuật toán Đồng bộ & Quy tắc Nghiệp vụ
- **Fuzzy Suffix Matching**: Chuẩn hóa chuỗi (lược bỏ dấu tiếng Việt, viết thường) và so khớp từ tố giữa `STAFF.csv` và `THONG TIN NHAN VIEN.csv` để ánh xạ chính xác nhân sự viết tắt hoặc thay đổi họ/tên đệm (ví dụ: "Thủy Vũ" ➔ "Võ Thị Thu Thủy").
- **Chuẩn Username**: Định dạng tự động theo cấu trúc `[tên_chính][họ_chính]` viết liền không dấu (ví dụ: `duyenvo`, `thuyvo`).
- **Bảo toàn Mật khẩu**: Đồng bộ hash mật khẩu mặc định khớp với plaintext `Company@2026` cho cả tài khoản cũ và mới, ngăn chặn lỗi sai thông tin đăng nhập sau seed.

### 3. Kết quả Thực thi & Kiểm thử
- **Domain Purity**: Đạt độ sạch tuyệt đối, chỉ sử dụng kiểu dữ liệu thuần túy (pure domain types).
- **Chỉ số Đồng bộ Hệ thống**: 8 nhân sự thực tế được ánh khớp, 10 vị trí định biên được thiết lập, 14 người dùng hoạt động và 23 hồ sơ nhân sự được đồng bộ thành công vào cơ sở dữ liệu.