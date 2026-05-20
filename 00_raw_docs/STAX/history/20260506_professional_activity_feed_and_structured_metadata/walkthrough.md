# Walkthrough: Professional CRM Logging & Activity Feed

## Changes Summary

### 1. Core Infrastructure
- **`auditable-event.interface.ts`**: Expanded `AuditEntryPayload` to include optional root-level `actorId` and `actorName`.
- **`ActivityFeedService.ts`**: Implemented smart aggregation logic to fetch Organization creation events when viewing Lead timelines.
- **`ActivityFormatter.ts`**: Added professional mappings for `LEAD.STATUS_CHANGED`, `CONTRACT.CREATED`, and improved templates for existing CRM actions.

### 2. Lead Intake Flow
- **`LeadController.ts`**: Fixed `user.id` mapping and ensured actor info is passed to all workflow actions.
- **`LeadIntakeService.ts`**: Updated to capture and propagate actor context and `isNewCustomer` status.
- **Events**: `LeadCreatedEvent` and `OrganizationCreatedEvent` now support root-level actor tracking.

### 3. Lead-to-Contract Conversion
- **`LeadWorkflowService.ts`**: Integrated the new `ContractCreatedEvent` with structured metadata (fee, tax code, service type).
- **`ContractCreatedEvent.ts`**: New auditable event following the "Clean Metadata" standard.
- **`AuditDomainEventHandler.ts`**: Registered handler for automatic contract logging.

### 4. CRM Consistency
- Updated `QuoteCreatedEvent`, `QuoteStatusChangedEvent`, `LeadStatusChangedEvent`, and `LeadAssignedEvent` to ensure 100% coverage of actor tracking across the CRM module.

## Verification
- Verified through Frontend JSON responses that `actor.id` and `actor.name` are correctly populated.
- Verified that `LEAD.STATUS_CHANGED` and `CONTRACT.CREATED` display professional Vietnamese titles and icons in the feed.
- Verified that Lead timeline correctly shows the parent Organization's creation event.
