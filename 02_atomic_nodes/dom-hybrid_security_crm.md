---
id: dom-hybrid_security_crm
title: Mô hình Bảo mật Lai cho CRM
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[arch-als-tenant-isolation]]"
summary: "Thiết kế bảo mật lai 3 lớp áp dụng cho module CRM Leads: Guard (Controller), Query Isolation (Repo), và Dynamic Actions (DTO)."
tags: [security, crm, hybrid-security, acl, action-dto]
---

### 1. Kiến trúc Bảo mật Lai 3 Lớp (Pragmatic Hybrid Security)
*   **Layer 1 (Guard - Controller):** Chặn thô bằng `@Permissions` decorator.
    *   `GET /crm/leads` & `GET /crm/leads/:id` -> `crm:leads:read`
    *   `PATCH /crm/leads/:id/assign` & `POST /crm/leads/:id/won` -> `crm:leads:edit`
    *   `POST /crm/leads/intake` -> `crm:leads:create`
*   **Layer 2 (Query Isolation):** `LeadQueryService` tự động áp `organizationId` từ ngữ cảnh người dùng để cô lập dữ liệu (xem `[[arch-als-tenant-isolation]]`).
*   **Layer 3 (Dynamic Action Logic):** Tính toán quyền hạn động tại cấp bản ghi và trả về Frontend qua DTO.

### 2. Thiết kế API & DTO Contract
`LeadResponseDto` kế thừa từ `ActionableDto` cung cấp metadata hành động (`_actions`):

```typescript
interface ActionState {
  allowed: boolean;
  reason?: string;
}

interface LeadResponseDto {
  id: string;
  title: string;
  organizationId: string;
  _actions: {
    edit: ActionState;     // Logic: !isClosed && (isOwner || isAdmin)
    assign: ActionState;   // Logic: !isClosed && isAdmin
    won: ActionState;      // Logic: !isClosed && isOwner
  };
}
```

*Mẫu logic phán xử động tại Service:*
```typescript
const editAllowed = !lead.isClosed && (user.id === lead.ownerId || user.role === 'admin');
const editReason = lead.isClosed ? 'Lead đã đóng, không thể sửa' : 'Bạn không phụ trách Lead này';
```