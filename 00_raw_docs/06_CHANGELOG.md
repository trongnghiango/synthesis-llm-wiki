# STAX V2 Changelog

Lưu trữ lịch sử các thay đổi nhỏ, sửa lỗi, và micro-features trong hệ thống STAX.

### [2026-05-20] - Sửa lỗi pgEnum Mismatch khi Cập nhật Trạng thái Lead

- **Module:** `crm`
- **Thay đổi:**
  - Cập nhật `LeadMapper` (`backend/src/modules/crm/infrastructure/mappers/lead.mapper.ts`) để ánh xạ chính xác giữa Domain enum `LeadStage` (`CONSULTING`, `NEGOTIATING`) và Database pgEnum `lead_status` (`CONTACTED`, `NEGOTIATION`).
  - Đã khắc phục lỗi `500 INTERNAL_SERVER_ERROR` khi kéo thả hoặc cập nhật trạng thái Lead.
  - Cập nhật hiển thị thời gian ở góc dưới trái thẻ Kanban từ `createdAt` (ngày hệ thống) sang `acquiredAt` (ngày tiếp nhận nghiệp vụ thực tế) để thông tin hiển thị chính xác hơn đối với dữ liệu import/seed.
  - Sửa lỗi API: Bổ sung trường `acquiredAt` vào `LeadResponseDto` và ánh xạ đầy đủ trong `LeadQueryService.mapToResponse` để Frontend nhận được giá trị `acquiredAt` thực tế từ cơ sở dữ liệu thay vì `undefined`.

