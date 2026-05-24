# Implementation Plan: Tenant Isolation & Casing Fix

**Ngày kế hoạch:** 2026-05-23
**Handoff Plan:** `lively-crafting-trinket.md`
**Chế độ:** Handoff của Backend (`stax-backend`)

---

## 1. Shared Contracts
Trong nhiệm vụ này, các cấu trúc dữ liệu không có sự thay đổi về Schema DTO hay API Contract được chia sẻ với Frontend, do đó không cần cập nhật các file Zod tại `shared/contracts/`.

---

## 2. Database Schema
Không có thay đổi về Schema Cơ sở dữ liệu hay `pgEnum` mới. Các schema hiện tại của `contracts`, `quotes`, `leads`, `organizations` được giữ nguyên.

---

## 3. Quy trình thực hiện chi tiết cho các file

### A. Sửa đổi `visibility-resolver.service.ts` (Domain Core - User Module)
- **Mục tiêu:** Sửa lỗi so sánh casing vai trò người dùng.
- **Chi tiết thay đổi:**
  Chuyển toàn bộ vai trò người dùng trong danh sách `user.roles` thành chữ in hoa (`toUpperCase()`) trước khi so sánh với `'ADMIN'`, `'SUPER_ADMIN'`, và `'MANAGER'`.
  ```typescript
  const upperRoles = roles.map(r => r.toUpperCase());
  if (upperRoles.includes('ADMIN') || upperRoles.includes('SUPER_ADMIN') || upperRoles.includes('MANAGER')) {
    return { userType: 'INTERNAL', scope: 'ALL', allowedOrganizationIds: [] };
  }
  ```

### B. Siết chặt fallback bảo mật trong các CRM Controllers (Presentation Layer)
Chúng ta sẽ import `ForbiddenException` từ `@nestjs/common` để ném ra Exception phù hợp khi thiếu `organizationId`.

#### 1. `contract.controller.ts`
- **Mục tiêu:** Loại bỏ fallback `|| 1` nguy hiểm cho người dùng bên ngoài.
- **Logic cập nhật:**
  ```typescript
  const user = req.user;
  const roles: string[] = user?.roles || [];
  const upperRoles = roles.map(r => r.toUpperCase());
  const isSuperAdmin = upperRoles.includes('SUPER_ADMIN');
  const isPlatformLeader = user?.organizationId === 1 && 
      upperRoles.some(r => ['ADMIN', 'CEO', 'DIR', 'MANAGER'].includes(r));

  let tenantId = user?.organizationId;
  if (!tenantId) {
      if (isSuperAdmin || isPlatformLeader) {
          tenantId = 1;
      } else {
          throw new ForbiddenException('Không tìm thấy thông tin tổ chức hợp lệ.');
      }
  }

  // Cho phép ghi đè tenantId từ query nếu là Super Admin hoặc Platform Leader
  if (isSuperAdmin || isPlatformLeader) {
      tenantId = orgId ? parseInt(orgId) : tenantId;
  }
  ```
  *(Áp dụng logic kiểm tra tương tự ở các endpoint `getContracts`, `getContractDetail`, `activateContract`, `suspendContract`, `terminateContract`, `uploadAttachment`, `generatePdf`)*

#### 2. `quote.controller.ts`, `lead.controller.ts`, và `organization.controller.ts` (Upload Attachment)
- **Mục tiêu:** Ngăn chặn việc ghi tệp tin đính kèm trái phép vào Org 1 nếu không phải là nhân sự nội bộ của STAX.
- **Logic cập nhật:**
  ```typescript
  let tenantId = currentUser?.organizationId; // hoặc user?.organizationId
  if (!tenantId) {
      if (currentUser?.isInternal) { // hoặc user?.isInternal
          tenantId = 1;
      } else {
          throw new ForbiddenException('Tài khoản không thuộc về bất kỳ doanh nghiệp nào để tải lên.');
      }
  }
  ```

### C. Tích hợp `applyTenantIsolation` vào `drizzle-contract.repository.ts` (Persistence Layer)
- **Mục tiêu:** Chuyển đổi từ cơ chế lọc `orgId > 1` thủ công sang tự động lọc theo `applyTenantIsolation`.
- **Logic cập nhật:**
  Sử dụng `this.applyTenantIsolation(conditions, schema.contracts)` thay cho các điều kiện thủ công:
  - Trong `findById(id, orgId)`
  - Trong `findDetailById(id, orgId)`
  - Trong `findMany(filter, orgId)`
  Bằng cách này, nếu tài khoản có `scope: 'ALL'` (Platform Owner), `applyTenantIsolation` sẽ tự động bỏ qua mệnh đề lọc `organizationId`, cho phép họ truy vấn chéo toàn bộ dữ liệu hợp đồng đúng như yêu cầu của người dùng.

---

Vui lòng gõ 'OK' để tôi tiến hành xuất Tasks Checklist.
