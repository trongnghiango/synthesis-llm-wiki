---
id: dom-rbac_resource_standardization
title: Chuẩn hóa Tài nguyên RBAC và Logic Khớp Quyền
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on: []
summary: "Chuẩn hóa tài nguyên hrm thành employee/org và cập nhật logic wildcard 'manage' để sửa lỗi phân quyền ADMIN."
tags: [rbac, permission, authorization, security]
---

### 1. Vấn đề & Mục tiêu
Khắc phục lỗi `Permission denied: employee:read` của vai trò `ADMIN` do sự bất nhất giữa seed data (`hrm`) và codebase (`employee`, `org`).

### 2. Thay đổi Dữ liệu hạt giống (`01_rbac_rules.csv`)
*   Tách tài nguyên `hrm` thành `employee` và `org`.
*   Cấp quyền wildcard (`*`) cho `ADMIN` trên cả hai tài nguyên mới.
*   Cập nhật và căn chỉnh lại cấu hình phân quyền cho các vai trò `MANAGER` và `STAFF`.

### 3. Cải tiến Logic Quyền (`permission.service.ts`)
*   Cập nhật hàm `checkPermissionMatch`: Cấu hình hành động `manage` hoạt động như một wildcard quyền lực cao nhất (tương đương `*` cho action), tự động khớp với mọi hành động cụ thể (`read`, `write`, `delete`, v.v.) thuộc cùng tài nguyên.

### 4. Đồng bộ UI Bootstrap (`bootstrap.service.ts`)
*   Đồng bộ hóa các cờ kiểm tra quyền ở frontend (UI flags như `canManageHRM`) dựa trên tài nguyên mới (`employee` và `org`) thay vì tài nguyên `hrm` cũ.

### 5. Xác minh hệ thống
*   **API Verification:** Đảm bảo `ADMIN` truy cập thành công `/api/hrm/employees` (Status `200 OK`).
*   **UI Integration:** Gọi `/api/system/bootstrap` để kiểm tra tính chính xác của các cờ phân quyền UI mới.