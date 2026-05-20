# Task List - Implement Position CRUD

- [x] Define Position DTOs (Application & Infrastructure)
    - [x] Create `src/modules/org-structure/application/dtos/position.dto.ts`
    - [x] Create `src/modules/org-structure/infrastructure/dtos/position.request.dto.ts`
- [x] Update Repository Layer
    - [x] Update `IOrgStructureRepository` interface
    - [x] Update `DrizzleOrgStructureRepository` implementation
- [x] Update Application Layer
    - [x] Add `createPosition`, `updatePosition`, `deletePosition` to `OrgStructureService`
- [x] Update Infrastructure Layer
    - [x] Add CRUD endpoints to `OrgStructureController`
- [x] Verification
    - [x] Check Swagger documentation
    - [x] Run unit tests
    - [x] Manual test via Curl/Postman
