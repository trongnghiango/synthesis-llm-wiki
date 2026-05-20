# Checklist Thực thi Backend (02_be_tasks.md)
**Feature:** CRM Lead Stage Transition (Kanban Support) & Reports
**Date:** 2026-05-20

## Danh sách công việc thực thi:
- [ ] 1. Cập nhật `LeadWorkflowService.updateLeadInfo` trong file `backend/src/modules/crm/application/services/lead-workflow.service.ts` để tích hợp đổi trạng thái `status` và phát hành sự kiện `LeadStatusChangedEvent`.
- [ ] 2. Cập nhật Unit Test trong `backend/src/modules/crm/application/services/lead-workflow.service.spec.ts` để kiểm định tính đúng đắn của logic đổi trạng thái và logic chặn chốt `WON`.
- [ ] 3. Chạy unit test để kiểm tra logic:
       `npm run test backend/src/modules/crm/application/services/lead-workflow.service.spec.ts`
- [ ] 4. Chạy toàn bộ build hệ thống để đảm bảo 0 lỗi TypeScript:
       `npm run build` ở thư mục backend.

---
Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
