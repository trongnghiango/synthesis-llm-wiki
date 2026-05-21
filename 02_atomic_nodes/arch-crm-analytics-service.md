---
id: arch-crm-analytics-service
title: Thiết kế CrmAnalyticsService
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Kiến trúc CrmAnalyticsService tối ưu truy vấn CTE qua Drizzle ORM phục vụ dashboard pipeline, doanh thu YoY và cảnh báo."
tags: [crm, analytics, drizzle-orm, pipeline, revenue]
---

### 1. Database & Infrastructure
- **Bảng đích**: `leads` (`status`, `source`, `acquired_at`), `contracts` (`type`, `value`, `status`), `quotes` (`status`, `sent_at`).
- **Indexes sử dụng**: `idx_leads_acquired_at` (time-series), `idx_leads_status` (funnel), `idx_contracts_tenant_status` (revenue).
- **Pattern**: Tạo service pure read-model `backend/src/modules/crm/application/services/crm-analytics.service.ts`. Inject trực tiếp `@Inject(DRIZZLE)`, viết truy vấn SQL CTE tối ưu bằng template literal `sql` của Drizzle. Không dùng entity domain, không transaction, không phát event.

### 2. API Contracts & Controller
Tích hợp vào `backend/src/modules/crm/presentation/dashboard.controller.ts` (Giữ các endpoints cũ để tương thích ngược):
- `GET /dashboard/pipeline` | Quyền: `lead:read` | Output: `PipelineResponseDto` (Funnel stages, conversion rate, conversion source, avgDaysToClose).
- `GET /dashboard/revenue` | Quyền: `lead:read` | Output: `RevenueResponseDto` (Doanh thu tháng: MRR, One-off, Leads Won và so sánh YoY cùng kỳ năm trước).
- `GET /dashboard/alerts` | Quyền: `lead:read` | Output: `AlertsResponseDto` (Cảnh báo: coldLeads >7 ngày, stalledQuotes >14 ngày, expiringContracts <30 ngày, unassignedLeads, revenueConcentration top 5 >60%).
- **Frontend Contract**: Định nghĩa interface tại `frontend/shared/contracts/crm.ts` (Không cần schema Zod validation).

### 3. Module Wiring
- **CrmModule**: Khai báo `CrmAnalyticsService` trong `providers` (chỉ dùng nội bộ, không export).
- **DashboardController**: Inject trực tiếp `CrmAnalyticsService` vào constructor bên cạnh `DashboardService`.