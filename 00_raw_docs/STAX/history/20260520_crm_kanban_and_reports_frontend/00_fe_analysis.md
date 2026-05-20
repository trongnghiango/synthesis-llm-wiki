# Phân tích UI/UX Frontend (00_fe_analysis.md)
**Feature:** CRM Kanban Board & Reports Dashboard
**Date:** 2026-05-20

## 1. Mục tiêu UX
- **Chuyển đổi View nhanh:** Tích hợp nút chuyển đổi giữa 3 chế độ xem: **Danh sách (List)**, **Kanban Board** và **Báo cáo (Reports)** trực tiếp tại trang Leads, giúp lưu giữ nguyên trạng thái tìm kiếm/bộ lọc hiện tại.
- **Tương tác kéo thả mượt mà:** Kéo thả thẻ Lead để đổi trạng thái nhanh.
  - Hỗ trợ chuyển đổi trạng thái: `NEW`, `CONSULTING`, `NEGOTIATING`, `LOST`.
  - Nếu kéo thả sang cột `WON` (Thành công): Kích hoạt mở Dialog chốt hợp đồng (Close Won Dialog) có sẵn để đảm bảo đầy đủ thông tin nghiệp vụ.
  - Phục hồi lại trạng thái kéo cũ nếu API báo lỗi (Rollback on Error).
  - Không cho phép kéo thả đối với các thẻ Lead có `_actions.edit.allowed === false`.
- **Trực quan hóa dữ liệu:** Hiển thị số liệu trực quan bằng biểu đồ Recharts (Biểu đồ tròn về nguồn lead, biểu đồ vùng về doanh thu & hợp đồng) và bảng cảnh báo việc cần làm khẩn cấp (Insights).

## 2. Luồng dữ liệu (Data Flow) & Trạng thái (State Management)
- **React Query:**
  - Danh sách Lead được quản lý bởi `queryKeys.crm.leads`. Chúng ta sẽ điều chỉnh tham số `limit: 100` khi xem chế độ Kanban để có thể tải đủ các Lead mà không bị cắt trang quá ngắn.
  - Các thống kê Dashboard được quản lý bởi 3 truy vấn riêng biệt:
    - `/dashboard/stats` -> Thẻ chỉ số.
    - `/dashboard/charts/revenue` -> Biểu đồ doanh thu/leads.
    - `/dashboard/insights` -> Danh sách cảnh báo.
- **Zustand:** Chỉ sử dụng cho các cấu hình giao diện chung (nếu cần), các trạng thái view chuyển đổi được quản lý qua URL query params (để hỗ trợ chia sẻ link/bookmark) hoặc local state.

## 3. Phân chia Component
- `LeadList` (Page Component gốc): Quản lý view switcher và các dialog (intake, close won).
- `LeadKanbanBoard`: Component hiển thị Kanban với 5 cột.
- `LeadKanbanColumn`: Cột tương ứng với từng giai đoạn (đếm số lượng, tổng expected value).
- `LeadKanbanCard`: Thẻ Lead hiển thị tóm tắt thông tin (Khách hàng, nhu cầu, giá trị, nguồn, người phụ trách, nhãn ngày).
- `LeadReportsDashboard`: Hiển thị các widgets thống kê và biểu đồ Recharts.

---
Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc FE.
