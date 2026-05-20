# Implementation Plan — Architecture Blueprint v1 Rollout

## 1) Mục tiêu
Chuẩn hóa và triển khai lộ trình kiến trúc trong `docs/kien-truc.md` theo hướng incremental, tránh big-bang rewrite, đảm bảo mọi thay đổi đều có khả năng truy vết qua context workflow.

Mục tiêu cụ thể:
- Chuyển kiến trúc hiện tại sang tổ chức domain-first rõ ràng.
- Tách các “điểm nghẽn” hiện hữu (`App.tsx`, `queryClient.ts`, `shared/schema.ts`, RBAC hardcode).
- Nâng chuẩn vận hành BFF (health/metrics/logging/request-id).
- Tăng độ tin cậy phát hành thông qua quality gates và test strategy.

## 2) Giải pháp đề xuất (theo phase)

### Phase 0 — Foundation
Phạm vi:
- Chốt ADR cho kiến trúc v1.
- Đặt convention boundary import.
- Chuẩn hóa env config client/server.
- Bổ sung logging baseline cho BFF.

Chiến lược kỹ thuật:
- Tạo ADR trong `docs/` để cố định quyết định kiến trúc.
- Áp quy tắc lint/convention để hạn chế import xuyên domain internals.
- Tách config env thành module riêng ở cả `client` và `server`.
- Cài middleware request logging tối thiểu (method, path, status, latency, request-id).

Exit criteria:
- Team đồng thuận kiến trúc mới.
- CI không giảm ổn định.

### Phase 1 — Client modularization
Phạm vi:
- Tách router khỏi `client/src/App.tsx`.
- Áp lazy loading theo module.
- Tách `queryClient.ts` thành `core/api` + `modules/*/api`.
- Chuẩn hóa query keys.

Chiến lược kỹ thuật:
- Introduce `client/src/app/router/index.tsx` và `route-guards.tsx`.
- Đưa logic API transport vào `core/api/http-client.ts`.
- Tạo `core/api/error-mapper.ts` và `core/api/query-keys.ts`.
- Domain API lives in `client/src/modules/{domain}/api/*.api.ts`.

Exit criteria:
- Mỗi domain có API file riêng.
- Giảm coupling liên domain.

### Phase 2 — Shared contracts refactor
Phạm vi:
- Tạo `shared/contracts/*`.
- Di chuyển schema/type theo domain.
- Tạo `shared/index.ts` export chuẩn.
- Cập nhật import path toàn codebase.

Chiến lược kỹ thuật:
- Cắt `shared/schema.ts` theo domain package nhỏ.
- Giữ compatibility tạm thời bằng re-export trong giai đoạn migrate.
- Chạy TypeScript checks theo từng batch import migration.

Exit criteria:
- Không còn phụ thuộc “god file” schema tổng hợp.

### Phase 3 — Auth/RBAC hardening
Phạm vi:
- Tạo `core/rbac/permission-checker.ts` tập trung.
- Loại hardcode bypass trong hooks UI (đặc biệt `useAuth.ts`).
- Chuẩn hóa contract user claims ở shared contracts.

Chiến lược kỹ thuật:
- Tất cả check quyền UI đi qua permission checker.
- Hooks chỉ gọi API/policy, không tự encode policy phân quyền.
- Đồng bộ tên permission format `domain:action`.

Exit criteria:
- AuthZ logic nhất quán, dễ audit.

### Phase 4 — Test & Observability uplift
Phạm vi:
- Bổ sung unit/integration/contract tests trọng yếu.
- Bổ sung health/metrics endpoint BFF.
- Chuẩn hóa dashboard theo dõi lỗi/latency.

Chiến lược kỹ thuật:
- Unit cho mappers + permission checker.
- Integration cho module API với mock backend.
- Contract tests FE/BE theo `shared/contracts`.
- Expose `/healthz` và `/metrics` trong BFF.

Exit criteria:
- Có quality gate rõ ràng trước release.

## 3) Thay đổi dự kiến theo module/file

