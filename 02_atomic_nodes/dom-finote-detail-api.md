---
id: dom-finote-detail-api
title: API Chi Tiết Finote & Server-Driven UI
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
  - "[[arch-tenancy-isolation]]"
summary: "API lấy chi tiết Finote tích hợp Tenancy Isolation và Metadata Actions hỗ trợ Server-Driven UI."
tags: [accounting, finote, tenancy, server-driven-ui, api]
---

### 1. Luồng Nghiệp Vụ & Tenancy
* **Data Access**: `DrizzleFinoteRepository.findByIdWithAttachments` sử dụng SQL Join để gom dữ liệu Finote và danh sách `attachments`.
* **Tenancy Enforcement**: `FinoteService.getById` bắt buộc đối khớp `orgId` của Finote với `user.orgId`. Ném `EntityNotFoundException` nếu vi phạm để đảm bảo bảo mật.
* **Role Check**: Truy cập `user.roles` trực tiếp tại root entity của User để phân quyền xử lý `_actions`.

### 2. Thiết Kế Server-Driven UI (SDUI)
Để đồng nhất giao diện, API trả về metadata `_actions` định nghĩa trạng thái của các nút bấm dựa trên vai trò (Manager/Staff):
* **DTO Mở Rộng (`ActionDetailDto`)**:
  ```typescript
  type ActionDetailDto = {
    allowed: boolean;
    label: string;
    color: string;
    reason?: string;
  }
  ```
* **Quy tắc Frontend**:
  * `allowed === true`: Hiển thị nút với `label` và `color` từ backend.
  * `allowed === false`: Disable nút và hiển thị tooltips giải thích bằng `reason`.

### 3. API Contract
* **Endpoint**: `GET /api/accounting/finotes/:id`
* **Response Highlight (`FinoteResponseDto`)**:
  ```json
  {
    "id": "string",
    "attachments": [],
    "_actions": {
      "approve": { "allowed": false, "label": "Duyệt", "color": "green", "reason": "Chỉ dành cho Manager" },
      "edit": { "allowed": true, "label": "Sửa", "color": "blue" }
    }
  }
  ```