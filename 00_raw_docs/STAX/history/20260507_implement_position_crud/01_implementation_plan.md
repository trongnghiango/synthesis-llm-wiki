# Implementation Plan - Position CRUD Completion

This plan outlines the steps to complete the CRUD operations for the `Positions` entity in the `OrgStructure` module, enabling full management of job positions.

## User Review Required

> [!IMPORTANT]
> - The implementation strictly follows **Clean Architecture (Stage 4)**: separation between Domain, Application, and Infrastructure layers.
> - We will use **Drizzle ORM** for persistence and **NestJS/Swagger** for the API surface.

## Proposed Changes

### 1. Application Layer (DTOs & Service)

#### [NEW] [position.dto.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/application/dtos/position.dto.ts)
- Define pure TypeScript interfaces for `CreatePositionDto` and `UpdatePositionDto`.
- These will be used by the `OrgStructureService` to remain framework-agnostic.

#### [MODIFY] [org-structure.service.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/application/services/org-structure.service.ts)
- **`createPosition(dto: CreatePositionDto)`**:
    - Check if `orgUnitId`, `jobTitleId`, and `gradeId` exist in the database.
    - Validate that the position `code` is unique.
    - Call repository to persist.
- **`updatePosition(id: number, dto: UpdatePositionDto)`**:
    - Ensure the position exists.
    - If `code` is being changed, ensure the new code is unique.
    - Call repository to update.
- **`deletePosition(id: number)`**:
    - Check if the position is currently assigned to any employees (safety check).
    - Call repository to delete.

---

### 2. Domain Layer (Repository Interface)

#### [MODIFY] [org-structure.repository.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/domain/repositories/org-structure.repository.ts)
- Add missing methods to `IOrgStructureRepository`:
    ```typescript
    updatePosition(id: number, data: Partial<PositionEntity>): Promise<PositionEntity | null>;
    deletePosition(id: number): Promise<boolean>;
    isPositionInUse(id: number): Promise<boolean>; // Check for assigned employees
    ```

---

### 3. Infrastructure Layer (Persistence & API)

#### [MODIFY] [drizzle-org-structure.repository.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/infrastructure/persistence/drizzle-org-structure.repository.ts)
- Implement `updatePosition` using Drizzle `.update()`.
- Implement `deletePosition` using Drizzle `.delete()`.
- Implement `isPositionInUse` by querying the `employees` table.

#### [NEW] [position.request.dto.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/infrastructure/dtos/position.request.dto.ts)
- Define `CreatePositionRequestDto` and `UpdatePositionRequestDto` with `@ApiProperty` and validation decorators (`IsString`, `IsInt`, etc.).

#### [MODIFY] [org-structure.controller.ts](file:///home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/org-structure/infrastructure/controllers/org-structure.controller.ts)
- **`POST /positions`**: Use `ORG_PERMISSIONS.MANAGE`.
- **`PATCH /positions/:id`**: Use `ORG_PERMISSIONS.UPDATE`.
- **`DELETE /positions/:id`**: Use `ORG_PERMISSIONS.DELETE` (or `MANAGE`).

---

## Verification Plan

### Automated Tests
- Create unit tests for new service methods in `org-structure.service.spec.ts`.
- Command: `pnpm test src/modules/org-structure/application/services/org-structure.service.spec.ts`

### Manual Verification
- **Swagger UI**: Access `http://localhost:8080/docs` to verify the new endpoints and their schemas.
- **Curl/Postman**: Perform a full CRUD cycle:
    1. Create a new position.
    2. Update its name/code.
    3. Delete it (and verify safety check by trying to delete a position with an assigned employee).