### Client
- `client/src/App.tsx` (giảm vai trò registry)
- `client/src/app/main.tsx` (mới)
- `client/src/app/providers/query-provider.tsx` (mới)
- `client/src/app/providers/auth-provider.tsx` (mới)
- `client/src/app/router/index.tsx` (mới)
- `client/src/app/router/route-guards.tsx` (mới)
- `client/src/core/api/http-client.ts` (mới)
- `client/src/core/api/error-mapper.ts` (mới)
- `client/src/core/api/query-keys.ts` (mới)
- `client/src/core/auth/auth-store.ts` (mới)
- `client/src/core/auth/auth-policy.ts` (mới)
- `client/src/core/rbac/permission-checker.ts` (mới)
- `client/src/core/config/env.ts` (mới)
- `client/src/modules/**` (mới, theo domain)
- `client/src/lib/queryClient.ts` (giảm dần trách nhiệm / deprecate)

### Shared
- `shared/schema.ts` (giảm dần / deprecate)
- `shared/contracts/auth/*`
- `shared/contracts/crm/*`
- `shared/contracts/hrm/*`
- `shared/contracts/accounting/*`
- `shared/contracts/rbac/*`
- `shared/primitives/*`
- `shared/index.ts` (mới)

### Server BFF
- `server/src/index.ts` (mới) hoặc migrate từ `server/index.ts`
- `server/src/config/env.ts`
- `server/src/middlewares/request-id.ts`
- `server/src/middlewares/logger.ts`
- `server/src/middlewares/error-handler.ts`
- `server/src/proxy/api-proxy.ts`
- `server/src/routes/health.ts`
- `server/src/routes/metrics.ts`
- `server/src/observability/logging.ts`
- `server/src/observability/metrics.ts`

## 4) Rủi ro và giảm thiểu
1. Refactor lan rộng làm chậm feature delivery.
   - Giảm thiểu: chia batch nhỏ theo domain, mỗi batch có kiểm tra TS/lint/test.

2. Đứt import khi tách contracts.
   - Giảm thiểu: áp dụng re-export tạm thời + migration map + contract tests.

3. Sai lệch AuthZ giữa UI và backend.
   - Giảm thiểu: backend là source of truth, UI chỉ UX gating, chuẩn hóa claims contract.

4. BFF phình business logic.
   - Giảm thiểu: enforce scope BFF (proxy/observability), code review checklist.

## 5) Nguyên tắc thực thi
- Incremental migration, không big-bang rewrite.
- Mỗi PR phải nêu ảnh hưởng contract (nếu có).
- Ưu tiên additive changes, hạn chế breaking changes.
- Mọi thay đổi chính phải cập nhật context checklist và walkthrough.

## 6) Execution Window — Phase 1 Completion (Current)

Mục tiêu window hiện tại: hoàn tất phần còn lại của **Phase 1 — Client modularization** trong cùng context, tránh phân mảnh tài liệu và đảm bảo traceability trước khi archive.

### Batch 0 — Context consolidation
- Cập nhật đồng bộ `01_implementation_plan.md`, `02_task.md`, `03_walkthrough.md` để phản ánh đúng đã làm/chưa làm.
- Không tạo context mới ở giai đoạn này.

### Batch 1 — Module skeleton + public API boundary
- Tạo `client/src/modules/{crm,hrm,accounting,rbac}/index.ts`.
- Thiết lập `api/` cho từng domain để chuẩn bị migration endpoint.

### Batch 2 — Domain APIs extraction
- Trích endpoint theo domain khỏi `client/src/lib/queryClient.ts` sang `client/src/modules/*/api/*.api.ts`.
- Ưu tiên CRM trước, sau đó HRM/Accounting/RBAC.
- Giữ compatibility bridge tạm thời để giảm regression.

### Batch 3 — Consumer migration
- Refactor các page/hook trọng điểm dùng domain APIs + `core/api/query-keys.ts`.
- Ưu tiên: `crm/leads`, `crm/clients`, `crm/lead-detail`, `rbac/index`.

### Batch 4 — Router/lazy-load verification
- Rà soát lazy loading tại `client/src/app/router/index.tsx`.
- Smoke check luồng admin chính sau migration.

### Batch 5 — Validation gates + evidence
- Chạy `npm run check`, lint, build.
- Cập nhật evidence vào `03_walkthrough.md` và checklist `02_task.md`.
