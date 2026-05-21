```yaml
---
id: dom-professional-activity-feed-and-structured-metadata
title: Hệ Thống Activity Feed & Siêu Dữ Liệu CRM
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
summary: "Chuẩn hóa cấu trúc AuditEntryPayload hỗ trợ actor tracking và cơ chế aggregation cho Activity Feed trong phân hệ CRM."
tags: [crm, activity-feed, audit-log, event-driven, actor-tracking]
---

### 1. Kiến Trúc Payload & Actor Tracking
Nâng cấp `AuditEntryPayload` để hỗ trợ truy vết tác nhân hệ thống ở cấp độ gốc (root-level actor tracking):
```typescript
interface AuditEntryPayload {
  actorId?: string;     // ID người thực hiện hành động
  actorName?: string;   // Tên hiển thị của người thực hiện
  [key: string]: any;   // Metadata nghiệp vụ bổ sung
}
```
*   **Đồng bộ hóa các Event:** `LeadCreatedEvent`, `OrganizationCreatedEvent`, `QuoteCreatedEvent`, `QuoteStatusChangedEvent`, `LeadStatusChangedEvent`, `LeadAssignedEvent` đều bắt buộc đính kèm root-level actor thông qua `LeadController` và `LeadIntakeService`.

### 2. Luồng Xử Lý Sự Kiện & Chuyển Đổi Lead-to-Contract
*   **`ContractCreatedEvent`**: Định dạng siêu dữ liệu sạch (Clean Metadata) chứa thông tin tài chính cốt lõi:
    ```typescript
    interface ContractCreatedEventMetadata {
      fee: number;          // Giá trị hợp đồng
      taxCode: string;      // Mã số thuế
      serviceType: string;  // Loại hình dịch vụ
    }
    ```
*   **Đăng ký Tự động**: `AuditDomainEventHandler` lắng nghe và tự động ghi chép lịch sử hợp đồng vào Audit Log ngay khi chuyển đổi Lead thành công.

### 3. Cơ Chế Aggregation & Formatter trên Activity Feed
*   **`ActivityFeedService` (Smart Aggregation)**: Khi truy vấn Timeline của `Lead`, hệ thống tự động gộp và hiển thị cả sự kiện tạo `Organization` cha liên kết để tối ưu hóa góc nhìn toàn diện cho Sales.
*   **`ActivityFormatter`**: Định nghĩa mapping hiển thị trực quan (chữ Việt hóa, icon nghiệp vụ phù hợp) cho các sự kiện cốt lõi:
    *   `LEAD.STATUS_CHANGED` (Thay đổi trạng thái Lead)
    *   `CONTRACT.CREATED` (Khởi tạo Hợp đồng)
```