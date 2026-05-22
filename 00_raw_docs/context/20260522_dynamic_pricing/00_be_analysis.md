# 00 Business Analysis: Bieu phi dong & Doanh thu bac thang CRM - Billing

Tài liệu phân tích nghiệp vụ và kiến trúc cho tính năng biểu phí động và tính phí theo doanh thu bậc thang tại dự án STAX.

## A. Phan loai module
- **Tier Level**: Tier 3 - Process Flow.
- **Lý do**: Đây là luồng nghiệp vụ xử lý giao dịch thương mại và tài chính trực tiếp giữa doanh nghiệp và khách hàng ( CRM -> Hợp đồng -> Hóa đơn/Finote).
- **Phụ thuộc**: Phụ thuộc vào các module Tier 2 (Organization, Customer, Employee) và các module Tier 3 khác (Accounting, Contracts).

## B. Bounded Context & Ubiquitous Language
Bảng đối chiếu ngôn ngữ nghiệp vụ sang ngôn ngữ kỹ thuật trong mã nguồn:

| Thuật ngữ Nghiệp vụ | Thuật ngữ Kỹ thuật | Phạm vi Context |
|---|---|---|
| Mô hình tính giá | `PricingModel` (FIXED, MANUAL_AGREEMENT, TIERED_REVENUE) | CRM / Catalog / Contracts |
| Biểu phí bậc thang doanh thu | `TieredRevenueConfig` (Mảng chứa các mốc min/max doanh thu và mức phí) | CRM / Catalog / Contracts |
| Hợp đồng giá động | Hợp đồng có `pricingModel` là `MANUAL_AGREEMENT` hoặc `TIERED_REVENUE` | Contracts |
| Phiếu thu cọc ban đầu | `Finote` loại `INCOME` sinh ra lúc chốt Won Lead giá động | Accounting / Finote |
| Doanh thu thực tế của khách | `actualRevenue` dùng để áp công thức tính phí | Accounting / Finote |

## C. Data Flow & API Design

### 1. Luồng dữ liệu
Client (Won Lead Dialog) -> `LeadController.closeLead()` -> `LeadWorkflowService.closeLeadAsWon()` -> Tạo Hợp đồng (`ContractRepository`) & Hạng mục hợp đồng (`ContractItemRepository`) -> Tạo phiếu thu cọc ban đầu (`FinoteService`) -> Ghi dữ liệu xuống DB.

### 2. Thiết kế API Endpoints
Cập nhật API Endpoint chốt Won Lead hiện tại:
- **Endpoint**: `POST /api/crm/leads/:id/won`
- **Quyền**: `lead:edit`
- **Request Payload DTO**: [close-lead.request.dto.ts](backend/src/modules/crm/infrastructure/dtos/close-lead.request.dto.ts)
  - Chuyển `feeAmount` thành optional.
  - Bổ sung `pricingModel` (Enum: FIXED, MANUAL_AGREEMENT, TIERED_REVENUE).
  - Bổ sung `pricingConfig` (JSONB chứa thông tin bậc thang).

## D. Cross-module dependencies
- `CRM` module giao tiếp trực tiếp với `Contracts` module để khởi tạo thực thể Hợp đồng và Hạng mục hợp đồng.
- `CRM` module gọi `Accounting` module (thông qua `FinoteService` hoặc `accountingApi`) để tạo phiếu thu đặt cọc ban đầu trong cùng một nghiệp vụ chốt Won Lead.
- Phát Domain Event: Phát event `LeadWonEvent` sau khi Transaction chốt lead hoàn tất thành công.

## E. Multi-tenancy
- Tất cả dữ liệu của Hợp đồng, Lead, Finote, và Dịch vụ đều được cô lập và lọc theo `organizationId` lấy từ ALS (Async Local Storage) / JWT.
- Không bypass tenant isolation.

## F. Security (_actions / Server-Driven UI)
- Chỉ hiển thị nút "Chốt Hợp Đồng" khi Lead có trạng thái hợp lệ và user có quyền `lead:edit` (trả về qua thuộc tính `_actions.close_won.allowed`).
- Cấu hình biểu phí mẫu tại Catalog Dịch vụ chỉ cho phép tài khoản có quyền `service:edit` thực hiện.
