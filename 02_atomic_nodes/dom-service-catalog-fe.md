---
id: dom-service-catalog-fe
title: Thiết kế Frontend Service Catalog & Tích hợp
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Zod schema, API contract, ServicePicker và luồng tích hợp Service Catalog vào Quote và Finote."
tags: [crm, service-catalog, frontend, integration]
---

## 1. API Contract & Data Model (Zod)
```typescript
const ServiceSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().optional(),
  type: z.enum(['ONE_OFF', 'RETAINER', 'SUBSCRIPTION']),
  basePrice: z.number(),
  status: z.enum(['ACTIVE', 'INACTIVE', 'ARCHIVED'])
});
type Service = z.infer<typeof ServiceSchema>;
```
- `GET /api/crm/services` $\rightarrow$ `fetchServices(): Promise<Service[]>`
- `POST /api/crm/services` $\rightarrow$ `createService(data: Omit<Service, 'id'>)`
- `PATCH /api/crm/services/:id` $\rightarrow$ `updateService(id: number, data: Partial<Service>)`

## 2. UI Components & Luồng tích hợp
- **`ServicePicker`**: Component Shadcn (Popover + Command) hỗ trợ tìm kiếm nhanh, hotkeys, hiển thị giá/loại. Output: Trả về full `Service` object cho form cha.
- **`ServiceTable`**: Trang Admin quản lý dịch vụ, hỗ trợ thay đổi nhanh trạng thái và giá trực tiếp (Inline Editing).
- **Tích hợp `QuoteForm` (Lead Detail)**: Thay thế trường nhập text tự do bằng `ServicePicker`. Tự động điền (auto-fill) `Unit Price` và `Description` ngay khi chọn.
- **Tích hợp `FinoteForm` (`[[dom-accounting-finote]]`)**: Bổ sung trường `Linked Service` (optional) phục vụ phân tích cấu trúc chi phí doanh thu theo dịch vụ.

## 3. Cấu trúc thư mục dự án
- `src/modules/crm/types/service.types.ts` (Zod schemas & Types)
- `src/modules/crm/api/service.api.ts` (API Hooks)
- `src/modules/crm/components/ServicePicker.tsx`
- `src/pages/admin/crm/services.tsx` (Trang quản trị)