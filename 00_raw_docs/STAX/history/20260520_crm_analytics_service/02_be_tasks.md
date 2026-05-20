# Bước 3️⃣: Checklist Thực thi (crm_analytics_service)

> Lưu ý: Đây là Analytics Service (read-only), không có Domain Entity, Repository, hay Migration.
> Checklist được điều chỉnh phù hợp với pattern này.

- [x] 1. Tạo Response DTO file: `backend/src/modules/crm/infrastructure/dtos/analytics.response.dto.ts`
       - `PipelineResponseDto` (stages + sources + avgDaysToClose)
       - `RevenueResponseDto` (monthly array với YoY)
       - `AlertsResponseDto` (coldLeads, stalledQuotes, expiringContracts, unassignedLeads, revenueConcentration)

- [x] 2. Tạo `CrmAnalyticsService`: `backend/src/modules/crm/application/services/crm-analytics.service.ts`
       - Method `getPipeline()`: SQL CTE group by stage + source với conversion rate
       - Method `getRevenue()`: SQL CTE monthly aggregation theo type (RETAINER/ONE_OFF) + YoY JOIN
       - Method `getAlerts()`: SQL CTE multi-count (coldLeads/stalledQuotes/expiring/unassigned + revenueConcentration)

- [x] 3. Cập nhật `DashboardController`: `backend/src/modules/crm/infrastructure/controllers/dashboard.controller.ts`
       - Inject `CrmAnalyticsService` vào constructor
       - Thêm route `GET /dashboard/pipeline` → `analyticsService.getPipeline()`
       - Thêm route `GET /dashboard/revenue` → `analyticsService.getRevenue()`
       - Thêm route `GET /dashboard/alerts` → `analyticsService.getAlerts()`
       - Giữ nguyên các route cũ (`/stats`, `/charts/revenue`, `/insights`) — deprecate dần

- [x] 4. Cập nhật `CrmModule`: `backend/src/modules/crm/crm.module.ts`
       - Thêm `CrmAnalyticsService` vào `providers[]`
       - KHÔNG export ra ngoài module

- [x] 5. Chạy build: `npm run build` — ✅ webpack compiled successfully, 0 errors

- [ ] 6. Manual API test via Swagger (`/api`) — test từng endpoint mới

---
Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
