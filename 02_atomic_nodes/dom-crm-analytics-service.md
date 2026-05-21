```yaml
---
id: dom-crm-analytics-service
title: Phân tích & Thống kê CRM
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Dịch vụ read-only phân tích CRM (Pipeline, Doanh thu, Cảnh báo) dùng Drizzle CTE trực tiếp."
tags: [crm, analytics, drizzle-orm, read-model, dashboard]
---

### 1. Kiến trúc & Database
- **Pattern**: Pure Read-Model Service. Inject `DRIZZLE` trực tiếp vào `CrmAnalyticsService`, dùng `sql` template literal viết CTE tối ưu (1 round-trip/method).
- **Database**: Chỉ đọc, không migration. Query các bảng:
  - `leads` (`idx_leads_acquired_at`, `idx_leads_status`)
  - `contracts` (`idx_contracts_tenant_status`)
  - `quotes`
- **File service**: `backend/src/modules/crm/application/services/crm-analytics.service.ts`

### 2. API Contracts & Controllers
Tích hợp vào `dashboard.controller.ts` (Guarded: `@Permissions('lead:read')`):
- `GET /dashboard/pipeline` -> `getPipeline()`: Thống kê phễu & tỷ lệ chuyển đổi nguồn lead.
- `GET /dashboard/revenue` -> `getRevenue()`: Doanh thu MRR vs One-off, so sánh YoY.
- `GET /dashboard/alerts` -> `getAlerts()`: Cảnh báo vận hành (leads/quotes trễ hạn, nợ đọng, rủi ro tập trung doanh thu >60% top 5).

*Lưu ý*: Giữ nguyên các API cũ (`GET /dashboard/charts/revenue`, `GET /dashboard/insights`) để tránh breaking changes.

### 3. Module Wiring
- **CrmModule**: Đăng ký `CrmAnalyticsService` trong `providers[]` (nội bộ, không export).
- **DashboardController**: Inject trực tiếp `CrmAnalyticsService` qua Constructor.
```