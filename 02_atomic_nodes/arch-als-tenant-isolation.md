---
id: arch-als-tenant-isolation
title: Cô lập Tenant qua Async Local Storage (ALS)
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-clean-boundaries]]"
summary: "Cơ chế cô lập dữ liệu đa doanh nghiệp (Multi-tenancy) tự động bằng cách lưu trữ và inject organizationId qua Async Local Storage (ALS)."
tags: [architecture, security, multi-tenancy, als, tenant-isolation]
---

# Cô lập Tenant qua Async Local Storage (ALS)

Để đảm bảo dữ liệu của các doanh nghiệp (Tenants) khác nhau không bao giờ bị rò rỉ chéo, STAX áp dụng chiến lược cô lập dữ liệu tự động tại tầng cơ sở dữ liệu thông qua Async Local Storage (ALS).

## 1. Lưu trữ Context tự động
*   Khi request đi qua hệ thống Middleware xác thực (JWT/Session Gateway), hệ thống giải mã token và lấy ra `organizationId`.
*   Middleware khởi tạo context ALS và lưu trữ `organizationId` của phiên làm việc hiện tại vào đó:
    ```typescript
    als.run({ organizationId }, () => next());
    ```

## 2. Tự động Scoping tại Repository
*   Tại lớp Infrastructure, lớp `DrizzleBaseRepository` sẽ tự động đọc `organizationId` trực tiếp từ ALS khi thực hiện bất kỳ lệnh truy vấn SQL nào.
*   Lập trình viên không cần truyền thủ công `organizationId` từ Controller xuống Repository. Tránh hoàn toàn rủi ro rò rỉ dữ liệu do quên lọc theo Tenant ID.

## 3. Ràng buộc Database Index
*   Mọi bảng trong Database chứa dữ liệu đa tenant đều bắt buộc chứa cột `organization_id`.
*   Các chỉ mục duy nhất (Unique Index) trên các cột nghiệp vụ (như `code` hoặc `tax_code`) bắt buộc phải ghép cặp với `organization_id`:
    ```typescript
    uniqueIndex('idx_org_code').on(table.organizationId, table.code)
    ```
