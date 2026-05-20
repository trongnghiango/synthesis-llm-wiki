# Kế hoạch Kiến trúc Chi tiết Backend (01_be_implementation_plan.md)
**Feature:** CRM Lead Stage Transition (Kanban Support) & Reports
**Date:** 2026-05-20

## A. Database Schema
Không cần thay đổi Database Schema. Bảng `leads` hiện có cột `status` kiểu `lead_status` enum, đã có đầy đủ các giá trị và index tương ứng cho hiệu năng tốt.

## B. Domain Layer
Domain Entity `Lead` (`backend/src/modules/crm/domain/entities/lead.entity.ts`) đã có sẵn phương thức nghiệp vụ:
- `transitionTo(newStage: LeadStage): void`
Phương thức này thực hiện thay đổi trạng thái trong Entity một cách an toàn.

## C. Infrastructure Layer
- **Schema & Mapper:** Mapper `LeadMapper` (`backend/src/modules/crm/infrastructure/mappers/lead.mapper.ts`) đã ánh xạ thuộc tính `status` ở DB sang `stage` trong Domain.
- Không cần thay đổi Mapper hay Repository.

## D. Application Layer
Chúng ta sẽ bổ sung logic thay đổi trạng thái Lead vào phương thức `updateLeadInfo` của `LeadWorkflowService` (`backend/src/modules/crm/application/services/lead-workflow.service.ts`):

```typescript
// 1. Kiểm tra sự thay đổi trạng thái (status) từ UpdateLeadRequestDto
const oldStage = lead.stage;
let stageChanged = false;

if (dto.status && dto.status !== lead.stage) {
    // 2. Chặn việc chuyển đổi sang WON trực tiếp từ API cập nhật thường
    if (dto.status === LeadStage.WON) {
        throw new BusinessRuleValidationException(
            'Để chốt WON Lead và tạo hợp đồng, vui lòng sử dụng API close-won dành riêng.'
        );
    }
    
    // 3. Thực hiện chuyển đổi trạng thái trong Entity
    lead.transitionTo(dto.status as LeadStage);
    stageChanged = true;
}

// 4. Lưu Lead
await this.leadRepo.save(lead);

// 5. Phát hành sự kiện sau khi lưu thành công (ngoài Transaction nếu có, hoặc bình thường qua eventBus)
if (stageChanged) {
    await this.eventBus.publish(
        new LeadStatusChangedEvent(lead, oldStage, lead.stage, actorId, actorName)
    );
}
```

## E. Presentation Layer & Contracts
- **Shared Contracts:** `updateLeadSchema` trong `shared/contracts/crm.ts` đã có sẵn trường `status: z.string().optional()`.
- **Request DTO:** `UpdateLeadRequestDto` đã có sẵn trường `status?: string;`.
- Do đó không cần sửa đổi Presentation Layer/DTO/Zod.

## F. Verification Plan
### Automated Tests
- Chạy unit test của `LeadWorkflowService` để kiểm tra logic đổi trạng thái và chặn `WON`:
  `npm run test backend/src/modules/crm/application/services/lead-workflow.service.spec.ts`

---
Thiết kế này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
