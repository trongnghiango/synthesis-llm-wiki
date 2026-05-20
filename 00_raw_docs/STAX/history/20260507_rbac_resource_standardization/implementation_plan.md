# Implementation Plan - RBAC Fix & Standardization

## Goal
Fix the `Permission denied: employee:read` error for the `ADMIN` role by aligning seed data with the codebase and enhancing permission matching logic.

## Proposed Changes

### [MODIFY] [01_rbac_rules.csv](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/database/seeds/01_rbac_rules.csv)
- Split `hrm` resource into `employee` and `org`.
- Assign `ADMIN` full access (`*`) to both.
- Align `MANAGER`, `STAFF`, and other roles.

### [MODIFY] [permission.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/rbac/application/services/permission.service.ts)
- Update `checkPermissionMatch` to treat `manage` action as a wildcard.

### [MODIFY] [bootstrap.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/system/application/services/bootstrap.service.ts)
- Sync UI flags (`canManageHRM`, etc.) with new resource names.

## Verification
- Verify `ADMIN` can access `/api/hrm/employees`.
- Check UI flags in `/api/system/bootstrap`.
