# Implementation Plan: Professional Services HRM Portal (Employee 360)

Build a modern, high-performance employee management system for a consulting/accounting firm. This module integrates core HR functions with task management and professional certification tracking.

## User Review Required

> [!IMPORTANT]
> **Task Integration**: We need to define how "Tasks" are stored in the database. Should we use an existing `Task` table or create a lightweight `EmployeeTask` link for this module?
> **Certification Tracking**: Are there specific accounting/tax certifications (e.g., CPA, CTA, ACCA) that must be hardcoded as options, or should it be a dynamic list?

## Proposed Architecture

### 1. Data Model Enhancements
- [ ] **Employee Profile**: Add fields for `biography`, `skills` (JSON), and `certifications` (JSON/Table).
- [ ] **Capacity Link**: Link employees to `ClientContract` to track active accounts.
- [ ] **Task Integration**: Interface with the current `tasks` table (if available) to pull real-time workload.

### 2. UI/UX Design (STAX Standard)
- [ ] **Main Employee Grid**: 
    - Advanced filtering (By Department, Role, Certification).
    - Status indicators (Active, On Leave, Full Capacity).
- [ ] **Employee 360 Side Panel**:
    - **Tab 1: Overview**: General info & Professional Summary.
    - **Tab 2: Skills & Certs**: Visual skill matrix and certificate badges.
    - **Tab 3: Workload**: List of active tasks and assigned clients.
    - **Tab 4: Timeline**: Recent activities and performance milestones.

### 3. Key Components
#### [NEW] [EmployeeGrid.tsx](file:///home/ka/temps/DentalCarePortal/client/src/components/hrm/EmployeeGrid.tsx)
A high-performance table using `DataGrid` with custom cells for professional badges.

#### [NEW] [EmployeeDetailPanel.tsx](file:///home/ka/temps/DentalCarePortal/client/src/components/hrm/EmployeeDetailPanel.tsx)
A rich interactive side panel for the 360-degree view.

#### [NEW] [CapacityChart.tsx](file:///home/ka/temps/DentalCarePortal/client/src/components/hrm/CapacityChart.tsx)
A visual representation of employee workload using a heat-map or progress bars.

## Implementation Steps

### Phase 1: Foundation & API
1. Extend `Employee` type in `shared/contracts/hrm.ts`.
2. Implement `hrmApi.getEmployeesWithDetails()` to fetch workload data.

### Phase 2: Core Grid & Management
1. Build the `EmployeeGrid` with basic CRUD actions.
2. Implement the Search & Filter engine.

### Phase 3: The 360 Experience
1. Build the `EmployeeDetailPanel` with multiple tabs.
2. Integrate Task data from the backend.

### Phase 4: Polish & Performance
1. Add micro-animations for transitions.
2. Optimize DataGrid for 500+ employees.

## Verification Plan
### Automated Tests
- `npm run test:hrm`: Verify data binding for complex employee objects.
- Playwright tests for Side Panel navigation.

### Manual Verification
- Verify that filtering by "CPA Certification" correctly shows only certified staff.
- Check if assigning a task in CRM reflects immediately in the HRM Workload tab.
