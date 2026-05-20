# Bước 2️⃣: Kế hoạch Kiến trúc Chi tiết (crm_analytics_service)

## A. Database Schema
**KHÔNG thay đổi schema, KHÔNG cần migration.**

Các bảng sẽ được query:
- `leads` — `status`, `source`, `acquired_at`, `assigned_employee_id`, `expected_value`
- `contracts` — `type` (ONE_OFF|RETAINER|SUBSCRIPTION), `value`, `status`, `start_at`, `end_at`, `lead_id`
- `quotes` — `status` (DRAFT|SENT|ACCEPTED|REJECTED|EXPIRED), `sent_at`, `total_amount`

Tất cả các column cần thiết đã tồn tại và có index phù hợp:
- `idx_leads_acquired_at` — cho time-series analytics
- `idx_leads_status` — cho funnel groupBy
- `idx_contracts_tenant_status` — cho revenue queries

## B. Domain Layer
**KHÔNG tạo Domain Entity mới.** `CrmAnalyticsService` là pure read-model service, không thao tác domain entities.

## C. Infrastructure Layer

### File mới cần tạo:
`backend/src/modules/crm/application/services/crm-analytics.service.ts`

Pattern: Inject `DRIZZLE` trực tiếp (như `DashboardService` hiện tại), sử dụng `sql` template literal của Drizzle ORM để viết CTE.

### Response DTOs (TypeScript Interfaces — trong cùng file service hoặc tách ra):
```typescript
// Có thể đặt trong: backend/src/modules/crm/infrastructure/dtos/analytics.response.dto.ts

export class PipelineStageDto {
  stage: string;
  count: number;
  conversionRate: number;   // % so với total leads
  avgDaysInStage: number;   // avg ngày head ở stage này (từ acquiredAt)
}

export class SourceEffectivenessDto {
  source: string;
  totalCount: number;
  wonCount: number;
  conversionRate: number;   // wonCount / totalCount * 100
  color: string;
}

export class PipelineResponseDto {
  stages: PipelineStageDto[];
  sources: SourceEffectivenessDto[];
  avgDaysToClose: number;   // Avg từ acquiredAt → contract.start_at (WON only)
}

export class RevenueMonthDto {
  month: string;            // "2026-05"
  mrr: number;              // Sum RETAINER contracts active trong tháng
  oneOff: number;           // Sum ONE_OFF contracts signed trong tháng
  leadsWon: number;         // Count leads WON trong tháng (theo acquiredAt)
  previousYear: number;     // Cùng tháng năm ngoái
}

export class RevenueResponseDto {
  monthly: RevenueMonthDto[];
}

export class AlertsResponseDto {
  coldLeads: number;              // Leads chưa tư vấn > 7 ngày
  stalledQuotes: number;          // Báo giá SENT > 14 ngày
  expiringContracts: number;      // Hợp đồng hết hạn trong 30 ngày
  unassignedLeads: number;        // Leads chưa assigned
  revenueConcentration: {
    topClientPercent: number;     // % doanh thu từ top 5 khách
    isRisky: boolean;             // true nếu > 60%
  };
}
```

## D. Application Layer

### Service Methods:
| Method | Input | Output | SQL Round-trips |
|---|---|---|---|
| `getPipeline()` | — | `PipelineResponseDto` | 1 CTE |
| `getRevenue()` | — | `RevenueResponseDto` | 1 CTE với LEFT JOIN YoY |
| `getAlerts()` | — | `AlertsResponseDto` | 1 CTE multi-count |

**Transaction boundary:** Không cần — read-only operations.
**Domain Events:** Không phát.
**Cross-module calls:** Không có.

## E. Presentation Layer & Contracts

### Shared Contracts (frontend/shared/contracts/crm.ts):
Không cần thêm Zod Schema cho analytics endpoints — đây là read-only data shape, Frontend đọc với `any` type hoặc TypeScript interface riêng. Không cần validate input.

### Controller — Thêm vào `dashboard.controller.ts`:
```
GET /dashboard/pipeline  → @Permissions('lead:read') → analyticsService.getPipeline()
GET /dashboard/revenue   → @Permissions('lead:read') → analyticsService.getRevenue()
GET /dashboard/alerts    → @Permissions('lead:read') → analyticsService.getAlerts()
```

**Deprecation plan:** Giữ nguyên `GET /dashboard/charts/revenue` và `GET /dashboard/insights` — không xóa để tránh break nếu có client nào còn dùng.

### Swagger:
```
@ApiOperation({ summary: 'Pipeline Funnel & Conversion Analytics' })
@ApiOperation({ summary: 'Revenue breakdown (MRR vs One-off) with YoY comparison' })
@ApiOperation({ summary: 'Operational alerts - at-risk leads, quotes, contracts' })
```

## F. Module Wiring

### CrmModule — Thêm vào `providers[]`:
```typescript
CrmAnalyticsService,  // Không cần Symbol token — internal service
```

### Inject vào DashboardController:
```typescript
constructor(
  private readonly dashboardService: DashboardService,
  private readonly analyticsService: CrmAnalyticsService, // THÊM
) {}
```

**CrmAnalyticsService constructor:**
```typescript
constructor(@Inject(DRIZZLE) private readonly db: NodePgDatabase<typeof schema>) {}
```

Không export ra ngoài `CrmModule` — chỉ dùng nội bộ qua Controller.

---
Kế hoạch này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
