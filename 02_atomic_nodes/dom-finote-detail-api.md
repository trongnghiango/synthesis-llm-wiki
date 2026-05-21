---
id: dom-finote-detail-api
title: Triển khai API Chi tiết Finote & Phân quyền Động
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "API GET /accounting/finotes/:id tích hợp Tenancy Enforcement và cơ chế Server-Driven UI Actions dựa trên vai trò người dùng."
tags: [finote, security, tenancy, server-driven-ui, api]
---

### 1. Luồng Dữ liệu & Tenancy Enforcement
*   **Repository (`DrizzleFinoteRepository`):**
    *   Hàm `findByIdWithAttachments(id, orgId)` thực hiện SQL Query kết hợp quan hệ One-to-Many giữa bảng `Finote` và `Attachment`.
*   **Tenancy Validation:** Ràng buộc chặt chẽ `orgId` của User Session. Nếu không khớp `orgId` của bản ghi, hệ thống ném `EntityNotFoundException` nhằm tránh tấn công dò quét ID (IDOR) theo chuẩn [[arch-tenancy-isolation]].

### 2. Thiết kế API & Server-Driven UI DTO
*   **Endpoint:** `GET /accounting/finotes/:id`
*   **Cấu trúc DTO (`FinoteResponseDto`):**
    *   Chứa danh sách `attachments`.
    *   Cung cấp cấu trúc Metadata `_actions` hỗ trợ dynamic UI render:
    ```typescript
    interface ActionDetailDto {
      allowed: boolean;
      label: string;
      color: string;
      reason?: string; // Lý do hiển thị khi nút bị disabled
    }
    ```
    *   `_actions` map trả về từ Backend: `{ approve: ActionDetailDto, edit: ActionDetailDto, delete: ActionDetailDto }`.

### 3. Logic Phân Quyền (Authorization)
*   **User Entity Mapping:** Đọc trực tiếp `user.roles` từ gốc đối tượng User thay vì qua `profileContext`.
*   **Matrix Phân quyền:**
    *   `Manager`: Hiển thị và cho phép kích hoạt tất cả hành động (`approve.allowed: true`).
    *   `Staff`: Chỉ cho phép `view`/`edit`, ẩn hoặc disable nút `approve` (`approve.allowed: false` kèm `reason`).