# Task Checklist — Architecture Blueprint v1 Rollout

> Trạng thái: In Progress
> 
> Nguyên tắc: Triển khai incremental theo phase, mỗi task hoàn tất phải cập nhật checklist và bằng chứng kiểm chứng.

---

## A. Setup & Governance

- [x] Tạo context folder theo chuẩn `docs/context/YYYYMMDD_slug`.
- [x] Tạo `01_implementation_plan.md`.
- [x] Tạo `02_task.md` với checklist chi tiết theo roadmap.
- [x] Tạo ADR chính thức cho “Architecture Blueprint v1”.
- [ ] Xác định owner/reviewer theo từng domain (`crm`, `hrm`, `accounting`, `rbac`).
- [ ] Thiết lập checklist PR chuẩn cho kiến trúc (contract impact, rollback plan, test evidence).

---

## B. Phase 0 — Foundation (1–2 tuần)

### B.1 Architecture Decision & Boundary Rules
- [x] Viết ADR v1 trong `docs/` (mục tiêu, decision, alternatives, consequences).
- [x] Bổ sung rule import boundary (eslint/convention) để tránh deep import xuyên domain.
- [x] Tạo guideline import public API (`modules/*/index.ts`).

### B.2 Env & Config Standardization
- [x] Tạo `client/src/core/config/env.ts` để gom env access phía client.
- [x] Tạo `server/src/config/env.ts` để gom env access phía server.
- [x] Refactor điểm đọc env rải rác về module config chuẩn.

### B.3 BFF Logging Baseline
- [x] Tạo middleware `request-id`.
- [x] Tạo middleware access logging (method/path/status/latency/request-id).
- [x] Tích hợp logging vào flow request hiện có.

### B.4 Validation / Exit criteria
- [x] `npm run check` pass.
- [ ] lint pass.
- [ ] build pass.
- [ ] Team review + đồng thuận baseline standards.

---

## C. Phase 1 — Client Modularization (2–4 tuần)

### C.1 App Shell & Router Split
- [x] Tạo `client/src/app/main.tsx`.
- [x] Tạo `client/src/app/router/index.tsx`.
- [x] Tạo `client/src/app/router/route-guards.tsx`.
- [x] Refactor `client/src/App.tsx` giảm trách nhiệm route registry.

### C.2 Providers Standardization
- [x] Tạo `client/src/app/providers/query-provider.tsx`.
- [x] Tạo `client/src/app/providers/auth-provider.tsx`.
- [x] Đảm bảo providers compose rõ ràng ở app entrypoint.

### C.3 API Layer Decomposition
- [x] Tạo `client/src/core/api/http-client.ts` (transport + auth header + status handling).
- [x] Tạo `client/src/core/api/error-mapper.ts`.
- [x] Tạo `client/src/core/api/query-keys.ts`.
- [x] Tách endpoint theo domain vào `client/src/modules/*/api/*.api.ts`.
- [x] Giảm vai trò `client/src/lib/queryClient.ts` (deprecate dần).

### C.4 Module Structure Adoption
- [x] Khởi tạo structure domain tối thiểu cho `crm`, `hrm`, `accounting`, `rbac`.
- [x] Mỗi module có `index.ts` public API.
- [ ] Cấm module khác deep import internals.

### C.5 Validation / Exit criteria
- [ ] Routing hoạt động sau split.
- [ ] Lazy loading cho các module chính.
- [ ] Query keys theo convention domain.
- [ ] Không phát sinh regression chức năng admin hiện tại.

---

## D. Phase 2 — Shared Contracts Refactor (2–3 tuần)

### D.1 Contracts Restructure
- [ ] Tạo `shared/contracts/auth/*`.
- [ ] Tạo `shared/contracts/crm/*`.
- [ ] Tạo `shared/contracts/hrm/*`.
- [ ] Tạo `shared/contracts/accounting/*`.
- [ ] Tạo `shared/contracts/rbac/*`.
- [ ] Tạo `shared/primitives/*`.

