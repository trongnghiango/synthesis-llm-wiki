# Implementation Plan - Position Management API

The frontend team has requested a new API endpoint to retrieve positions within an organizational unit: `GET /api/org-structure/positions?orgUnitId={id}`. This endpoint is currently missing and needs to be implemented following the project's Clean Architecture standards.

## User Review Required

> [!IMPORTANT]
> This plan adds a new method to the `IOrgStructureRepository` and a corresponding endpoint in the `OrgStructureController`. It assumes that the `positions` table already exists in the database schema (which it does).

## Proposed Changes

### [Component Name] Org Structure Module

#### [MODIFY] [org-structure.repository.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/domain/repositories/org-structure.repository.ts)
- Add `findPositionsByOrgUnitId(orgUnitId: number): Promise<PositionEntity[]>;` to the `IOrgStructureRepository` interface.

#### [MODIFY] [drizzle-org-structure.repository.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/infrastructure/persistence/drizzle-org-structure.repository.ts)
- Implement `findPositionsByOrgUnitId` using Drizzle to query the `positions` table filtered by `org_unit_id`.

#### [MODIFY] [org-structure.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/application/services/org-structure.service.ts)
- Add `getPositionsByOrgUnit(orgUnitId: number): Promise<PositionEntity[]>` method to handle the business logic of retrieving positions.

#### [NEW] [position-response.dto.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/infrastructure/dtos/position-response.dto.ts)
- Create a DTO to standardize the API response for positions.

#### [MODIFY] [org-structure.controller.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/infrastructure/controllers/org-structure.controller.ts)
- Add `@Get('positions')` endpoint that accepts `orgUnitId` as a query parameter.
- Apply appropriate RBAC permissions (`org:read`).

## Verification Plan

### Automated Tests
- Create a unit test for the new repository method in `drizzle-org-structure.repository.spec.ts` (if it exists) or verify via manual API testing.

### Manual Verification
- Call `GET /api/org-structure/positions?orgUnitId=527` using an API client (e.g., Postman or cURL) and verify the JSON response structure.
- Ensure that the `org:read` permission is required and correctly enforced.
