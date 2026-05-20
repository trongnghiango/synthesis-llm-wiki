## 1. Tóm tắt tính năng (Feature Summary)
- **Tier**: Tier 3 — Process Flow (CRM Module)
- **Endpoints đã sửa đổi**: `GET /crm/leads` và `GET /crm/leads/:id` để trả về `acquiredAt` của Leads.
- **Tables/Enums mới**: Không có.

## 2. Quyết định kiến trúc (Architecture Decisions)
- Sửa đổi `LeadResponseDto` để đồng bộ với Domain Entity và Database Schema, giúp trả về đúng ngày tiếp nhận thực tế (`acquiredAt`) thay vì fallback về ngày tạo hệ thống (`createdAt`).
- Việc gán fallback cho `acquiredAt || createdAt` đã có sẵn ở UI Frontend (`LeadKanbanBoard.tsx`), do đó việc trả về đúng dữ liệu `acquiredAt` từ API sẽ sửa triệt để việc hiển thị ngày giống nhau trên thẻ Kanban.

## 3. Khó khăn & Xử lý (Troubleshooting)
- Không có lỗi nào phát sinh. Build thành công `0` error.

## 4. Bàn giao cho Frontend (Frontend Handoff)
- **File Contract Zod**: `shared/contracts/crm.ts` (đã có sẵn `acquiredAt?: string`, không cần cập nhật).
- API trả về thuộc tính `acquiredAt` định dạng ISO string. Thẻ Kanban trên frontend sẽ tự động nhận diện và hiển thị chính xác.
