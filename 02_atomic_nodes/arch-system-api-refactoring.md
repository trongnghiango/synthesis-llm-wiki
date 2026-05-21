---
id: arch-system-api-refactoring
title: Tách biệt SystemModule & Chuẩn hóa Backend-Driven UI Actions
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on: []
summary: "Tái cấu trúc SystemModule qua Lookup/Bootstrap Service và chuẩn hóa tương tác Backend-Driven UI qua ActionableDto."
tags: [system-module, backend-driven-ui, actionable-dto, refactoring, crm-api]
---

## 1. Tái Cấu Trúc SystemModule
*   **Pattern**: Dịch chuyển toàn bộ business logic ra khỏi `SystemController` vào hai Service chuyên biệt:
    *   `LookupService`: Quản lý truy vấn danh mục, dữ liệu tĩnh hệ thống.
    *   `BootstrapService`: Xử lý khởi tạo và cấu hình ứng dụng ban đầu.
*   **Mục tiêu**: Đảm bảo Single Responsibility, Controller chỉ làm nhiệm vụ định tuyến và phân phối request.

## 2. Chuẩn Hóa Tương Tác Backend-Driven UI (`_actions`)
Hỗ trợ Frontend giảm thiểu logic kiểm tra điều kiện hiển thị nút/action bằng cách trả về metadata quyền trực tiếp từ API:

```typescript
export interface ActionableDto<T> {
  data: T;
  _actions: {
    [actionKey: string]: {
      allowed: boolean;
      reason?: string; // Giải thích chi tiết nếu action bị chặn (allowed = false)
    };
  };
}
```

## 3. Cập Nhật API Contracts
*   **Phân phối Lead**:
    *   `PATCH /crm/leads/:id/assign`
    *   Payload: `{ assigneeId: string }`
*   **Báo cáo hiệu suất nhóm**:
    *   `GET /system/my-team/summary`
    *   Response: `{ totalLeads: number, conversionRate: number, activeMembers: number }`