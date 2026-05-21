---
id: dom-crm-client-360-view
title: Hồ Sơ Khách Hàng CRM 360°
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
summary: "Triển khai màn hình chi tiết khách hàng ClientDetail 360° tích hợp Glassmorphism, chỉ số tài chính, tuân thủ thuế và dòng hoạt động."
tags: [crm, client-360, react, api-contract, compliance]
---

## 1. Cấu trúc Routing & File
- **Route:** `/admin/crm/clients/:id` (Điều hướng từ `clients.tsx` khi click dòng).
- **Files thay đổi:**
  - Frontend UI: `client-detail.tsx` (Glassmorphism layout), `router/index.tsx`
  - API Client: `crm.api.ts` (Tích hợp SDK/API fetch thông tin 360°).

## 2. API Contract (`crm.api.ts`)
```typescript
// GET /api/crm/clients/:id
interface Client360Detail {
  profile: { id: string; name: string; taxCode: string; status: string; contact: string };
  metrics: { complianceScore: number; ytdRevenue: number; pendingTasks: number; healthScore: string };
  compliance: Array<{ taxType: 'VAT' | 'TNDN' | 'TNCN'; period: string; status: 'submitted' | 'pending' | 'overdue' }>;
  contracts: Array<{ id: string; code: string; value: number; status: string }>;
  activities: Array<{ id: string; action: 'create' | 'update'; message: string; timestamp: string }>;
}
```

## 3. Kiến trúc Component & UX Pattern
- **Layout Glassmorphism:** Áp dụng `backdrop-blur`, `border-white/20` tạo chiều sâu thị giác cao cấp.
- **Identity Sidebar:** Khóa cứng thông tin MST, liên hệ pháp lý của doanh nghiệp.
- **Top Metrics Grid:** 4 thẻ chỉ số nhanh (Tuân thủ, YTD Revenue, Tasks, Health).
- **Tabbed Interface:**
  - *Overview:* Biểu đồ doanh thu tháng + Danh sách Key Personnel.
  - *Compliance:* Bảng tiến độ nộp tờ khai (VAT, TNDN, TNCN) trực quan hóa theo màu trạng thái.
  - *Contracts:* Quản lý phụ lục, hợp đồng thông qua `DataGrid`.
- **Interaction Timeline:** Tích hợp với `[[hb-delta-logging]]` để hiển thị dòng lịch sử tương tác theo thời gian thực (Emerald đại diện cho Create, Blue cho Update).