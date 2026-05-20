# Implementation Plan - Hardening STAX Constitution & Fixing Incomplete Code

This plan addresses the "code nửa vời" (incomplete code) and "smells" identified during the architectural review. The goal is to ensure full compliance with the STAX Constitution (Clean Architecture, Event-Driven Audit Log, Server-Driven UI).

## Proposed Changes

### 1. Hardening Audit Log System

#### [NEW] [lead-status-changed.event.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/domain/events/lead-status-changed.event.ts)
- Define `LeadStatusChangedEvent` implementing `IAuditableEvent`.
- Capture `before` and `after` stages for Delta Logging.

#### [NEW] [lead-assigned.event.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/domain/events/lead-assigned.event.ts)
- Define `LeadAssignedEvent` to track lead allocation to employees.

#### [MODIFY] [lead-workflow.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/application/services/lead-workflow.service.ts)
- Publish `LeadAssignedEvent` in `assignLead`.
- Publish `LeadStatusChangedEvent` in `closeLeadAsWon`.

#### [NEW] [finote-status-changed.event.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/accounting/domain/events/finote-status-changed.event.ts)
- Define `FinoteStatusChangedEvent` for approval/rejection tracking.

#### [MODIFY] [finote.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/accounting/application/services/finote.service.ts)
- Publish `FinoteStatusChangedEvent` in `approve` and `reject`.

#### [MODIFY] [audit-domain-event.handler.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/logging/application/handlers/audit-domain-event.handler.ts)
- Register listeners for:
    - `LeadStatusChangedEvent`
    - `LeadAssignedEvent`
    - `FinoteCreatedEvent`
    - `FinoteStatusChangedEvent`

---

### 2. Fixing "Nửa vời" in Bootstrap & Services

#### [MODIFY] [bootstrap.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/system/application/services/bootstrap.service.ts)
- Inject `IPermissionService` (from RBAC) to calculate real UI permissions.
- Inject `ILeadRepository` and `IFinoteRepository` to calculate real team summary statistics.
- Remove all static mocks.

---

### 3. Consistency & UI Refinement

#### [MODIFY] [lead.response.dto.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/infrastructure/dtos/lead.response.dto.ts)
- Rename `estimatedValue` to `expectedValue` to match the Domain Entity.

#### [MODIFY] [lead-query.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/application/services/lead-query.service.ts)
- Update mapping to use `expectedValue`.

## Verification Plan

### Automated Tests
- Run existing unit tests for CRM and Accounting to ensure no regressions.
- Add new test cases to verify that events are published when status changes.

### Manual Verification
- Perform a "Lead Won" action and verify a new entry in the `audit_logs` table.
- Approve a Finote and verify the audit log.
- Check the `/bootstrap` API response to ensure it returns real data instead of mocks.
