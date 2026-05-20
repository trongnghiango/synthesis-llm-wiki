# REVISED Implementation Plan - Clean Lead-Contact Integration

This plan corrects previous design deviations and aligns the CRM module with the project's normalized database design and Clean Architecture. We will move away from storing contact information directly on the `leads` table and instead use a robust many-to-one relationship between Leads and Contacts.

## Corrected Design Principles

1.  **Normalization**: The `leads` table MUST NOT store `contact_name`, `contact_phone`, or `contact_email`. These belong to the `contacts` table.
2.  **Relationship**: A `Lead` links to a `Contact` via `contact_id`.
3.  **Data Integrity**: Every legacy lead being migrated must result in the creation of a `Contact` (if not found) and a link established via `contact_id`.
4.  **Retrieval**: Data retrieval for lead list must use `LEFT JOIN` on the `contacts` table to display contact details.

## Proposed Changes

### 1. Database Schema Refactoring

#### [MODIFY] [leads.schema.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/database/schema/crm/leads.schema.ts)
- **DELETE**: `contactName`, `contactPhone`, `contactEmail` columns.
- **ADD**: `contactId` column as a foreign key to `contacts.id`.

---

### 2. Domain & Application Layer

#### [MODIFY] [lead.entity.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/domain/entities/lead.entity.ts)
- Update properties to include `contactId`.
- Restored `assignTo`, `closeAsWon`.
- Supported `serviceNeed` and `note` via `metadata` fallback.

#### [MODIFY] [crm-legacy-migration.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/test/application/services/crm-legacy-migration.service.ts)
- **CORRECT LOGIC**: 
    1. Extract phone/name from CSV.
    2. Create/Find `Contact` record first.
    3. Insert `Lead` record with the resulting `contactId`.

---

### 3. Persistence Layer (Repository & Mapper)

#### [MODIFY] [lead.mapper.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/infrastructure/mappers/lead.mapper.ts)
- Update to map `contact_id` and handle virtual metadata fields (`serviceNeed`, `note`).

#### [MODIFY] [drizzle-lead.repository.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/infrastructure/persistence/drizzle-lead.repository.ts)
- Update `findAll` to `leftJoin` with `schema.contacts`.
- Update search logic to target joined contact fields.

## Verification Plan

### Automated Tests
- `npx tsc --noEmit`: 0 errors.
- Migration script results: 1172 successes, 0 errors.

### Manual Verification
- `GET /crm/leads` results verify joined data retrieval.
