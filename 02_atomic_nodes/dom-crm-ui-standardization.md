```yaml
---
id: dom-crm-ui-standardization
title: Chuẩn hóa UI CRM & Sửa lỗi Lead Repository
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Chuẩn hóa UI Components (PageHeader, DataGrid) cho CRM và sửa lỗi Drizzle mapping trong Lead Repository."
tags: [crm, ui-standardization, drizzle-orm, lead-repository, nestjs]
---

## 1. Chuẩn Hóa UI Component (Module CRM)
*   **`PageHeader`**: Bổ sung prop `backUrl: string`, `onBack: () => void`, và `titleBadge: ReactNode` hỗ trợ cho trang chi tiết (`LeadDetail`, `ContractDetail`).
*   **`DataGrid`**: Thay thế bảng thủ công, tích hợp sẵn Pagination, Loading, Empty State và tối ưu responsive (cuộn ngang thông minh).
*   **Hiệu ứng & Trải nghiệm**: Áp dụng Framer Motion cho chuyển trang admin mượt mà và tối ưu hóa loading state.

## 2. Thay Đổi Database Schema & Backend Repository
*   **Schema Update** (`leads.schema.ts`): Thêm giá trị `'RELATIONSHIP'` vào `leadSourceEnum` để khớp với dữ liệu nghiệp vụ thực tế.
*   **Repository Refactor** (`drizzle-lead.repository.ts`):
    *   Refactor phương thức `LeadRepository.save`.
    *   Tách biệt tường minh cơ chế `INSERT` và `UPDATE` thay vì dùng cơ chế save hỗn hợp, giải quyết triệt để lỗi mapping tham số SQL của Drizzle ORM.

## 3. Khắc Phục Lỗi Lead Intake Form (Frontend)
*   Sửa lỗi component Autocomplete bị mất focus khi thay đổi trạng thái nhập liệu.
*   Khắc phục hiện tượng tràn khung hình (overflow layout) trên giao diện di động.

## 4. Tệp tin tác động (Absolute Paths)
*   **Frontend Components & Pages**:
    *   `/home/ka/temps/DentalCarePortal/client/src/pages/admin/crm/clients.tsx`
    *   `/home/ka/temps/DentalCarePortal/client/src/pages/admin/crm/lead-detail.tsx`
    *   `/home/ka/temps/DentalCarePortal/client/src/pages/admin/crm/contract-detail.tsx`
    *   `/home/ka/temps/DentalCarePortal/client/src/components/common/PageHeader.tsx`
*   **Backend Core & Schema**:
    *   `/home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/infrastructure/persistence/drizzle-lead.repository.ts`
    *   `/home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/database/schema/crm/leads.schema.ts`
```