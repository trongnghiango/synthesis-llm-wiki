# Bước 1️⃣: Phân tích Nghiệp vụ & Kiến trúc (fix_lead_acquired_at_display)

## A. Phân loại module
- **Tier**: Tier 3 — Process Flow (CRM Module).
- **Phụ thuộc**: CRM phụ thuộc vào các module Tier 2 (User, Employee, OrgStructure) và Tier 1 (Rbac, AuditLog). Thay đổi này chỉ sửa đổi cách trả về dữ liệu của CRM Lead API (`LeadResponseDto` và `LeadQueryService`).

## B. Bounded Context & Ubiquitous Language
Bảng đối trọng thuật ngữ nghiệp vụ và kỹ thuật liên quan:

| Tên nghiệp vụ STAX | Tên kỹ thuật trong Code/DB | Kiểu dữ liệu | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- | :--- |
| Ngày tiếp nhận | `acquiredAt` / `acquired_at` | `timestamp` / `Date` | Ngày khách hàng liên hệ thực tế (ghi nhận từ Excel/CSV lịch sử hoặc lúc tạo mới). |
| Ngày tạo hệ thống | `createdAt` / `created_at` | `timestamp` / `Date` | Ngày bản ghi được insert vào database hệ thống STAX. |

## C. Data Flow & API Design
- **Luồng dữ liệu**:
  - `GET /crm/leads` -> `LeadController.getLeads()` -> `LeadQueryService.getListLeads()` -> `ILeadRepository.findAll()` -> `LeadMapper.toDomain()` -> Trả về `Lead` entity.
  - Sau đó, `LeadQueryService.mapToResponse()` chuyển đổi `Lead` entity thành `LeadResponseDto`.
- **Vấn đề hiện tại**: `LeadResponseDto` bị thiếu trường `acquiredAt`. Do đó, hàm `mapToResponse` không map trường này từ entity sang DTO. Frontend khi nhận dữ liệu không có `acquiredAt` nên fallback về `createdAt` (vốn là ngày chạy migration seed dữ liệu giống hệt nhau cho toàn bộ lead).
- **Giải pháp**: Bổ sung `acquiredAt` vào `LeadResponseDto` và map nó trong `LeadQueryService.mapToResponse`.

## D. Cross-module dependencies
- Thay đổi này cô lập hoàn toàn trong module CRM, không ảnh hưởng hay gọi chéo module khác.

## E. Multi-tenancy
- API danh sách Leads đã lọc theo `organizationId` của User hiện tại qua `LeadQueryService.getListLeads()` và `DrizzleLeadRepository.findAll()`. Thay đổi này không làm ảnh hưởng hay thay đổi logic multi-tenancy sẵn có.

## F. Security (`_actions` / Server-Driven UI)
- Giữ nguyên cấu trúc logic `_actions` hiện có (xác định quyền `view`, `edit`, `assign`, `close_won` dựa trên trạng thái đóng/mở của Lead và ownership của Employee/Admin).

---
Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết.
