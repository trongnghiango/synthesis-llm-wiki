# Bước 1: Phân tích Nghiệp vụ & Kiến trúc — Module Service Catalog

## A. Phân loại module
- **Phân loại:** Tier 3 — Process Flow.
- **Lý do:** Module này phục vụ trực tiếp cho dòng chảy bán hàng (CRM), quản lý các hạng mục hàng hóa/dịch vụ để đưa vào Báo giá (Quote) và Hợp đồng (Contract).
- **Phụ thuộc:** Phụ thuộc vào `Core` (Shared types).
- **Module phụ thuộc nó:** `CRM` (Quotes, Contracts) sẽ phụ thuộc vào `Service Catalog` để chuẩn hóa dữ liệu đầu vào.

## B. Bounded Context & Ubiquitous Language
- **Domain:** Service Catalog & Product Management.
- **Ubiquitous Language:**
  | Tên nghiệp vụ | Tên kỹ thuật | Mô tả |
  |---|---|---|
  | Dịch vụ | `Service` | Đơn vị dịch vụ nhỏ nhất (VD: Khai báo thuế tháng). |
  | Gói dịch vụ | `ServicePackage` | Tập hợp nhiều dịch vụ hoặc một dịch vụ lớn. |
  | Loại hình | `ServiceType` | Định nghĩa cách tính phí (RETAINER - Định kỳ, ONE_OFF - Vụ việc). |
  | Đơn giá gốc | `BasePrice` | Giá tham chiếu cơ bản trước khi chiết khấu. |

## C. Data Flow & API Design
- **Flow:** User → ServiceController → ServiceCatalogService → ServiceRepository → DB.
- **API Endpoints:**
  - `GET /api/services`: Lấy danh sách dịch vụ (có phân trang, search, filter theo type/status).
  - `GET /api/services/:id`: Chi tiết dịch vụ.
  - `POST /api/services`: Tạo mới dịch vụ (Admin only).
  - `PATCH /api/services/:id`: Cập nhật thông tin dịch vụ.
  - `DELETE /api/services/:id`: Lưu trữ (Archive) dịch vụ, không xóa cứng để bảo vệ tính toàn vẹn của Hợp đồng cũ.

## D. Cross-module dependencies
- **CRM Module:** Cần gọi `ServiceCatalogService` để lấy thông tin dịch vụ khi tạo Quote Items.
- **Events:** Phát event `ServiceCreatedEvent`, `ServiceUpdatedPriceEvent` (nếu cần tracking biến động giá).

## E. Multi-tenancy
- **Tenant Isolation:** Dữ liệu dịch vụ có thể là Global (STAX cung cấp chung) hoặc Tenant-specific (nếu STAX cho phép khách hàng tự định nghĩa dịch vụ của riêng họ). 
- **Quyết định:** Giai đoạn 1 sẽ là Global (mọi tenant dùng chung danh mục của STAX). Cần bypass tenant check hoặc gán `organizationId = 0` cho hệ thống.

## F. Security (_actions / Server-Driven UI)
- **Entity:** `Service`
- **Actions:** 
  - `canEdit`: Dành cho role Admin hệ thống.
  - `canSelect`: Dành cho Sales/Accountant khi soạn báo giá.

---
Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết.
