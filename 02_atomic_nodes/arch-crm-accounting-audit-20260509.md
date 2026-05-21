---
id: arch-crm-accounting-audit-20260509
title: Sửa lỗi Cô lập Accounting & Định danh CRM
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-tenant-isolation]]"
  - "[[dom-accounting-finote]]"
summary: "Giải quyết trùng lặp thực thể CRM, áp dụng cô lập Tenant cho Accounting và chuẩn hóa Attachment."
tags: [crm, accounting, tenant-isolation, identity, refactoring]
---

## 1. Bảo vệ Định danh CRM (`LeadIntakeService`)
- **Vấn đề:** Khớp nối Lead vào Organization cũ chỉ dựa trên Phone Number gây ghi đè chéo dữ liệu.
- **Giải pháp:** 
  - Bổ sung `IOrganizationRepository.findByName(name: string)`.
  - Quy trình xử lý: Xác thực chéo cả Name và Phone. Nếu không trùng khớp đồng thời, hệ thống bắt buộc tạo mới `Organization` và `Contact` độc lập.

## 2. Cô lập Tenant Accounting (`Finote`)
- **Write (`createFinote`):** Áp dụng chế độ cô lập Tenant triệt để, gán cứng `ownerOrgId` theo `user.organizationId` từ session context.
- **Read (`getFinotes`):** Bỏ qua tham số `orgId` truyền từ Query String. Bắt buộc filter dữ liệu theo `user.organizationId` của phiên đăng nhập.
- **Xử lý ngoại lệ:** Thay thế hoàn toàn `BadRequestException` (HTTP Layer) bằng `BusinessRuleValidationException` (Domain Layer) để đảm bảo tính độc lập của kiến trúc.

## 3. Chuẩn hóa Cơ sở dữ liệu & Entity
- **Data Fix:** Thực hiện migration cập nhật `source_org_id = 1` cho bản ghi `INC-2026-0003` để hiển thị chính xác trên Dashboard của Accounting Firm.
- **Refactoring:** Loại bỏ hoàn toàn thực thể cũ `FinoteAttachment`. Đồng nhất toàn bộ cấu trúc lưu trữ qua thực thể dùng chung `Attachment`.