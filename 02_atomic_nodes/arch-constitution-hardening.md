---
id: arch-constitution-hardening
title: Tăng cường Tuân thủ Hiến pháp Hệ thống STAX
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-delta-logging]]"
  - "[[dom-accounting-finote]]"
summary: "Chuẩn hóa kiến trúc STAX thông qua Event-Driven Auditing, dynamic Bootstrap permissions và thuần hóa Domain Exceptions."
tags: [architecture, auditing, event-driven, security, domain-purity]
---

### 1. Kiến trúc Event-Driven Auditing
*   **Cơ chế:** Phân rã (decouple) nghiệp vụ ghi log bằng cách phát hành Event từ `LeadWorkflowService` và `FinoteService` thay vì gọi trực tiếp service Audit.
*   **Domain Events mới:** `LeadStatusChangedEvent`, `LeadAssignedEvent`, `FinoteStatusChangedEvent`.
*   **Xử lý:** `AuditDomainEventHandler` tiêu thụ event và thực hiện [[hb-delta-logging]] (lưu trữ diff trước/sau thay đổi - `before`/`after`) vào bảng `audit_logs`.

### 2. Dynamic Bootstrap & UI Intelligence
*   **API Endpoint:** `GET /system/bootstrap`
*   **Quyền hạn thực tế:** Sử dụng `PermissionService` để tính toán quyền UI động của người dùng dựa trên Roles/Permissions từ DB/Redis thay vì dữ liệu tĩnh (mock).
*   **Báo cáo hiệu năng:** Phương thức `getTeamSummary` truy vấn thời gian thực hiệu suất nhân sự (Staff Performance) và tỷ lệ chuyển đổi (conversion rate) từ DB.

### 3. Tách biệt Nghiệp vụ & Đồng nhất Dữ liệu (Domain Purity)
*   **Domain Exceptions:** Triển khai các ngoại lệ thuần túy (`EntityNotFoundException`, `BusinessRuleValidationException`) để cô lập tầng nghiệp vụ khỏi NestJS Framework.
*   **Đồng nhất Schema/DTO:** Đồng bộ thuộc tính `estimatedValue` thành `expectedValue` trên `LeadResponseDto`, `LeadQueryService` để khớp hoàn toàn với Domain Entity.
*   **Repository Interface:** Bổ sung các phương thức tính toán tổng hợp (aggregate calculations) vào `ILeadRepository` và `IFinoteRepository` thuộc tầng Domain.