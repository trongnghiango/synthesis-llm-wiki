# Tasks Checklist - CRM & Accounting Tenant Isolation Fix

## 📋 Checklist

- [ ] **Task 0: Upgrade Base Repository**
  - [ ] Modify `backend/src/core/shared/infrastructure/persistence/drizzle-base.repository.ts` to identify and isolate the `organizations` table via `table.id` when `'organizationName' in table`.

- [ ] **Task 1: CRM Repositories Isolation**
  - [ ] `DrizzleOrganizationRepository.ts`: Integrate `applyTenantIsolation` in `findById` and `findAll`.
  - [ ] `DrizzleLeadRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, `findByContactId`, `findMany`, and `count`.
  - [ ] `DrizzleQuoteRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, `findByLeadId`, and `count`.
  - [ ] `DrizzleContactRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, `findByEmail`, and `count`.
  - [ ] `DrizzleAssignmentRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, `findByEmployeeId`, `findByServiceId`, and `count`.

- [ ] **Task 2: HRM/Employee Repositories Isolation**
  - [ ] `DrizzleEmployeeRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, `findByCode`, `findByUserId`, and `count`.
  - [ ] `DrizzleEmployeeTaskRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, `findByEmployeeId`, and `count`.
  - [ ] `DrizzleOrgStructureRepository.ts`: Integrate `applyTenantIsolation` across all organizational unit, position, grade, and job title queries.

- [ ] **Task 3: Accounting Repositories Isolation**
  - [ ] `DrizzleFinoteRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, `findByCode`, and `count`.
  - [ ] `DrizzleCashFundRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, and `findByCode`.
  - [ ] `DrizzleAccountRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, and `findByCode`.
  - [ ] `DrizzleJournalRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, and `findByCode`.
  - [ ] `DrizzleFinotePaymentRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, and `findByFinoteId`.

- [ ] **Task 4: System & Notification Repositories Isolation**
  - [ ] `DrizzleAttachmentRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, and `findByEntity`.
  - [ ] `DrizzleNotificationRepository.ts`: Integrate `applyTenantIsolation` in `findAll`, `findById`, and `findByUserId`.

- [ ] **Task 5: Verification & Verification Checks**
  - [ ] Run backend compile checks (`pnpm run build` or equivalent) to confirm 0 compilation errors.
  - [ ] Run backend unit and integration tests (`npm run test`) to ensure all assertions pass.

- [ ] **Task 6: Documentation & Changelog**
  - [ ] Document changes in `docs/06_CHANGELOG.md`.
