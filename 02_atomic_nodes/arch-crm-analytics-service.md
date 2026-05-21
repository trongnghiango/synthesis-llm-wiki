---
id: arch-crm-analytics-service
title: Thiết kế CrmAnalyticsService
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Thiết kế CrmAnalyticsService cung cấp API phân tích pipeline, doanh thu YoY và cảnh báo vận hành sử dụng Drizzle CTE."
tags: [crm, analytics, drizzle, nestjs, architecture]
---

## 1. Database & Domain Context
- **Read-only service**: Không có entity mới, không write/transaction, không domain event.
- **Bảng truy vấn**: `leads`, `contracts`, `quotes` (sử dụng index sẵn có: `idx_leads_acquired_at`, `idx_leads_status`, `idx_contracts_tenant_status`).

## 2. Infrastructure & Application Layer
- **File tạo mới**: `backend/src/modules/crm/application/services/crm-analytics.service.ts`
- **Pattern**: Inject `DRIZZLE` (`NodePgDatabase<typeof schema>`), sử dụng Drizzle `sql` literal viết CTE tối ưu hóa round-trip (1 CTE/method).

### API Endpoints (`dashboard.controller.ts`)
Yêu cầu guard `@Permissions('lead:read')`:
- `GET /dashboard/pipeline` -> `PipelineResponseDto` (Funnel & Conversion rate).
- `GET /dashboard/revenue` -> `RevenueResponseDto` (MRR vs One-off, so sánh YoY).
- `GET /dashboard/alerts` -> `AlertsResponseDto` (Cảnh báo vận hành & rủi ro tập trung doanh thu).

### DTOs Structure (Tóm tắt)
- `PipelineResponseDto`: `stages` (stage, count, conversionRate, avgDaysInStage), `sources` (won/total, rate), `avgDaysToClose`.
- `RevenueResponseDto`: `monthly` (month, mrr, oneOff, leadsWon, previousYear).
- `AlertsResponseDto`: `coldLeads` (>7 ngày), `stalledQuotes` (>14 ngày), `expiringContracts` (<30 ngày), `unassignedLeads`, `revenueConcentration` (top 5 clients >60% doanh thu).

## 3. Module Wiring
- **CrmModule**: Khai báo `CrmAnalyticsService` trong `providers` (không export).
- **DashboardController**: Inject trực tiếp qua constructor:
  ```typescript
  constructor(
    private readonly dashboardService: DashboardService,
    private readonly analyticsService: CrmAnalyticsService
  ) {}
  ```
- **Deprecation**: Giữ nguyên `/charts/revenue` và `/insights` để đảm bảo tương thích ngược.