# 01 Implementation Plan: Architecture v1 Adoption & Context Standardization

## Mục tiêu
- Đồng bộ hóa Backend NestJS với tiêu chuẩn **Architecture v1** (Standardized monorepo/contract approach).
- Áp dụng quy trình quản lý bối cảnh mới (`CONTRIBUTING_WORKFLOW.md`).
- Chuẩn hóa hệ thống phân quyền (RBAC) và API Bootstrap cho Frontend v1.

## Giải pháp đề xuất
1.  **RBAC Standardization**: Đổi tên resource trong `01_rbac_rules.csv` sang định dạng `domain:action` (crm, accounting, hrm, system).
2.  **Bootstrap API Upgrade**: Nâng cấp `BootstrapService` để trả về `rawPermissions` và các flags tương ứng.
3.  **Context Migration**: Di chuyển tài liệu làm việc vào `docs/STAX/context/20260505_architecture_v1_adoption/`.
4.  **Unit Testing**: Đảm bảo các thay đổi được kiểm chứng bằng test suite.

## Thay đổi dự kiến
- `database/seeds/01_rbac_rules.csv`: Cập nhật resource names.
- `src/modules/system/application/services/bootstrap.service.ts`: Thay đổi cấu trúc response.
- `src/modules/system/application/services/bootstrap.service.spec.ts`: Thêm mới unit test.
- `docs/STAX/context/architecture.md`: Thêm Section 9.
- `docs/STAX/context/changelog.md`: Ghi nhận thay đổi.

## Rủi ro
- Thay đổi resource name có thể ảnh hưởng đến các service đang check quyền bằng string cũ. (Đã rà soát: chủ yếu dùng Decorator/Guard, cần kiểm tra logic logic bypass).
