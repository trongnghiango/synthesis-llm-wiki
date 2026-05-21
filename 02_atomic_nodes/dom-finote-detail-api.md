```yaml
---
id: dom-finote-detail-api
title: Triển khai API Chi tiết Finote & Phân quyền Động
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
  - "[[arch-tenant-isolation]]"
summary: "API chi tiết Finote hỗ trợ đa thuê sở (Tenancy) và cơ chế phân quyền động phục vụ Server-Driven UI."
tags: [finote, accounting, api, tenancy, authorization, server-driven-ui]
---
```

## 1. API Contract & Thiết kế Dữ liệu

### Endpoint
`GET /api/accounting/finotes/:id`

### Cấu trúc Schema Response nâng cao (`FinoteResponseDto`)
Hỗ trợ cơ chế **Server-Driven UI** qua metadata `_actions`:
```typescript
interface ActionDetailDto {
  allowed: boolean;
  label?: string;   // Label hiển thị trên nút
  color?: string;   // Mã màu hiển thị (e.g. primary, danger)
  reason?: string;  // Lý do bị disable (nếu allowed = false)
}

interface FinoteResponseDto {
  id: string;
  orgId: string;
  attachments: Attachment[];
  _actions: Record<string, ActionDetailDto>; // Quyền: Approve, Edit, View...
}
```

## 2. Kiến trúc Xử lý & Luồng Nghiệp vụ

### Tầng Dữ liệu (Repository)
* `DrizzleFinoteRepository.findByIdWithAttachments`: Sử dụng SQL Query tối ưu để nạp kèm quan hệ 1-N `attachments` trong cùng một phiên truy vấn thay vì lazy load.

### Tầng Nghiệp vụ (Service & Security)
1. **Tenancy Enforcement**: `FinoteService.getById` bắt buộc đối chiếu chéo `OrgId` của User đang đăng nhập với `OrgId` của bản ghi Finote. Trả về `EntityNotFoundException` nếu không khớp để ngăn chặn việc dò quét dữ liệu chéo (ID harvesting).
2. **Quyết định Quyền hạn (RBAC)**:
   * **Manager**: Được cấp quyền `Approve`, `Edit`, `View`.
   * **Staff**: Chỉ được cấp quyền `View`, `Edit`. Quyền `Approve` set `allowed: false` kèm `reason` cụ thể.
   * *Lưu ý sửa lỗi*: Truy cập trực tiếp qua `user.roles` tại Controller (thay thế cho `user.profileContext.roles` cũ).

## 3. Hướng dẫn Tích hợp Frontend
* Kiểm tra `_actions[actionName].allowed` để ẩn/hiện hoặc disable nút bấm.
* Sử dụng trực tiếp `label` và `color` từ API trả về để đồng bộ giao diện mà không cần hardcode logic phân quyền ở client.