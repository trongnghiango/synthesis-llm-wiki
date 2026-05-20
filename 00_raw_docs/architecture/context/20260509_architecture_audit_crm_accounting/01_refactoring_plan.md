# STAX Refactoring Plan: CRM Identity & Accounting Isolation
Date: 2026-05-09
Status: Pending Review

## 1. Goal Description
Resolve the identity collision in CRM where new leads are incorrectly linked to existing organizations based only on phone numbers. Standardize the Finote creation logic to enforce tenant isolation and ensure data visibility. Clean up remaining legacy references to FinoteAttachment.

## 2. User Review Required
> [!IMPORTANT]
> **Identity Change:** Chúng ta sẽ thay đổi logic của `LeadIntakeService`. Nếu một SĐT đã tồn tại nhưng tên công ty (Organization Name) trong yêu cầu khác với công ty hiện tại của Contact đó, hệ thống sẽ **TẠO MỚI** Organization và Contact thay vì dùng lại cái cũ. Điều này có thể dẫn đến việc một SĐT xuất hiện ở nhiều Contact/Org khác nhau (đúng với thực tế kinh doanh).

## 3. Proposed Changes

### CRM Module (Identity Collision Fix)
---
#### [MODIFY] [lead-intake.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/application/services/lead-intake.service.ts)
- Sửa logic kiểm tra `existingContact`: Chỉ link vào Org cũ nếu tên Org trong DTO khớp hoặc trống.
- Nếu tên Org mới khác hoàn toàn, bắt buộc tạo Org mới và Contact mới để tránh trộn lẫn dữ liệu.

#### [MODIFY] [drizzle-organization.repository.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/infrastructure/persistence/drizzle-organization.repository.ts)
- Thêm phương thức `findByName(name: string)` để hỗ trợ kiểm tra chính xác hơn.

### Accounting Module (Isolation & Cleanup)
---
#### [MODIFY] [finote.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/accounting/application/services/finote.service.ts)
- Thay đổi logic `targetOrgId`: Ưu tiên `context.orgId` (Tổ chức của nhân viên đang thao tác) cho trường `source_org_id`.
- Chuyển `dto.organizationId` (ID khách hàng) vào một trường metadata hoặc trường `referenceOrgId` (nếu cần) để tránh làm nhiễu Tenant Isolation.

#### [MODIFY] [finote.controller.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/accounting/infrastructure/controllers/finote.controller.ts)
- Đảm bảo `user.organizationId` được truyền vào context một cách tường minh và an toàn.

#### [DELETE] [finote-attachment.entity.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/accounting/domain/entities/finote-attachment.entity.ts) (Double check and delete if still there).

## 4. Verification Plan

### Automated Tests
- Viết Unit Test cho `LeadIntakeService` với kịch bản: 2 Lead dùng chung 1 SĐT nhưng khác tên Công ty -> Kết quả phải là 2 Org riêng biệt.
- Viết Integration Test cho `FinoteService` để đảm bảo `source_org_id` luôn là Org của nhân viên tạo phiếu.

### Manual Verification
- Kiểm tra lại danh sách Finote sau khi chốt Won để đảm bảo phiếu thu hiện đúng ở Org 1 (Internal).
- Kiểm tra Database để xác nhận không còn dữ liệu rác hoặc gán sai Org.
