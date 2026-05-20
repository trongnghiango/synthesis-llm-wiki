# Phân tích Nghiệp vụ & Kiến trúc Backend (00_be_analysis.md)
**Feature:** CRM Lead Stage Transition (Kanban Support) & Reports
**Date:** 2026-05-20

## A. Phân loại module
- **Phân tầng:** Module `CRM` là **Tier 3 (Process Flow)** vì nó xử lý các quy trình nghiệp vụ khách hàng (Leads, Hợp đồng, Báo giá) và phụ thuộc vào các module Tier 2 (`Employee`, `OrgStructure`, `User`) cùng các module Tier 1 (`Rbac`, `Logging`, `System`).
- **Phụ thuộc:**
  - Phụ thuộc xuôi: `user`, `employee`, `org-structure`, `system` (Lookup, Bootstrap), `logging` (Audit Log).
  - Phụ thuộc ngược: Không có module Tier 1 hay Tier 2 nào được phụ thuộc ngược lại vào `CRM`.

## B. Bounded Context & Ubiquitous Language
- **Domain:** Quản lý đường ống bán hàng (Sales Pipeline) trong CRM.
- **Bảng đối trọng (Ubiquitous Language):**
  | Thuật ngữ STAX (Nghiệp vụ) | Tên kỹ thuật trong code | Ghi chú |
  | :--- | :--- | :--- |
  | Cơ hội kinh doanh / Lead | `Lead` (Domain Entity) | Thực thể ghi nhận nhu cầu của KH |
  | Giai đoạn Lead | `LeadStage` (Enum) | `NEW`, `CONSULTING`, `NEGOTIATING`, `WON`, `LOST` |
  | Chuyển trạng thái Lead | `transitionTo(newStage)` | Phương thức nghiệp vụ đổi trạng thái |
  | Sự kiện đổi trạng thái | `LeadStatusChangedEvent` | Phát hành qua `IEventBus` để ghi Audit Log |

## C. Data Flow & API Design
- **Luồng dữ liệu:**
  `Client (FE) -> BFF Proxy -> Controller (LeadController) -> Application Service (LeadWorkflowService) -> Domain Entity (Lead) -> Repository (ILeadRepository) -> Database`
- **Thiết kế API:**
  Chúng ta sẽ tích hợp cập nhật trạng thái (`stage`) trực tiếp vào API cập nhật Lead hiện tại:
  - **Method:** `PATCH`
  - **Path:** `/crm/leads/:id`
  - **Permission:** `lead:edit`
  - **Payload:** `UpdateLeadRequestDto` bổ sung thuộc tính `stage` kiểu `LeadStage`.

## D. Cross-module dependencies
- **Giao tiếp liên module:**
  - Phát hành `LeadStatusChangedEvent` (implements `IAuditableEvent`) lên `IEventBus` sau khi lưu thành công.
  - Hệ thống `AuditLog` (Tier 1) sẽ lắng nghe sự kiện này qua event handler để tự động ghi chép log (Deep Diff).
  - Không phát sinh liên kết coupling trực tiếp nào khác.

## E. Multi-tenancy & Isolation
- **Tenant Isolation:** Dữ liệu Leads được phân vùng theo `organizationId`. Việc kiểm tra quyền hạn cập nhật Lead đã được cài đặt sẵn qua `JwtAuthGuard` và việc tải Entity từ Database chỉ cho phép người dùng thao tác trên Lead mà họ được gán hoặc thuộc tổ chức của họ (thực thi ở tầng Service/Repository).
- **Bypass:** Không bypass.

## F. Security & UI Actions (_actions)
- **Server-Driven UI:**
  - `LeadResponseDto` trả về `_actions` bao gồm:
    - `edit.allowed`: Quyết định xem người dùng có quyền chỉnh sửa / kéo thả trên Kanban không. Chỉ cho phép khi Lead chưa đóng (chưa WON/LOST) và User là Owner (người phụ trách) hoặc Admin.
    - `close_won.allowed`: Chỉ cho phép chốt hợp đồng khi Lead chưa đóng và User có quyền chỉnh sửa.
  - Frontend sẽ đọc `lead._actions.edit.allowed` để xác định xem card Lead có cho phép kéo thả hay không.

---
Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết.
