---
id: dom-crm-ui-standardization
title: Chuẩn hóa UI Component Module CRM & Sửa Lỗi Lead Intake
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Chuẩn hóa UI CRM qua PageHeader/DataGrid và tách biệt logic INSERT/UPDATE của Drizzle ORM để sửa lỗi lưu Lead."
tags: [crm, ui-ux, refactor, drizzle, nestjs, bug-fix]
---

### 1. Nâng cấp & Đồng bộ UI/UX (Frontend)
- **`PageHeader`** (`/home/ka/temps/DentalCarePortal/client/src/components/common/PageHeader.tsx`):
  - Bổ sung các props: `backUrl: string`, `onBack?: () => void`, và `titleBadge?: React.ReactNode` để tối ưu cho trang Detail.
- **`DataGrid`**: Tích hợp sẵn Phân trang (Pagination), Trạng thái tải (Loading), Trạng thái trống (Empty State) và tự động cuộn ngang (Responsive).
- **Phạm vi áp dụng**: 
  - Refactor các trang danh sách và chi tiết tại `/home/ka/temps/DentalCarePortal/client/src/pages/admin/crm/` gồm: `clients.tsx`, `lead-detail.tsx`, và `contract-detail.tsx`.
  - Tích hợp `framer-motion` cho hiệu ứng chuyển trang mượt mà trong phân hệ Admin.

### 2. Khắc phục Logic Backend & Database Schema
- **Database Schema** (`/home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/database/schema/crm/leads.schema.ts`):
  - Bổ sung giá trị `'RELATIONSHIP'` vào `leadSourceEnum` để khớp với dữ liệu thực tế từ Client.
- **Repository Pattern** (`/home/ka/Repos/github.com/trongnghiango/rbac-nest-project/src/modules/crm/infrastructure/persistence/drizzle-lead.repository.ts`):
  - Tái cấu trúc hàm `LeadRepository.save()`. 
  - Phân tách tường minh hành vi `INSERT` (khi không có ID/chưa tồn tại) và `UPDATE` thay vì dùng cơ chế tự động suy đoán để tránh lỗi mapping tham số truy vấn SQL của Drizzle ORM.