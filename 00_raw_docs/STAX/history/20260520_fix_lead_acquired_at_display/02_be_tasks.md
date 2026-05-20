# Bước 3️⃣: Checklist Thực thi (fix_lead_acquired_at_display)

- [x] 1. Thêm trường `acquiredAt` vào `LeadResponseDto` (`backend/src/modules/crm/infrastructure/dtos/lead.response.dto.ts`)
- [x] 2. Cập nhật `LeadQueryService.mapToResponse` để map và trả về `acquiredAt` (`backend/src/modules/crm/application/services/lead-query.service.ts`)
- [x] 3. Chạy build backend để đảm bảo không lỗi TypeScript compile (`pnpm run build` trong `backend`)
- [x] 4. Chạy script test `check-leads-dates.ts` hoặc kiểm tra API thực tế để xác nhận dữ liệu đã có `acquiredAt`

---
Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
