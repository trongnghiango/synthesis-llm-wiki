# Implementation Plan — Legacy API Cleanup

Dọn dẹp triệt để `queryClient.ts` và chuyển đổi sang hệ thống Modular API.

## Proposed Changes
- Khởi tạo `core/api/auth.api.ts` và `core/api/system.api.ts`.
- Refactor Consumers: `useAuth`, `useLookups`, `Dashboard`, `Settings`, `RoleDetail`, `Leads`, `ContractDetail`, `Contracts`.
- Xóa bỏ object `api` trong `queryClient.ts`.

## Verification Plan
- `npm run check` & `npm run build`.
