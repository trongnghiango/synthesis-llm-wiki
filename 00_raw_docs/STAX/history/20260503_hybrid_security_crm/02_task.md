# 📋 TASK RECORD: CHUẨN HÓA BẢO MẬT LAI CHO CRM MODULE

**Mã số:** 2026-05-03-001
**Nội dung:** Triển khai mô hình Pragmatic Hybrid Security cho module Leads.
**Trạng thái:** ✅ COMPLETED

---

## 📝 DANH SÁCH CÔNG VIỆC (CHECKLIST)

- [x] **Cập nhật DTO:** Mở rộng `LeadResponseDto` với `ActionableDto` và field `_actions`.
- [x] **Củng cố Layer 1:** Gắn `@Permissions` và `@UseGuards(PermissionGuard)` cho tất cả API trong `LeadController`.
- [x] **Xây dựng Layer 2:** Triển khai logic Multi-tenant Isolation tại `LeadQueryService` (Tự động lọc theo `organizationId`).
- [x] **Hoàn thiện Layer 3:** Viết logic phán xử hành động (`edit`, `assign`, `won`) dựa trên trạng thái Lead và định danh User ngay tại DTO Mapper.
- [x] **Bổ sung Endpoint:** Thêm API Detail (`GET /crm/leads/:id`) để hỗ trợ đầy đủ bộ phán xử hành động cho UI.
- [x] **Cập nhật Tài liệu:** Refactor [policy-engine-abac.md](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/docs/policy-engine-abac.md) thành chuẩn STAX Hybrid Security.

---

## 💡 GHI CHÚ KỸ THUẬT
*   Logic Ownership được xác định bằng cách so khớp `assignedPositionId` của Lead với `employee.id` của User hiện tại.
*   Admin STAX (Global Admin) được phép bypass lọc Layer 2 để xem toàn bộ dữ liệu (Ph vụ hỗ trợ/vận hành hệ thống).
