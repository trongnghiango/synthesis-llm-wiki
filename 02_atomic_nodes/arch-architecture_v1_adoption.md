---
id: arch-architecture_v1_adoption
title: Áp dụng Kiến trúc V1 - Giai đoạn 0
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Quy hoạch RBAC sang chuẩn domain:action, cấu trúc lại API Bootstrap permissions.raw/flags và xác lập Backend làm Domain Service."
tags: [architecture, rbac, bootstrap-service, migration]
---

## 1. Chuẩn hóa Quy hoạch Domain RBAC
Thay đổi cơ chế phân quyền tại `database/seeds/01_rbac_rules.csv` từ Resource-based cũ sang định dạng chuẩn `domain:action`:
- `lead` $\rightarrow$ `crm` (Ví dụ: `crm:read`, `crm:write`)
- `finote` $\rightarrow$ `accounting` (Chi tiết nghiệp vụ: [[dom-accounting-finote]])
- `employee` $\rightarrow$ `hrm`

## 2. API Contract: Bootstrap Service
`BootstrapService` nâng cấp cấu trúc dữ liệu phân quyền trả về phía Client, đã được kiểm thử tại `bootstrap.service.spec.ts`:
```typescript
interface BootstrapResponse {
  permissions: {
    raw: string[];                 // Danh sách quyền thô dạng "domain:action" (e.g., "crm:read")
    flags: Record<string, boolean>; // Cờ boolean mapping phục vụ dựng UI nhanh
  };
}
```

## 3. Định vị Kiến trúc & Quản lý Bối cảnh
- **Domain Service:** Khẳng định vai trò Backend hoạt động như một Domain Service (Cập nhật tại `architecture.md#Section-9`).
- **Context Path:** Toàn bộ tài liệu bối cảnh chuyển dịch lưu tại `docs/STAX/context/20260505_architecture_v1_adoption/`.