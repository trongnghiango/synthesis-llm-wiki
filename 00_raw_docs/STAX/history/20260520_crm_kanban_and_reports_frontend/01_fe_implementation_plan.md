# Kế hoạch Kiến trúc Frontend (01_fe_implementation_plan.md)
**Feature:** CRM Kanban Board & Reports Dashboard
**Date:** 2026-05-20

## A. Contract Sync
Chúng ta đồng bộ dữ liệu thông qua Zod Contract:
- API cập nhật Lead: gửi lên `{ status: string }` tương thích với `updateLeadSchema` có sẵn.
- Đối tượng `Lead` chứa trường `stage` (NEW, CONSULTING, NEGOTIATING, WON, LOST) và `_actions` để check phân quyền.

## B. API Client (React Query hooks)
Bổ sung các hàm gọi API thống kê vào `crmApi` (`frontend/client/src/modules/crm/api/crm.api.ts`):
- `getStats: (orgId?: number) => apiRequest<any>("GET", withQuery("/dashboard/stats", orgId ? { organizationId: orgId } : {}))`
- `getCharts: () => apiRequest<any>("GET", "/dashboard/charts/revenue")`
- `getInsights: () => apiRequest<any>("GET", "/dashboard/insights")`

Định nghĩa các React Query hook tương ứng:
- `useCrmStats(orgId)`
- `useCrmCharts()`
- `useCrmInsights()`

## C. Component Tree & UI Structure
```
Leads Page (/admin/crm/leads)
  ├── PageHeader (Chứa nút Switcher: List | Kanban | Reports và Nút Tạo Lead)
  ├── Dialogs (Intake Form & Close Won Form)
  ├── IF viewMode === 'list'
  │     └── DataGrid (Bảng danh sách như hiện tại)
  ├── IF viewMode === 'kanban'
  │     └── LeadKanbanBoard (Grid 5 cột)
  │           └── LeadKanbanColumn (NEW, CONSULTING, NEGOTIATING, WON, LOST)
  │                 └── LeadKanbanCard (Khách hàng, Expected Value, Source, Phone, Date)
  └── IF viewMode === 'reports'
        └── LeadReportsDashboard
              ├── Stats Cards Grid (Tổng lead, báo giá, hợp đồng, doanh thu)
              ├── Charts Grid (AreaChart cho Revenue & PieChart cho Funnel/Source)
              └── Insights Checklist Panel (Cảnh báo việc cần làm)
```

## D. State Management & Optimistic Updates
Để tạo hiệu ứng kéo thả tức thì (Zero-Latency), chúng ta sử dụng **Optimistic Updates** trong React Query cho mutation cập nhật trạng thái Lead:
- **onMutate:** Hủy bỏ các query đang chạy, lưu giữ dữ liệu cache cũ làm backup. Sau đó cập nhật trực tiếp cache `queryKeys.crm.leads` đổi trạng thái của lead sang cột mới.
- **onError:** Phục hồi (Rollback) lại cache cũ nếu cuộc gọi API thất bại.
- **onSettled:** Invalidate queries để đồng bộ dữ liệu mới nhất từ server.

---
Thiết kế này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
