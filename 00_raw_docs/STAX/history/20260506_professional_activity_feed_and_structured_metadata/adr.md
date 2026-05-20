# ADR: Professional Activity Feed & Structured Metadata Standards

## Context
The previous activity feed implementation relied on manual text logs or loosely defined event metadata. This led to "ugly" logs (plain action names), missing actor information (showing as "System"), and difficulty in extracting structured business data (like contract values) from the timeline.

## Decisions

### 1. Root-Level Actor Tracking
Every `IAuditableEvent` MUST include `actorId` and `actorName` at the root of the `AuditEntryPayload`, rather than hidden inside `metadata`. This ensures the `AuditLogService` can correctly populate the `actor_id` and `actor_name` columns in the database, even when request context is lost in asynchronous event handling.

### 2. Clean Metadata Standard
We shift away from "Textual Logging" towards "Structured Logging". 
- Logs should NOT contain pre-formatted strings in the database.
- Instead, they should contain raw data (e.g., `feeAmount: 5000000`) in the `metadata` field.
- The UI representation is handled by the `ActivityFormatter` using localized templates.

### 3. Smart Resource Aggregation
The `ActivityFeedService` is enhanced to perform "Relation-Aware Queries". For example, when viewing a Lead, the system automatically pulls relevant Organization-level events (like Organization Creation) to provide a 360-degree view.

## Consequences
- **Positive**: Professional and localized UI, precise actor tracking, searchable business metrics within logs.
- **Negative**: Requires slightly more boilerplate when defining new Domain Events (passing actor info).

## Status
Approved & Implemented.
