# Business Analysis - CRM & Accounting Tenant Isolation Fix

## 📋 Context & Objectives
During the multi-tenant audit of the STAX platform, we identified a critical vulnerability in how multi-tenancy is handled at the database persistence layer (specifically using Drizzle ORM):

1. **Organization Table Isolation Leak**:
   The base class `DrizzleBaseRepository` implements automatic tenant isolation via ALS context by checking if `organizationId` is a property of the table. However, the `organizations` table itself doesn't have an `organizationId` column. Instead, it has a primary key `id` which represents the tenant ID. As a result, the automatic `applyTenantIsolation` bypasses the `organizations` table completely.
   This allows external/assigned users to query and fetch all tenant organizations across the platform (e.g. calling `findAll` or `findById` on organizations they do not belong to).

2. **Manual and Inconsistent Isolation in CRM, Accounting, HRM/Employee, and System Repositories**:
   Multiple repositories under Phân khu 3 (CRM) and Phân khu 4 (Accounting & HRM/Employee) either lack tenant isolation completely or filter manually in inconsistent ways.
   
Our objective is to implement the **approved Approach B**:
- Upgrade `DrizzleBaseRepository.applyTenantIsolation` to intelligently detect and filter the `organizations` table by `table.id` (checking for a distinguishing property like `organizationName` in the table schema object).
- Systematically integrate `this.applyTenantIsolation(conditions, table)` across all tenant-bound repositories in Phân khu 3, Phân khu 4, and System/Notification modules.
- Ensure Platform Owner (scope `ALL`) can still view all data as authorized.

## 👥 Target Users & Segments
1. **Platform Owner (STAX Admin)**: Authenticated user with scope `ALL` who needs to oversee and manage all organizations, customers, and operations without restriction.
2. **Tenant Admin**: Authenticated user with scope `SELF_ONLY` who must only see data matching their own `organizationId`.
3. **Tenant Employee/Agent**: Authenticated user with scope `ASSIGNED_ONLY` who should only access records under organization IDs they are assigned/permitted to access.

## 📖 Ubiquitous Language & Mapping
- **Organization (Tổ chức / Doanh nghiệp)** ↔ `schema.organizations` / `id` (represents the Tenant)
- **Lead (Cơ hội kinh doanh)** ↔ `schema.leads` / `organizationId`
- **Quote (Báo giá)** ↔ `schema.quotes` / `organizationId`
- **Contact (Người liên hệ)** ↔ `schema.contacts` / `organizationId`
- **Service Assignment (Giao dịch dịch vụ)** ↔ `schema.serviceAssignments` / `organizationId`
- **Employee (Nhân viên)** ↔ `schema.employees` / `organizationId`
- **Employee Task (Công việc nhân viên)** ↔ `schema.employeeTasks` / `organizationId`
- **Org Structure Entities (Sơ đồ tổ chức - units, positions, grades, jobTitles, locations)** ↔ `schema.orgUnits`, `schema.positions`, `schema.grades`, `schema.jobTitles`, `schema.locations` / `organizationId`
- **Cash Fund (Quỹ tiền mặt)** ↔ `schema.cashFunds` / `organizationId`
- **Account (Tài khoản kế toán)** ↔ `schema.accounts` / `organizationId`
- **Finote (Phiếu thu/chi)** ↔ `schema.finotes` / `organizationId`
- **Journal (Nhật ký chung)** ↔ `schema.journals` / `organizationId`
- **Finote Payment (Thanh toán)** ↔ `schema.finotePayments` / `organizationId`
- **Attachment (Tệp đính kèm)** ↔ `schema.attachments` / `organizationId`
- **Notification (Thông báo)** ↔ `schema.notifications` / `organizationId`

## 🛡️ Guardrails & Safety Protocols
- **Domain Purity**: Keep all domain entities free of ORM and NestJS decorator imports.
- **ALS Safety**: If there is no Active Request Context (e.g. running in background queues, cron tasks), `applyTenantIsolation` must fail safe or default to no-op if context is absent, ensuring explicit invocation of `RequestContextService.run` is used for background context.
- **Fail-Closed Strategy**: For `ASSIGNED_ONLY` users with no assigned organization IDs, we must explicitly push a non-existent ID filter (`eq(columnToFilter, -1)`) rather than allowing full access or throwing silent errors.
