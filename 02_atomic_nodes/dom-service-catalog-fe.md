---
id: dom-service-catalog-fe
title: Thiết kế Frontend Service Catalog & Tích hợp CRM/Accounting
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Định nghĩa Zod Schema, API Contract và tích hợp UI component Service Catalog vào CRM & Accounting."
tags: [frontend, service-catalog, zod, crm, react]
---

## 1. Zod Schema & API Contract
```typescript
// src/modules/crm/types/service.types.ts
export const ServiceSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().optional(),
  type: z.enum(['ONE_OFF', 'RETAINER', 'SUBSCRIPTION']),
  basePrice: z.number(),
  status: z.enum(['ACTIVE', 'INACTIVE', 'ARCHIVED'])
});
export type Service = z.infer<typeof ServiceSchema>;
```
*   `GET /api/crm/services` $\rightarrow$ `fetchServices()`
*   `POST /api/crm/services` $\rightarrow$ `createService(data)`
*   `PATCH /api/crm/services/:id` $\rightarrow$ `updateService(id, data)`

## 2. Core UI Components
*   **`ServicePicker.tsx` (Shadcn Popover + Command):** Smart Selector hỗ trợ hotkeys, tìm kiếm nhanh, hiển thị giá & loại hình. Output: Trả về object `Service` đầy đủ để auto-fill form cha.
*   **`ServiceTable.tsx`:** Quản lý dịch vụ phía Admin, hỗ trợ sửa giá nhanh (Inline Edit) và cập nhật trạng thái.

## 3. Điểm tích hợp (Integration Points)
*   **`QuoteForm`:** Thay thế trường nhập mô tả tự do bằng `ServicePicker`. Tự động điền `basePrice` $\rightarrow$ Unit Price và `description`.
*   **`FinoteForm` (Accounting - `[[dom-accounting-finote]]`):** Tích hợp field `Linked Service` (optional) để phân bổ chi phí trực tiếp cho dịch vụ.

## 4. Cấu trúc thư mục mục tiêu
*   `src/modules/crm/types/service.types.ts`
*   `src/modules/crm/api/service.api.ts`
*   `src/modules/crm/components/ServicePicker.tsx`
*   `src/pages/admin/crm/services.tsx`