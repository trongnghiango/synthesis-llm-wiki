# Implementation Plan - CRM & Accounting Tenant Isolation Fix

## 🛠️ Architecture & Core Changes

### 1. `DrizzleBaseRepository.applyTenantIsolation` Upgrade
We will modify the core implementation of `applyTenantIsolation` inside `backend/src/core/shared/infrastructure/persistence/drizzle-base.repository.ts`.
- **Target check**: Check if `'organizationId' in table` OR `'organizationName' in table` (uniquely identifies the `organizations` table).
- **Column extraction**:
  - If `'organizationId' in table`, the isolation column is `table.organizationId`.
  - If `'organizationName' in table`, the isolation column is `table.id`.
- **No-op scenarios**: If neither property is in the table schema object, skip applying tenant isolation.

```typescript
protected applyTenantIsolation<T extends { organizationId?: any; id?: any }>(
  conditions: any[],
  table: T
): void {
  const hasOrgId = 'organizationId' in table;
  const isOrgTable = 'organizationName' in table;

  if (!hasOrgId && !isOrgTable) {
    return; // Not a tenant-isolated table
  }

  const visibility = RequestContextService.getContext()?.visibilityContext;
  if (!visibility) {
    return; // Fallback for context-less scenarios (crons, background tasks)
  }

  const columnToFilter = hasOrgId ? (table as any).organizationId : (table as any).id;

  if (visibility.scope === 'SELF_ONLY') {
    conditions.push(eq(columnToFilter, visibility.allowedOrganizationIds[0]));
  } else if (visibility.scope === 'ASSIGNED_ONLY') {
    if (visibility.allowedOrganizationIds.length > 0) {
      conditions.push(inArray(columnToFilter, visibility.allowedOrganizationIds));
    } else {
      conditions.push(eq(columnToFilter, -1)); // Block access
    }
  }
}
```

### 2. Repositories Integration Strategy
We will integrate `applyTenantIsolation` into the query pipeline (in where clauses) of all tenant repositories. The isolation filters must be pushed to a list of conditions and combined using `and(...conditions)`:

#### A. CRM Module Repositories:
- `DrizzleOrganizationRepository.ts`: Apply to `findAll`, `findById`. (Ensure only allowed organizations are queried).
- `DrizzleLeadRepository.ts`: Apply to `findAll`, `findById`, `findByContactId`, `findMany`.
- `DrizzleQuoteRepository.ts`: Apply to `findAll`, `findById`, `findByLeadId`, `count`.
- `DrizzleContactRepository.ts`: Apply to `findAll`, `findById`, `findByEmail`, `count`.
- `DrizzleAssignmentRepository.ts`: Apply to service assignments.

#### B. HRM/Employee Module Repositories:
- `DrizzleEmployeeRepository.ts`: Apply to `findAll`, `findById`, `findByCode`, `findByUserId`, etc.
- `DrizzleEmployeeTaskRepository.ts`: Apply to task querying.
- `DrizzleOrgStructureRepository.ts`: Apply to `locations`, `orgUnits`, `positions`, `grades`, `jobTitles`.

#### C. Accounting Module Repositories:
- `DrizzleFinoteRepository.ts`: Apply to `findAll`, `findById`, `count`.
- `DrizzleCashFundRepository.ts`: Apply to cash fund queries.
- `DrizzleAccountRepository.ts`: Apply to account queries.
- `DrizzleJournalRepository.ts`: Apply to journal queries.
- `DrizzleFinotePaymentRepository.ts`: Apply to payments.

#### D. System & Notification Modules:
- `DrizzleAttachmentRepository.ts`: Apply to attachment queries.
- `DrizzleNotificationRepository.ts`: Apply to notifications.

## 🛡️ Key Safety Measures
- **Explicit ANDs**: Always combine manual search filters and other criteria together with the tenant isolation condition in `and(...)`.
- **PLATFORM_OWNER Bypass**: Verified that when `visibility.scope === 'ALL'`, no isolation filters are added, enabling STAX Platform Owners to access all customer organizations and operations smoothly.
