---
id: std-naming-rules
title: Quy ước đặt tên trong dự án STAX
layer: 3-atomic
parent: "[[02_standards_governance]]"
depends_on: []
summary: "Hệ thống quy chuẩn đặt tên tệp, thư mục, biến, lớp và bảng cơ sở dữ liệu đảm bảo tính nhất quán tuyệt đối."
tags: [standards, naming-conventions, guidelines]
---

# Quy ước đặt tên trong dự án STAX

Tính đồng bộ trong cách đặt tên giúp AI Agent và Developer hiểu cấu trúc mã nguồn ngay lập tức mà không cần suy đoán.

## 1. Tên Tệp và Thư mục (Files & Folders)
*   **Thư mục module:** Sử dụng kebab-case (e.g., `org-structure`, `cash-book`).
*   **Quy tắc hậu tố file:** Tên file bắt buộc theo dạng `[name].[type].ts` để chỉ rõ phân lớp Clean Arch:
    *   Entity: `employee.entity.ts`
    *   Repository Interface: `employee.repository.ts`
    *   Use Case: `create-employee.usecase.ts`
    *   Controller: `employee.controller.ts`
    *   DTO: `create-employee.dto.ts`
    *   DB Schema: `employees.schema.ts`

## 2. Tên Biến, Hàm và Lớp (In-code Naming)
*   **Classes/Interfaces/Types:** Định dạng PascalCase (e.g., `OrgStructureService`, `CreateEmployeeDto`).
*   **Hàm & Biến:** Định dạng camelCase (e.g., `organizationId`, `isExpired()`).
*   **Hậu tố định danh ID bắt buộc:**
    *   `organizationId`: Multi-tenancy context.
    *   `userId`: Tài khoản đăng nhập.
    *   `employeeId`: Nhân sự nội bộ.
    *   `contactId`: Khách hàng/đối tác.
    *   `actorId`: Định danh người thực hiện hành động ghi log.

## 3. Cơ sở dữ liệu (Database Schema)
*   **Database Tables:** Số nhiều, snake_case (e.g., `organizations`, `employees`).
*   **Database Columns:** Chữ thường, snake_case (e.g., `organization_id`, `created_at`).
