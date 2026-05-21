---
id: arch-architecture_blueprint_v1_rollout
title: Rollout Kiến Trúc Modular Monolith v1
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-import-boundary-rules]]"
summary: "Thiết lập nền tảng Modular Monolith và thực hiện Phase 0 & Phase 1 Client Modularization cho dự án STAX."
tags: [architecture, modular-monolith, client-refactor, api-modularization, bff]
---

## 1. Nền tảng Kiến trúc (Phase 0)
- **ADR-0001**: Xác lập mô hình *Modular Monolith*, *domain-first*, *thin BFF* và lộ trình *incremental migration*.
- **Boundary Rules**: Áp dụng quy tắc kiểm soát import chiều ngang/dọc qua `docs/import-boundary-guideline.md`.
- **BFF Baseline**: Tích hợp truy vết giao dịch bằng `X-Request-ID` qua request-id middleware, chuẩn hóa access log định dạng latency/status và bổ sung endpoint giám sát `/healthz`.
- **Centralized Env**: Đồng bộ hóa cấu hình môi trường tại `server/config/env.ts` và `client/src/core/config/env.ts`.

## 2. Tái cấu trúc Client Modularization (Phase 1)
### App Shell & Routing
- **Tách Router**: Chuyển đổi định tuyến và bảo vệ route (`AdminRoute`) từ `App.tsx` vào `client/src/app/router/index.tsx` và `route-guards.tsx` (hỗ trợ lazy loading).
- **Providers**: Gom cụm quản lý trạng thái vào `query-provider.tsx` và `auth-provider.tsx`.

### Core API Client
- Triển khai HTTP Client cơ sở tại `client/src/core/api/http-client.ts`, kết hợp bộ ánh xạ lỗi `error-mapper.ts` và quản lý khóa truy vấn tập trung `query-keys.ts`.
- Giảm coupling bằng cách refactor `client/src/lib/queryClient.ts` sử dụng trực tiếp cấu trúc HTTP Client mới.

### Module Domain & Public API
- Thiết lập cấu trúc thư mục domain cô lập:
  - `client/src/modules/{crm,hrm,accounting,rbac}/`
  - Đầu mối export (Public API): `index.ts` và lớp giao tiếp mạng: `api/*.api.ts`.
- Thực hiện dịch chuyển (migration) các page tiêu điểm: CRM (`leads.tsx`, `clients.tsx`, `lead-detail.tsx`) và RBAC (`index.tsx`) sang import trực tiếp từ các module API cục bộ thay vì client dùng chung.
- Tương thích ngược: Duy trì `queryClient.ts` làm cầu nối chuyển tiếp và chia sẻ schema dùng chung.