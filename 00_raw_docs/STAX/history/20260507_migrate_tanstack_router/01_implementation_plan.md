# Implementation Plan: TanStack Router Migration

## 1. Core Architecture Changes
We will shift from "Route-wraps-Layout" to "Layout-wraps-Route-Outlet" pattern.

### Layer Separation:
- **Infrastructure Layer**: TanStack Router Instance and Route Tree definition.
- **Application Layer**: `beforeLoad` hooks for Authentication and Authorization logic.
- **UI Layer**: `AdminLayout` with `<Outlet />` for rendering nested content.

## 2. File Structure
We will adopt a centralized route tree structure to maintain high visibility.

```text
client/src/app/router/
├── routes/             # Route definitions
│   ├── __root.tsx      # Global root (Providers)
│   ├── admin.tsx       # Admin Layout Route
│   ├── dashboard.tsx   # Individual leaf routes
│   └── ...
├── index.tsx           # Router provider and exports
└── guards/             # Auth/Permission logic
```

## 3. Step-by-Step Implementation

### Step 1: Base Configuration
1.  Install `@tanstack/react-router`.
2.  Define the `RootRoute` in `client/src/app/router/routes/__root.tsx`.
3.  Inject global context (QueryClient, Auth State) into the router.

### Step 2: Persistent Layouts
1.  Refactor `AdminLayout` to use `<Outlet />` instead of `{children}`.
2.  Create an `adminRoute` that uses `AdminLayout` as its component.
3.  All child routes (Dashboard, HRM, CRM) will be children of `adminRoute`.

### Step 3: Type-Safe Guards
1.  Implement a `requireAuth` helper using TanStack's `beforeLoad`.
2.  Define permission requirements in the route metadata.

### Step 4: Cleanup
1.  Remove `wouter` and its related logic.
2.  Replace `<Link>` and `useLocation` throughout the application.
3.  Fix all TypeScript errors arising from the migration.

## 4. Avoiding Code Smells
- **No Prop Drilling**: Use `useRouteContext` to access auth data instead of passing props through the layout.
- **Explicit Constants**: All route paths will be defined in a single source of truth.
- **Modular Routes**: Each major module (HRM, CRM) will have its own route subtree file.
