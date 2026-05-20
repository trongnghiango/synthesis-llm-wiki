# Context: Organization Structure Management
**Date**: 2026-05-07
**Status**: Completed

## 1. Goal
Xây dựng trang quản lý sơ đồ tổ chức trực quan, quản lý phân cấp phòng ban, đội nhóm và chức vụ, liên kết với dữ liệu nhân sự (HRM).

## 2. Proposed Changes
### Backend / Shared
- [NEW] `shared/contracts/hrm.ts`: Định nghĩa schema cho Department, Position, Employee.
- [MODIFY] `shared/index.ts`: Export hrm contracts.

### Frontend
- [MODIFY] `client/src/modules/hrm/api/hrm.api.ts`: Thêm các endpoint quản trị tổ chức.
- [NEW] `client/src/components/hrm/OrgChart.tsx`: Component sơ đồ cây trực quan.
- [MODIFY] `client/src/pages/admin/hrm/org-structure.tsx`: Trang quản trị chính với side panel chi tiết.

## 3. Architecture Compliance
- Tuân thủ ranh giới module HRM.
- Sử dụng Contract-First để định nghĩa API.
- Đảm bảo UI/UX theo Material Design 3 healthcare refinements.
