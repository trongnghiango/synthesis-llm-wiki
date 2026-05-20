# Research: Migration from wouter to TanStack Router

## Current State Analysis (wouter)
The current routing implementation using `wouter` is simple but has reached its architectural limits for an ERP-scale application.

### Identified Code Smells & Issues:
1.  **Redundant Layout Mounting**: Since `AdminLayout` is wrapped inside individual `AdminRoute` components, the layout (including Sidebar/Header) re-mounts on every navigation. This causes state loss (sidebar menus close) and visual flickering.
2.  **String-based Routing**: URLs are hardcoded as strings everywhere (`<Link href="/admin/..." />`). There is no compile-time check if a route exists.
3.  **Loose Search Params**: Filtering and pagination params are parsed manually using `useLocation`, leading to fragile logic when handling multiple optional parameters.
4.  **Implicit Auth Guards**: Navigation guards are implemented as UI wrappers (`AdminRoute`), which means the component starts mounting before authentication is verified.

## Why TanStack Router?
TanStack Router provides a first-class solution for all the above issues while maintaining a high-performance profile.

### Technical Benefits:
- **Nested Layouts (Out-of-the-box)**: Routes are hierarchical. The Sidebar/Header will be defined in a parent route and will *never* re-render or re-mount when children change.
- **Full Type-Safety**: Links and Navigations are validated at compile-time.
- **Built-in Loaders**: Data can be pre-fetched before the component renders.
- **Explicit Search Param Management**: Built-in validation (via Zod) for search params ensures data integrity.
