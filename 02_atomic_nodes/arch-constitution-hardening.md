---
id: arch-constitution-hardening
title: Tăng cường Tuân thủ Constitution STAX
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-delta-logging]]"
  - "[[dom-accounting-finote]]"
summary: "Thiết kế kiến trúc Event-Driven Audit Log, chuẩn hóa Domain Exception và tái cấu trúc Bootstrap Service tuân thủ STAX Constitution."
tags: [architecture, event-driven, audit-log, domain-exception, clean-architecture]
---

## 1. Kiến trúc Event-Driven Audit Log
Chuyển đổi cơ chế ghi log thủ công sang mô hình Pub/Sub hướng sự kiện để đảm bảo decoupling:
- **Sự kiện Domain**: `LeadStatusChangedEvent`, `LeadAssignedEvent`, `FinoteStatusChangedEvent`.
- **Luồng xử lý**: `LeadWorkflowService` / `FinoteService` phát sự kiện -> `AuditDomainEventHandler` tiếp nhận -> Thực hiện ghi log thay đổi trạng thái (Delta Logging - so sánh `before`/`after`) vào bảng `audit_logs`. Chi tiết xem tại `[[hb-delta-logging]]`.

## 2. Tái cấu trúc Bootstrap & Quyền động (RBAC)
Loại bỏ mock data trong `BootstrapService` bằng cơ chế dữ liệu thời gian thực:
- **Quyền UI**: Tích hợp `PermissionService` truy vấn động quyền hạn của user từ Database/Redis.
- **Hiệu suất (Staff Performance)**: Bổ sung phương thức tính toán tổng hợp trong `ILeadRepository` và `IFinoteRepository` để thống kê hiệu suất thực tế và tỷ lệ chuyển đổi (conversion rate) của nhân sự.

## 3. Đồng bộ hóa Domain & Kiến trúc sạch (Clean Architecture)
- **Domain Exceptions**: Định nghĩa `EntityNotFoundException` và `BusinessRuleValidationException` tại tầng Domain, cô lập lỗi nghiệp vụ khỏi Framework (NestJS).
- **Chuẩn hóa Schema**: Đổi tên trường từ `estimatedValue` thành `expectedValue` đồng bộ từ Domain Entity, `LeadQueryService`, đến `LeadResponseDto`.
- **Repository Interface**: Nâng cấp `IFinoteRepository` hỗ trợ tính toán aggregate phục vụ nghiệp vụ kế toán tại `[[dom-accounting-finote]]`.