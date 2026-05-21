---
id: dom-crm-kanban-reports-fe
title: "Frontend CRM Kanban & Báo cáo Dashboard"
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Thiết kế và giải pháp kỹ thuật frontend cho Kanban Board kéo thả và Dashboard báo cáo CRM."
tags: [frontend, crm, kanban, dashboard, react-query, drag-drop]
---

### 1. Kiến trúc Component & Luồng Nghiệp vụ
*   **Phân rã Component**: Tách biệt `LeadKanbanBoard` và `LeadReportsDashboard` ra khỏi file page chính `leads.tsx`.
*   **Trạng thái Kanban**: Gồm 5 cột (`NEW`, `CONSULTING`, `NEGOTIATING`, `WON`, `LOST`).
    *   Kiểm tra phân quyền: Chặn kéo thả đối với các lead có `_actions.edit.allowed === false`.
    *   Tích hợp Tài chính: Kéo sang `WON` kích hoạt Dialog Chốt hợp đồng để tự động tạo `[[dom-accounting-finote]]`.

### 2. Giải pháp Kỹ thuật & State Management
*   **Kéo thả Native**: Sử dụng trực tiếp HTML5 Drag and Drop API kết hợp `framer-motion` thay vì dùng các thư viện bên thứ ba cồng kềnh.
*   **Optimistic Updates**: Sử dụng React Query cache manipulation trên mutation đổi trạng thái để đạt hiệu ứng Zero-Latency. Tự động rollback dữ liệu cũ và hiện Toast thông báo nếu API trả về lỗi.

### 3. Khắc phục Sự cố Kỹ thuật (Troubleshooting)
*   **Recharts ResponsiveContainer**: Chuyển đổi thuộc tính `h="100%"` thành `height` để đảm bảo tương thích hoàn toàn với SVG container.
*   **Badge Variant Type**: Khắc phục lỗi type badge variant `success` bằng cách chuyển sang `variant="outline"` kết hợp `cn()` helper để tùy biến CSS tailwind.