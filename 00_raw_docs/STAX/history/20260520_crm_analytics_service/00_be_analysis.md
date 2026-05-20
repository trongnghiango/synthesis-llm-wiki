# Bước 1️⃣: Phân tích Nghiệp vụ & Kiến trúc (crm_analytics_service)

> **Context Base:** Decision Log từ `@stax-think` session 20260520.

## A. Phân loại module
- **Tier**: Tier 3 — Process Flow (CRM module).
- `CrmAnalyticsService` sẽ nằm trong `crm` module, là internal service — không expose Symbol DI Token ra module khác vì không có module nào cần inject analytics service.
- **Phụ thuộc**: `CrmModule` (tự thân) → inject `DRIZZLE` token trực tiếp từ `DrizzleModule`.
- **Không phụ thuộc**: `ILeadRepository`, `IContractRepository`, `IQuoteRepository` — analytics là read-only cross-entity, không đi qua domain layer.

## B. Bounded Context & Ubiquitous Language

| Tên nghiệp vụ | Tên kỹ thuật | Ghi chú |
|---|---|---|
| Funnel chuyển đổi | Pipeline / Conversion Funnel | Tỷ lệ Lead qua từng stage |
| Ngày tiếp nhận thực tế | `acquiredAt` / `acquired_at` | Dùng thay vì `createdAt` cho time-series |
| Hợp đồng trọn gói | `type = 'RETAINER'` | Khách hàng retainer hàng tháng |
| Hợp đồng dự án | `type = 'ONE_OFF'` | Hợp đồng dự án một lần |
| Doanh thu tái tục (MRR) | Monthly Recurring Revenue | Tổng giá trị RETAINER active |
| Lead nguội | coldLeads | Lead chưa tư vấn >7 ngày kể từ acquiredAt |
| Báo giá tắc | stalledQuotes | Báo giá SENT >14 ngày chưa phản hồi |
| Rủi ro tập trung | revenueConcentration | Top clients chiếm >60% doanh thu |

## C. Data Flow & API Design

```
Client → DashboardController → CrmAnalyticsService → Drizzle SQL CTE → PostgreSQL
```

Các endpoint cần thiết:

| Method | Path | Service method | Ghi chú |
|---|---|---|---|
| GET | `/dashboard/pipeline` | `getPipeline()` | MỚI |
| GET | `/dashboard/revenue` | `getRevenue()` | MỚI (thay thế `/charts/revenue`) |
| GET | `/dashboard/alerts` | `getAlerts()` | NÂNG CẤP (thay `getInsights()`) |
| GET | `/dashboard/stats` | Giữ nguyên `DashboardService.getStats()` | Không thay đổi |

Permission: `lead:read` cho tất cả (đồng nhất với route hiện tại).

## D. Cross-module dependencies
- **KHÔNG** cross-module. `CrmAnalyticsService` inject `DRIZZLE` trực tiếp — đây là pattern đúng cho read-model/analytics, tương tự cách `DashboardService` đang hoạt động.
- Không phát Domain Event (read-only).
- Không cần `ITransactionManager` (không có write operation).

## E. Multi-tenancy
- Analytics hiện tại không filter theo `organizationId` vì STAX là single-tenant per deployment. `DashboardService` hiện đang nhận `orgId` qua query param nhưng thực tế là optional.
- **Giữ nguyên pattern này** cho `CrmAnalyticsService` — không thêm tenant isolation mới.
- Lưu ý: Nếu STAX chuyển sang multi-tenant SaaS, cần review lại toàn bộ analytics queries.

## F. Security (`_actions` / Server-Driven UI)
- Analytics endpoints là **read-only**, không trả về `_actions`.
- Chỉ cần `@Permissions('lead:read')` — đồng nhất với controller hiện tại.

---
Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết.
