# Implementation Plan - Manage Position and Department Assignment UI (Refined)

## Goal
Develop a premium, visual interface for managing employee assignments, focusing on a "Staffing Board" mode within the Org Structure page.

## Proposed Changes
1. **API Standardization**: Fix inconsistencies in `hrm.api.ts` and add missing position management endpoints.
2. **Staffing Board Mode**: Integrate a Kanban-style "Board" view in `OrgStructurePage` for visual staffing.
3. **Position Management**: Add UI for creating/editing positions directly in the Org Structure sidebar.
4. **Assignment Modal**: A reusable component for assigning employees to positions.

## Tasks
- [ ] Standardize `hrm.api.ts` endpoints.
- [ ] Add `PositionModal` for managing positions.
- [ ] Implement "Board" mode toggle and layout in `OrgStructurePage`.
- [ ] Create `AssignmentModal` for employee assignment.
- [ ] Integrate assignment logic into Employee List and Detail Panel.
- [ ] Final UI Polish & Animations.
