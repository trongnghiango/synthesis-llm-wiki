---
id: dom-hrm_master_data_implementation
title: Triển khai Module Danh mục HRM
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
summary: "Triển khai module Danh mục HRM gồm Chức danh, Bậc lương và cơ chế lookup động phục vụ định biên nhân sự."
tags: [hrm, master-data, use-lookups, clean-architecture]
---

## 1. Cấu trúc Schema & Quan hệ
Thiết lập hệ thống Master Data bổ trợ cho Định biên Vị trí (`Position`):
- **JobTitle (Chức danh)**: `id` (UUID), `name` (Varchar), `code` (Varchar), `tenant_id` (UUID) -> Hỗ trợ cô lập dữ liệu đa người dùng qua [[arch-als-tenant-isolation]].
- **SalaryScale (Bậc lương)**: `id` (UUID), `name` (Varchar), `grade` (Varchar), `tenant_id` (UUID).
- **Position (Vị trí)**: Tích hợp FK tham chiếu trực tiếp đến `JobTitle` và `SalaryScale`.

## 2. API Contract & Luồng Dữ liệu
Toàn bộ logic nghiệp vụ tập trung tại `hrm.api.ts`:
- `GET /api/hrm/titles` | `POST /api/hrm/titles` - Truy vấn/Khai báo Chức danh.
- `GET /api/hrm/salary-scales` | `POST /api/hrm/salary-scales` - Truy vấn/Khai báo Bậc lương.

## 3. Cơ chế Đồng bộ State (Lookups)
- Nâng cấp hook `useLookups` để tự động nạp và quản lý cache trạng thái của các danh mục mới.
- Khớp nối luồng: Khi người dùng thêm mới Chức danh/Bậc lương tại `Danh mục HRM` -> Kích hoạt cơ chế invalidation của `useLookups` -> Cập nhật tức thì dữ liệu chọn (Dropdown) tại form cấu trúc Vị trí thuộc trang Sơ đồ tổ chức.