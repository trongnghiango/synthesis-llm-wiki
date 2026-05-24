---
id: arch-tenant-isolation-casing-fix
title: Chuẩn hóa Casing Quyền và Vá Lỗ hổng Cô lập Tenant CRM
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
  - "[[hb-drizzle-base-repo]]"
summary: "Chuẩn hóa so sánh role bằng toUpperCase, loại bỏ fallback tenant ID nguy hiểm tại CRM Controllers và tích hợp applyTenantIsolation tự động."
tags: [security, tenant-isolation, authorization, drizzle-orm, crm]
---

### 1. Chuẩn hóa Casing Quyền (`VisibilityResolverService`)
- **Logic:** Chuyển đổi role strings sang `.toUpperCase()` trước khi so sánh với các hằng số hệ thống (`'ADMIN'`, `'SUPER_ADMIN'`, `'MANAGER'`).
- **Mục tiêu:** Đảm bảo tính tương thích ngược và ngăn chặn lỗi phân quyền do bất đồng bộ casing giữa JWT/CSDL và logic nghiệp vụ.

### 2. Loại bỏ Fallback Bảo mật Nguy hiểm (`|| 1`) tại CRM Controllers
- **Phạm vi áp dụng:** `ContractController`, `QuoteController`, `LeadController`, `OrganizationController`.
- **Cơ chế kiểm soát:**
  - Ném ngay `ForbiddenException` nếu request từ người dùng bên ngoài thiếu `organizationId` hợp lệ (thay vì tự động đưa về Tổ chức `1` - Platform Owner).
  - **Tệp đính kèm (Attachment Upload):** Cho phép fallback về thư mục hệ thống `1` của STAX duy nhất khi `isInternal === true`. Người dùng bên ngoài không hợp lệ sẽ bị chặn ngay lập tức.

### 3. Tự động hóa Cô lập Dữ liệu (`DrizzleContractRepository`)
- Áp dụng hàm dùng chung `this.applyTenantIsolation(conditions, schema.contracts)` kế thừa từ `[[hb-drizzle-base-repo]]`.
- Tận dụng Request Context (JWT/ALS) từ `[[arch-als-tenant-isolation]]` để tự động lọc theo Tenant, đồng thời hỗ trợ tài khoản Platform Owner (`scope: 'ALL'`) truy vấn chéo toàn bộ dữ liệu.

### 4. Giải quyết Xung đột Kiểu Dữ liệu Multer File
- Khai báo kiểu dữ liệu tham số file upload ở Controller từ `Express.Multer.File` thành `any`.
- Triệt tiêu hoàn toàn lỗi biên dịch TypeScript cục bộ (`Namespace 'global.Express' has no exported member 'Multer'`) mà không ảnh hưởng tới luồng xử lý runtime.