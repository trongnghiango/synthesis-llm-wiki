# ADR-0001 — Architecture Blueprint v1 (Modular Monolith, Domain-first)

- Status: Accepted
- Date: 2026-05-05
- Related: `docs/kien-truc.md`

## Context
Codebase hiện tại đã có tách `client/server/shared` nhưng tồn tại các điểm nghẽn scale:
- `client/src/App.tsx` phình to route registry.
- `client/src/lib/queryClient.ts` trộn transport + endpoint catalog nhiều domain.
- `shared/schema.ts` là god-file.
- BFF thiếu chuẩn request-id/logging production baseline.

## Decision
Chọn kiến trúc **Modular Monolith trước, Microservices sau** với nguyên tắc:
1. Domain-first organization ở client (`modules/{domain}` + public API `index.ts`).
2. Contract-first ở `shared/contracts/*`.
3. Thin BFF: proxy/orchestration nhẹ + observability cơ bản.
4. Incremental migration theo phase, không big-bang rewrite.

## Consequences
### Positive
- Giảm coupling liên domain, dễ scale team.
- Giảm conflict trên file trung tâm.
- Nâng khả năng kiểm thử/quan sát hệ thống.

### Trade-offs
- Tăng số lượng file và yêu cầu kỷ luật import boundary.
- Cần migration plan rõ theo batch để tránh regression.

## Rollout Notes
- Phase 0: foundation (ADR, env config, boundary rules, logging baseline).
- Phase 1+: thực thi theo checklist trong `docs/context/20260505_architecture_blueprint_v1_rollout/02_task.md`.
