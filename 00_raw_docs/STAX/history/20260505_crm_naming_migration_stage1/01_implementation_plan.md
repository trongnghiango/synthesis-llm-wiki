# 01 Implementation Plan: CRM Naming Migration (Stage 1 - Backend)

## Mục tiêu
- Chuẩn hóa tên trường từ `companyName` sang `organizationName` để đồng nhất với Module Leads và yêu cầu từ đội Frontend.
- Đổi tên cột trong Database từ `company_name` sang `organization_name`.
- Duy trì tính tương thích ngược cho API (trả về cả 2 trường) trong giai đoạn chuyển tiếp.

## Giải pháp đề xuất

### 1. Database Layer
- Cập nhật `src/database/schema/crm/organizations.schema.ts`.
- Đổi tên cột `company_name` thành `organization_name`.
- Chạy `drizzle-kit generate` để tạo migration.

### 2. Domain Layer
- Refactor `Organization` entity:
  - Đổi interface `OrganizationProps.companyName` thành `organizationName`.
  - Đổi thuộc tính private `_companyName` thành `_organizationName`.
  - Cập nhật các method liên quan (`applyEnterpriseInfo`, v.v.).

### 3. Infrastructure Layer
- **Mapper**: Cập nhật `OrganizationMapper` để chuyển đổi dữ liệu từ DB (organization_name) sang Domain (organizationName).
- **Repository**: Cập nhật `DrizzleOrganizationRepository` để hỗ trợ tìm kiếm (search) trên cột mới.
- **DTO**: Cập nhật `OrganizationResponseDto` để bao gồm cả `organizationName` (mới) và `companyName` (cũ - sẽ bị xóa ở Stage 2).

### 4. Application Layer
- Cập nhật `OrganizationQueryService` và `LeadQueryService` để đảm bảo dữ liệu được trả về đúng chuẩn mới.

## Thay đổi dự kiến
- `src/database/schema/crm/organizations.schema.ts`
- `src/modules/crm/domain/entities/organization.entity.ts`
- `src/modules/crm/infrastructure/mappers/organization.mapper.ts`
- `src/modules/crm/infrastructure/persistence/drizzle-organization.repository.ts`
- `src/modules/crm/infrastructure/dtos/organization-response.dto.ts`
- `src/modules/crm/application/services/organization-query.service.ts`

## Rủi ro
- Các câu truy vấn SQL thuần (nếu có) hoặc các report cũ có thể bị lỗi nếu không được cập nhật tên cột.
- Cần chạy migration cẩn thận để không mất dữ liệu `company_name` hiện có.
