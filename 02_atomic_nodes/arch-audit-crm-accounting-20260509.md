---
id: arch-audit-crm-accounting-20260509
title: Sửa đổi Định danh CRM & Cô lập Kế toán STAX
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-tenant-isolation]]"
  - "[[dom-accounting-finote]]"
summary: "Khắc phục lỗi trùng lặp định danh CRM và rò rỉ dữ liệu đa bên (multi-tenancy) trong module Kế toán."
tags: [crm, accounting, tenant-isolation, identity-integrity, refactoring]
---

### 1. CRM Identity Protection
- **Vấn đề:** Trùng lặp liên kết tổ chức/liên hệ mới vào tổ chức cũ khi trùng số điện thoại.
- **Giải pháp:** Cập nhật `LeadIntakeService` bắt buộc kiểm tra tên tổ chức trước khi liên kết. Nếu tên khác biệt hoặc mới, tạo `Organization` và `Contact` riêng biệt.
- **Repo Contract:** Thêm phương thức `findByName(name: string)` vào `IOrganizationRepository`.

### 2. Accounting Isolation & Security ([[arch-tenant-isolation]])
- **Giao dịch Ghi (Write):** Áp đặt kiểm tra tenant isolation trong `FinoteService.createFinote`.
- **Giao dịch Đọc (Read):** Cập nhật `FinoteController.getFinotes` loại bỏ `orgId` từ Query String; bắt buộc sử dụng `user.organizationId` trích xuất trực tiếp từ session bảo mật.
- **Design Pattern:** Thay thế `BadRequestException` bằng `BusinessRuleValidationException` tại tầng Domain/Application để tuân thủ thiết kế sạch, tránh rò rỉ framework.

### 3. Cleanup & DB Patch
- **Schema Refactor:** Loại bỏ hoàn toàn thực thể liên kết cũ `FinoteAttachment`. Thống nhất sử dụng thực thể dùng chung `Attachment`.
- **Data Patch:** Cập nhật bản ghi `INC-2026-0003` chuyển `source_org_id = 1` (Accounting Firm) đảm bảo hiển thị đúng dashboard của Tenant sở hữu.