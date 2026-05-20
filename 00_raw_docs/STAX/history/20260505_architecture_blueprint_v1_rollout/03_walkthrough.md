# Walkthrough — Architecture Blueprint v1 Rollout

## 1) Tóm tắt thay đổi quan trọng

Trong đợt này, mình đã hoàn thiện bộ context nền tảng để triển khai kiến trúc v1 theo chuẩn workflow:

1. **Tạo context làm việc chuẩn**
   - `docs/context/20260505_architecture_blueprint_v1_rollout/`

2. **Soạn kế hoạch triển khai tổng (`01_implementation_plan.md`)**
   - Phân rã đầy đủ Phase 0 → Phase 4.
   - Nêu rõ mục tiêu, chiến lược kỹ thuật, phạm vi file/module, rủi ro và biện pháp giảm thiểu.

3. **Soạn checklist thực thi (`02_task.md`)**
   - Checklist chi tiết theo phase, có exit criteria và DoD.
   - Có mục governance, quality gates, handoff/archiving.

> Lưu ý: Đây là đợt **chuẩn bị kế hoạch + điều phối execution**, chưa bắt đầu refactor code nghiệp vụ trong client/server/shared.

## 1.1 Cập nhật mới — Phase 1 (đợt refactor hiện tại)

Đã bắt đầu refactor Client Modularization với phạm vi an toàn, giữ tương thích ngược:

1. **Tách App Shell / Router**
   - Tạo `client/src/app/router/index.tsx` với lazy loading theo route/module.
   - Tạo `client/src/app/router/route-guards.tsx` (đưa `AdminRoute` ra khỏi `App.tsx`).
   - Refactor `client/src/App.tsx` để chỉ còn vai trò compose providers + router.

2. **Chuẩn hóa Providers**
   - Tạo `client/src/app/providers/query-provider.tsx`.
   - Tạo `client/src/app/providers/auth-provider.tsx` (placeholder để mở rộng Auth context ở phase sau).

3. **Tách API core khỏi query client**
   - Tạo `client/src/core/config/env.ts`.
   - Tạo `client/src/core/api/http-client.ts`.
   - Tạo `client/src/core/api/error-mapper.ts`.
   - Tạo `client/src/core/api/query-keys.ts`.
   - Refactor `client/src/lib/queryClient.ts` dùng lại `httpRequest`/`withQuery` để giảm coupling.

4. **Kiểm tra kỹ thuật**
   - Đã chạy TypeScript check (`npm run check`) không báo lỗi trong output hiện tại.

---

## 2) Hướng dẫn kiểm tra (Testing Instructions)

### 2.1 Kiểm tra cấu trúc context
Xác nhận tồn tại đủ 3 file bắt buộc:

- `docs/context/20260505_architecture_blueprint_v1_rollout/01_implementation_plan.md`
- `docs/context/20260505_architecture_blueprint_v1_rollout/02_task.md`
- `docs/context/20260505_architecture_blueprint_v1_rollout/03_walkthrough.md`

### 2.2 Kiểm tra nội dung theo chuẩn `standard_workflow.md`

1. `01_implementation_plan.md` có đủ:
   - Mục tiêu
   - Giải pháp đề xuất
   - Thay đổi dự kiến
   - Rủi ro

2. `02_task.md` có:
   - Checklist markdown (`[x]`, `[ ]`)
   - Task theo phase
   - Exit criteria / DoD / handoff

3. `03_walkthrough.md` có:
   - Tóm tắt thay đổi
   - Testing instructions
   - Reviewer notes

### 2.3 Kiểm tra tính đồng bộ với `kien-truc.md`
- Phase và mục tiêu trong plan/checklist phản ánh đúng roadmap kiến trúc v1.
- Không có task nào vi phạm nguyên tắc incremental migration.

---

## 3) Reviewer Notes

1. **Phạm vi hiện tại**
   - Tập trung vào **context orchestration** (kế hoạch + tasking), chưa commit thay đổi source code kiến trúc.

2. **Cách sử dụng trong sprint**
   - Dùng `02_task.md` làm nguồn theo dõi tiến độ chính.
   - Khi hoàn thành từng batch implementation, cập nhật checklist tương ứng và bổ sung bằng chứng test.

3. **Khuyến nghị bước kế tiếp (ưu tiên)**
   - Bắt đầu **Phase 0** với 3 nhánh nhỏ:
     1) ADR + import boundary rule
     2) env config chuẩn hóa
     3) BFF logging baseline
   - Mỗi nhánh nên đi kèm PR nhỏ, dễ review và rollback.

4. **Điểm cần chú ý khi triển khai thật**
   - Tránh migrate đồng thời quá nhiều domain.
   - Giữ compatibility tạm thời khi tách `shared/schema.ts`.
   - Luôn để backend là source of truth cho AuthZ.

