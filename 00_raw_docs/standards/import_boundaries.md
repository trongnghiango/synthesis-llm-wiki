---
title: "Ranh giới Import"
description: "Quy tắc phân cấp import giữa các Module và ngăn coupling chéo domain"
tags: [standards, import, boundaries, dependency]
last_updated: "2026-05-21"
---

# Import Boundary Guideline (v1)

> Nguyên bản từ: `docs/import-boundary-guideline.md`

## Mục tiêu
Giảm coupling liên domain và ngăn deep import vào internals.

## Quy tắc bắt buộc
1. Module domain chỉ expose qua `index.ts` (public API).
2. Không import chéo internals giữa các domain.
3. `shared/*` chỉ chứa contract/primitives/constants kỹ thuật.

## Allowed patterns (Client)
- `@/app/*` -> app bootstrap/router/providers
- `@/core/*` -> infra/core services
- `@/modules/<domain>` -> chỉ import từ public API

## Disallowed patterns
- `@/modules/<domain>/components/*` từ domain khác
- `@/modules/<domain>/api/*` từ domain khác (trừ khi qua `index.ts`)

---
*Vi phạm quy tắc import sẽ bị từ chối merge PR.*
