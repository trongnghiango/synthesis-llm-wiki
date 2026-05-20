# Tasks: TanStack Router Migration & Polish

- [x] **Infrastructure Setup**
    - [x] Install dependencies
    - [x] Create root route and router instance
    - [x] Implement type-safe route registration

- [x] **Core Migration**
    - [x] Refactor `AdminLayout` (Outlet-based)
    - [x] Migrate `useAuth` and `PageHeader` navigation
    - [x] Implement Auth guards in `beforeLoad`

- [x] **Module Migration**
    - [x] CRM Module (Leads, Clients, Contracts + Details)
    - [x] RBAC Module (Roles + Detail)
    - [x] HRM Module (Employees, Org Structure)

- [x] **UI/UX Optimization (Post-Migration)**
    - [x] Fix Detail Page parameter passing (`NaN` fix)
    - [x] Implement Full-Width mode for Org Chart
    - [x] Fix Org Chart info panel positioning (Absolute right)
    - [x] Enable Left-Click dragging for Org Chart
    - [x] Implement smooth Fade transitions between routes

- [x] **Cleanup**
    - [x] Remove `wouter` references and uninstall package
    - [x] Delete legacy `route-guards.tsx`
    - [x] Final code audit for type-safety