### D.2 Migration from `shared/schema.ts`
- [ ] Tách schema/types theo từng domain từ file tổng hợp.
- [ ] Tạo `shared/index.ts` export chuẩn.
- [ ] Duy trì compatibility tạm bằng re-export (nếu cần).
- [ ] Cập nhật import path toàn codebase theo batch nhỏ.

### D.3 Validation / Exit criteria
- [ ] Không còn import trực tiếp “god file” cho phần đã migrate.
- [ ] TypeScript check pass sau mỗi batch migration.
- [ ] Contract thay đổi có ghi chú version/migration note.

---

## E. Phase 3 — Auth/RBAC Hardening (2–3 tuần)

### E.1 Centralized Authorization
- [ ] Tạo `client/src/core/rbac/permission-checker.ts`.
- [ ] Tạo/chuẩn hóa `client/src/core/auth/auth-policy.ts`.
- [ ] Refactor `client/src/hooks/useAuth.ts` để loại hardcode bypass.

### E.2 Claims Contract Alignment
- [ ] Chuẩn hóa user claims contract trong `shared/contracts/auth/*`.
- [ ] Đồng bộ naming permission format `domain:action`.
- [ ] Đảm bảo UI chỉ làm UX gating, không coi là security boundary.

### E.3 Validation / Exit criteria
- [ ] Luồng phân quyền nhất quán ở các page/hook chính.
- [ ] Có test cho permission checker.
- [ ] Reviewer xác nhận logic dễ audit.

---

## F. Phase 4 — Test & Observability Uplift (2–4 tuần)

### F.1 Testing
- [ ] Unit tests cho utils/mappers/permission-checker.
- [ ] Integration tests cho module APIs với mock backend.
- [ ] Contract tests FE-BE theo `shared/contracts`.
- [ ] E2E smoke tests: login, lead lifecycle, role assignment cơ bản.

### F.2 BFF Observability
- [ ] Thêm route `/healthz`.
- [ ] Thêm route `/metrics`.
- [ ] Bổ sung error handler chuẩn.
- [ ] Chuẩn hóa log format để tích hợp dashboard (Sentry/Grafana tương đương).

### F.3 Quality Gates
- [ ] CI gate: `npm run check`.
- [ ] CI gate: lint.
- [ ] CI gate: test.
- [ ] CI gate: build.

---

## G. Definition of Done (cross-phase)

- [ ] Có code + docs tương ứng.
- [ ] Không phá backward compatibility ngoài kế hoạch.
- [ ] Có test hoặc bằng chứng xác minh phù hợp.
- [ ] Có rollback plan tối thiểu cho thay đổi chính.
- [ ] Có ít nhất 1 reviewer không trực tiếp implement.

---

## H. Handoff / Archiving

- [ ] Hoàn thiện `03_walkthrough.md` sau từng đợt implementation chính.
- [ ] Khi PR merge hoặc hạng mục ổn định: di chuyển context sang `docs/history/`.
- [ ] Lệnh mẫu: `mv docs/context/20260505_architecture_blueprint_v1_rollout docs/history/`

---

## I. Current Execution Window — Phase 1 Completion Batches

- [x] Batch 0.1: Đồng bộ `01_implementation_plan.md` với mục “Execution Window — Phase 1 Completion”.
- [x] Batch 0.2: Đồng bộ `02_task.md` + `03_walkthrough.md` phản ánh đúng trạng thái hiện tại.
- [x] Batch 1: Tạo module skeleton `client/src/modules/{crm,hrm,accounting,rbac}` + `index.ts` public API.
- [x] Batch 2: Tách domain APIs khỏi `client/src/lib/queryClient.ts` sang `client/src/modules/*/api/*.api.ts`.
- [x] Batch 3: Migrate consumers trọng điểm (`crm/leads`, `crm/clients`, `crm/lead-detail`, `rbac/index`) sang domain APIs + query keys chuẩn.
- [x] Batch 4: Verify lazy loading routes + smoke regression các luồng admin chính.
- [x] Batch 5: Validation gates (`npm run check`, lint, build) + cập nhật evidence vào walkthrough.

### Ghi chú validation hiện tại
- `npm run check`: ✅ pass
- `npm run lint`: ⚠️ chưa có script `lint` trong `package.json`
- `npm run build`: ✅ pass
