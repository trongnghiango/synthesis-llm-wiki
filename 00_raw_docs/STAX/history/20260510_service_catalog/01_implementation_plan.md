# Bước 2: Kế hoạch Kiến trúc Chi tiết — Module Service Catalog

## A. Database Schema (Drizzle ORM)

### 1. Bảng `services` (Danh mục dịch vụ)
- **File:** `src/database/schema/crm/services.schema.ts`
- **Cấu trúc:**
  - `id`: serial primary key
  - `name`: text, not null
  - `description`: text
  - `type`: `service_type` enum ('ONE_OFF', 'RETAINER', 'SUBSCRIPTION')
  - `status`: `service_status` enum ('ACTIVE', 'INACTIVE', 'ARCHIVED')
  - `basePrice`: numeric(15, 2), default '0'
  - `currency`: text, default 'VND'
  - `createdAt`, `updatedAt`: timestamp

### 2. Cập nhật `quote_items`
- **File:** `src/database/schema/crm/quotes.schema.ts`
- **Thay đổi:** Thêm cột `serviceId` (integer, nullable) references `services.id`.

### 3. Bảng `contract_items` (Hạng mục hợp đồng)
- **File:** `src/database/schema/crm/contracts.schema.ts` (hoặc tạo mới file riêng trong folder crm)
- **Lý do:** Hiện tại `contracts` đang lưu value tổng. Cần bảng items để quản lý chi tiết dịch vụ đang thực hiện.
- **Cấu trúc:**
  - `id`: serial primary key
  - `contractId`: integer references `contracts.id`
  - `serviceId`: integer references `services.id` (nullable để hỗ trợ dịch vụ tùy chỉnh không có trong danh mục)
  - `description`: text (lưu snapshot tên dịch vụ tại thời điểm ký)
  - `quantity`: numeric(10, 2)
  - `unitPrice`: numeric(15, 2)
  - `amount`: numeric(15, 2)

## B. Domain Layer

### 1. Entity `Service`
- **Path:** `src/modules/crm/domain/entities/service.entity.ts`
- **Methods:**
  - `activate()`, `deactivate()`, `archive()`
  - `updatePrice(newPrice: number)`

### 2. Repository Port `IServiceRepository`
- **Path:** `src/modules/crm/domain/repositories/service.repository.ts`
- **Token:** `Symbol('IServiceRepository')`
- **Methods:** `findById`, `findAll`, `save`, `delete`

## C. Infrastructure Layer

### 1. Mapper `ServiceMapper`
- **Path:** `src/modules/crm/infrastructure/mappers/service.mapper.ts`
- **Methods:** `toDomain`, `toPersistence`

### 2. Implementation `DrizzleServiceRepository`
- **Path:** `src/modules/crm/infrastructure/persistence/drizzle-service.repository.ts`

## D. Application Layer

### 1. `ServiceCatalogService`
- **Methods:** `getServiceList`, `getServiceDetail`, `createService`, `updateService`

### 2. Integration: `LeadWorkflowService`
- Cập nhật logic `closeLeadAsWon`: Tự động copy dữ liệu từ `quote_items` (có `serviceId`) sang `contract_items` mới.

## E. Presentation Layer

### 1. `ServiceController`
- **Path:** `src/modules/crm/infrastructure/controllers/service.controller.ts`
- **Routes:** 
  - `GET /crm/services` (Public/Auth)
  - `POST /crm/services` (Admin only)
  - `PATCH /crm/services/:id` (Admin only)

## F. Module Wiring
- Cập nhật `CRMModule` để bind `IServiceRepository` và `ServiceCatalogService`.

---
Kế hoạch này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
