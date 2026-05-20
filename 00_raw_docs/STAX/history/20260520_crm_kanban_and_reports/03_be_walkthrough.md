# Báo cáo Thực thi Backend (03_be_walkthrough.md)
**Feature:** CRM Lead Stage Transition (Kanban Support) & Reports
**Date:** 2026-05-20

## 1. Tóm tắt tính năng (Feature Summary)
- **Tier:** 3 (Process Flow) — Module CRM
- **Endpoints đã bổ sung/cập nhật:**
  - `PATCH /crm/leads/:id`: Đã được cập nhật để chấp nhận trường `status` (kiểu string) trong payload DTO, cho phép chuyển đổi giai đoạn nghiệp vụ của Lead.
- **Tables/Enums mới:** Không có (sử dụng schema leads hiện tại).

## 2. Quyết định kiến trúc (Architecture Decisions)
- **Mở rộng API hiện tại:** Thay vì tạo thêm một endpoint chuyên biệt (như `/crm/leads/:id/stage`), chúng ta sử dụng trực tiếp API `PATCH /crm/leads/:id` để giữ thiết kế Restful tinh gọn.
- **Ràng buộc nghiệp vụ chốt WON:** Kiểm tra trong Service: nếu kéo thả sang `WON`, chặn trực tiếp và trả về lỗi `BusinessRuleValidationException` yêu cầu frontend phải gọi qua API `close-won` chuyên dụng (đảm bảo tạo hợp đồng và phiếu thu đồng thời).
- **Domain Event:** Sự thay đổi trạng thái Lead kích hoạt phát hành `LeadStatusChangedEvent` sau khi lưu thành công vào cơ sở dữ liệu. Sự kiện này được hệ thống Audit Log đăng ký lắng nghe và tự động ghi nhật ký lịch sử thay đổi.

## 3. Khó khăn & Xử lý (Troubleshooting)
- **Nghiệp vụ Mapping:** Database sử dụng trường `status` trong khi Domain Entity sử dụng `stage`. Chúng ta đã xử lý đồng bộ này thông qua `LeadMapper` và tích hợp ánh xạ `status` trong DTO một cách đồng nhất, giúp phía Frontend không cần thay đổi Zod schema.

## 4. Bàn giao cho Frontend (Frontend Handoff)
- **Shared Contracts:** `shared/contracts/crm.ts` đã có `status: z.string().optional()` trong `updateLeadSchema`.
- **API Call:** Frontend thực hiện gọi:
  ```typescript
  crmApi.updateLead(leadId, { status: newStage })
  ```
  Trong đó `newStage` thuộc các giá trị `NEW`, `CONSULTING`, `NEGOTIATING`, `LOST`. Nếu muốn chuyển sang `WON`, phải sử dụng luồng dialog gọi API `/crm/leads/:id/won`.
