# Báo cáo Thực thi Frontend (03_fe_walkthrough.md)
**Feature:** CRM Kanban Board & Reports Dashboard
**Date:** 2026-05-20

## 1. Tóm tắt giao diện (UI Summary)
- **View Switcher:** Nút chuyển đổi (Danh sách / Kanban / Báo cáo) được đặt ngay trên thanh PageHeader của trang Leads CRM.
- **Kanban View:**
  - 5 cột tương ứng với các giai đoạn: Mới (NEW), Đang tư vấn (CONSULTING), Thương lượng (NEGOTIATING), Thành công (WON), Thất bại (LOST).
  - Mỗi cột hiển thị số lượng lead và tổng giá trị dự kiến bằng đồng VNĐ.
  - Hỗ trợ kéo thả mượt mà với hiệu ứng động từ `framer-motion`.
  - Kéo sang WON sẽ kích hoạt mở Dialog Chốt hợp đồng để hoàn tất tạo hợp đồng/phiếu thu.
  - Các lead không được cấp quyền edit (`_actions.edit.allowed === false`) sẽ bị chặn kéo thả và có biểu tượng khóa cảnh báo.
- **Reports Dashboard:**
  - 4 thẻ thống kê: Tổng số lead, Báo giá, Hợp đồng, Doanh thu với nhãn xu hướng và màu sắc trực quan.
  - Biểu đồ tăng trưởng doanh thu & số lượng hợp đồng (Recharts Area + Bar Chart).
  - Biểu đồ cơ cấu nguồn lead (Recharts Pie Chart).
  - Bảng cảnh báo việc cần xử lý khẩn cấp (Insights) cho các trường hợp: Lead chưa phân phối, Báo giá chờ duyệt, Hợp đồng sắp hết hạn.

## 2. Quyết định kỹ thuật (Technical Decisions)
- **Optimistic Updates:** Sử dụng React Query cache manipulation trên mutation đổi trạng thái. Khi người dùng kéo thả card, card sẽ nhảy sang cột mới ngay lập tức mà không có độ trễ mạng (Zero-Latency). Nếu API trả về lỗi, hệ thống tự động rollback card về vị trí cũ và hiển thị Toast thông báo.
- **HTML5 Drag and Drop API:** Tận dụng API kéo thả gốc của trình duyệt giúp ứng dụng siêu nhẹ, không cần cài đặt các thư viện nặng nề bên thứ ba như react-beautiful-dnd.
- **Tận dụng lại Close Won Dialog:** Kéo sang WON sẽ gọi lại hàm `handleOpenWonDialog` đã có sẵn, giúp tận dụng tối đa logic form, schema validation (zod) và tự động tạo phiếu thu tài chính.

## 3. Khó khăn & Xử lý (Troubleshooting)
- **TypeScript & Badge Variants:** Khắc phục lỗi type badge variant `success` bằng cách chuyển sang `variant="outline"` kết hợp styling CSS trực tiếp qua `cn()` helper để hiển thị màu sắc theo thiết kế.
- **ResponsiveContainer h="100%":** Thay thế thuộc tính `h` thành `height` trên các component của Recharts để đảm bảo render đúng chuẩn HTML5 & SVG container.

## 4. Tự đánh giá & Bài học (Self-Review & Retrospective)
- **Đạt được:** Hoàn thành giao diện Kanban mượt mà, trực quan hóa dữ liệu sinh động và báo cáo hữu ích đáp ứng xuất sắc yêu cầu Sprint 03.
- **Bài học:** Việc phân tách các component hiển thị (`LeadKanbanBoard`, `LeadReportsDashboard`) ra khỏi file page chính (`leads.tsx`) giúp code sạch sẽ, dễ bảo trì và dễ dàng test độc lập.
