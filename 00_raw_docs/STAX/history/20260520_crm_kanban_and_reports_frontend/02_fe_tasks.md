# Checklist Thực thi Frontend (02_fe_tasks.md)
**Feature:** CRM Kanban Board & Reports Dashboard
**Date:** 2026-05-20

## Danh sách công việc thực thi:
- [ ] 1. Khai báo thêm các hàm API `getStats`, `getCharts`, `getInsights` trong `frontend/client/src/modules/crm/api/crm.api.ts`.
- [ ] 2. Tạo component `LeadKanbanBoard` (kéo thả HTML5, check phân quyền `_actions.edit.allowed`, kéo thả sang `WON` mở Close Won Dialog).
- [ ] 3. Tạo component `LeadReportsDashboard` (sử dụng Recharts: AreaChart cho Revenue & PieChart cho Funnel, hiển thị Top Cards & Insights Panel).
- [ ] 4. Cập nhật `frontend/client/src/pages/admin/crm/leads.tsx`:
       - Thêm state `viewMode` để chuyển đổi qua lại giữa List / Kanban / Báo cáo.
       - Tách biệt/điều chỉnh tham số fetching React Query (ví dụ: limit 100 cho Kanban, limit 10 cho List).
       - Tích hợp mutation cập nhật Lead sử dụng **Optimistic Update** cho trạng thái kéo thả mượt mà.
- [ ] 5. Chạy kiểm tra TypeScript và Build để chắc chắn 0 lỗi:
       - `npm run check` (hoặc build frontend).

---
Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
