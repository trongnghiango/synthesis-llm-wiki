---
id: dom-manage-position-department-ui
title: Giao diện Quản lý Định biên & Phân bổ Nhân sự
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Thiết kế Kanban Staffing Board và chuẩn hóa API nghiệp vụ quản lý chức vụ, phân bổ nhân sự."
tags: [hrm, staffing-board, org-structure, api-contract]
---

## 1. API Contracts (`hrm.api.ts`)
```typescript
export interface Position {
  id: string;
  title: string;
  departmentId: string;
  maxSlots: number; // Định biên tối đa
  filledSlots: number;
}

export interface AssignmentPayload {
  employeeId: string;
  positionId: string;
  departmentId: string;
  effectiveDate: string;
}

// Endpoints chuẩn hóa:
// - GET/POST/PUT /api/v1/positions
// - POST /api/v1/assignments (Phân bổ nhân sự mới)
```

## 2. Thiết kế Luồng UI & Component
- **Staffing Board (Kanban Mode):** Chế độ xem trực quan tích hợp trong `OrgStructurePage`.
  - **Cột (Columns):** Chức vụ (`Position`) nhóm theo Phòng ban (`Department`), hiển thị chỉ số định biên (e.g., 2/5 Slots).
  - **Thẻ (Cards):** Nhân sự (`Employee`). Cho phép Drag-and-Drop giữa các cột để kích hoạt `AssignmentModal`.
- **PositionModal:** Khởi tạo/chỉnh sửa định biên chức vụ trực tiếp từ Sidebar cấu trúc tổ chức.
- **AssignmentModal:** Form tái sử dụng để cấu hình chi tiết phân bổ (chức vụ, phòng ban, ngày hiệu lực).