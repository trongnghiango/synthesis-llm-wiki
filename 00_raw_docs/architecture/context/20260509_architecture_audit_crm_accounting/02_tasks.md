# Refactoring Tasks: CRM & Accounting Cleanup

- [x] **P1: CRM Identity Collision Fix**
    - [x] Modify `LeadIntakeService` to prevent incorrect Org linking via phone
    - [x] Verify `OrganizationRepository` for `findByName` or similar check
- [x] **P2: Accounting Isolation & Visibility Fix**
    - [x] Update `FinoteService.createFinote` to enforce `source_org_id` from context
    - [x] Update `FinoteController` to ensure context is passed correctly
- [x] **P3: Data & Code Cleanup**
    - [x] Fix existing mis-isolated finotes (update `source_org_id` for INC-2026-0003)
    - [x] Remove any dead code or stale comments regarding `FinoteAttachment`
    - [x] Update `03_walkthrough.md` with results