5. **Trạng thái còn lại của Phase 1**
   - Chưa tách endpoint catalog sang `client/src/modules/*/api/*.api.ts`.
   - Chưa tạo đầy đủ module public API (`modules/*/index.ts`).
   - Chưa migrate các page/hook sang `queryKeys` mới đồng nhất.

## 1.2 Cập nhật mới — Phase 0 (Foundation)

Đã hoàn thiện các hạng mục foundation chính trong đợt này:

1. **ADR kiến trúc v1**
   - Tạo `docs/adr-0001-architecture-blueprint-v1.md`.
   - Chốt decision: modular monolith, domain-first, thin BFF, incremental migration.

2. **Boundary guideline**
   - Tạo `docs/import-boundary-guideline.md`.
   - Chuẩn hóa allowed/disallowed import patterns + PR checklist.

3. **Env config chuẩn hóa**
   - Server: tạo `server/config/env.ts` và refactor `server/index.ts` dùng `env.backendUrl`, `env.port`.
   - Client: đã có `client/src/core/config/env.ts` dùng cho API base URL.
   - Cập nhật `.env.example` thêm `PORT` và `VITE_API_BASE_URL`.

4. **BFF logging baseline + health endpoint**
   - Thêm request-id generation/forwarding (`X-Request-ID`) trong `server/index.ts`.
   - Chuẩn hóa access log format có request-id + latency + status.
   - Bổ sung endpoint `/healthz`.

5. **Validation**
   - Đã chạy `npm run check` (TypeScript) và không thấy lỗi mới trong output.

## 1.3 Cập nhật mới — Context Consolidation (Batch 0)

Để tránh context bị “nửa vời”, đã thực hiện đồng bộ tài liệu trong **cùng một context** thay vì tách context mới:

1. **Cập nhật implementation plan**
   - Bổ sung mục `Execution Window — Phase 1 Completion (Current)` trong `01_implementation_plan.md`.
   - Chốt rõ 6 batch thực thi từ dọn context đến validation gates.

2. **Cập nhật task checklist**
   - Điều chỉnh trạng thái đúng thực tế của các mục đã hoàn tất ở Phase 1 (router/providers/core API).
   - Bổ sung section `Current Execution Window — Phase 1 Completion Batches` trong `02_task.md` để theo dõi execution hiện tại.

3. **Nguyên tắc quản lý context được chốt**
   - Giữ nguyên context: `docs/context/20260505_architecture_blueprint_v1_rollout/` cho đến khi hoàn tất rollout chính.
   - Chỉ archive sang `docs/history/` khi hạng mục ổn định/merge.

Trạng thái sau Batch 0:
- Context đã đồng bộ và có thể tiếp tục thực thi code theo Batch 1 mà không gây phân mảnh truy vết.

## 1.4 Cập nhật mới — Phase 1 Completion Execution

Trong đợt này đã hoàn tất phần execution chính của Phase 1 theo batch đã chốt:

1. **Module skeleton + public API**
   - Tạo module structure và public API:
     - `client/src/modules/crm/{api/crm.api.ts,index.ts}`
     - `client/src/modules/hrm/{api/hrm.api.ts,index.ts}`
     - `client/src/modules/accounting/{api/accounting.api.ts,index.ts}`
     - `client/src/modules/rbac/{api/rbac.api.ts,index.ts}`

2. **Tách domain APIs khỏi API catalog tập trung**
   - Di chuyển endpoint chính theo domain sang các file `modules/*/api/*.api.ts`.
   - Giữ `client/src/lib/queryClient.ts` làm bridge dùng lại `apiRequest` để hạn chế regression trong giai đoạn chuyển tiếp.

3. **Migrate consumers trọng điểm**
   - Đã migrate các màn:
     - `client/src/pages/admin/crm/leads.tsx`
     - `client/src/pages/admin/crm/clients.tsx`
     - `client/src/pages/admin/crm/lead-detail.tsx`
     - `client/src/pages/admin/rbac/index.tsx`
   - Đổi import từ `@/lib/queryClient` sang module APIs (`@/modules/crm`, `@/modules/rbac`, `@/modules/hrm`).
   - Áp dụng query key theo namespace domain ở các điểm chính.

4. **Validation kết quả**
   - `npm run check`: pass.
   - `npm run build`: pass.
   - `npm run lint`: chưa chạy được vì hiện tại `package.json` **không có script `lint`**.

5. **Observations**
   - Build có cảnh báo chunk size lớn và PostCSS `from` warning, chưa phải blocker cho rollout hiện tại nhưng nên đưa vào backlog tối ưu.
