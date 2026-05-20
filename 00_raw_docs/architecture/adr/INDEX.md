---
folder: architecture/adr
description: "Architecture Decision Records — Hồ sơ các quyết định kiến trúc quan trọng của STAX"
tags: [architecture, adr, decisions]
last_updated: "2026-05-10"
---

# 📂 Architecture Decision Records (ADR)

> Các quyết định kiến trúc là "linh hồn" của hệ thống. ADR giúp ghi lại bối cảnh, quyết định và lý do tại sao một giải pháp được chọn thay vì giải pháp khác.

## Danh sách ADR

| ID | Tiêu đề | Tags | Tóm tắt |
|---|---|---|---|
| [ADR-001](./ADR-001-export-repository.md) | Export Repo trực tiếp từ CRM | `#repository` `#crm` | Cho phép Accounting/HRM truy cập trực tiếp Organizations. |
| [ADR-002](./ADR-002-strict-enum.md) | Triển khai Strict Enum | `#db` `#type-safety` | Thay thế text bằng pgEnum để gia cố dữ liệu. |
| [ADR-003](./ADR-003-hybrid-storage.md) | Hybrid Storage (JSONB) | `#jsonb` `#legacy` | Lưu dữ liệu legacy không chuẩn vào cột metadata. |
| [ADR-004](./ADR-004-centralized-audit-log.md) | Audit Log Tập trung | `#audit` `#tier-1` | Xây dựng foundation logging tại Tier 1. |
| [ADR-005](./ADR-005-fire-and-forget-logging.md) | Fire-and-forget Logging | `#performance` | Log không được làm lỗi nghiệp vụ chính. |
| [ADR-006](./ADR-006-delta-logging.md) | Delta Logging (Diff) | `#optimization` | Chỉ lưu các trường thay đổi để tiết kiệm storage. |
| [ADR-007](./ADR-007-rich-domain-model.md) | Rich Domain Model | `#ddd` `#encapsulation` | Đưa logic vào Entity, ẩn các trường trạng thái. |
| [ADR-008](./ADR-008-event-driven-audit.md) | Event-Driven Audit | `#event` `#audit` | Ghi log thông qua lắng nghe Domain Events. |
| [ADR-009](./ADR-009-bootstrap-intelligence.md) | Decoupled Bootstrap | `#frontend` `#bootstrap` | Cung cấp UI context trực tiếp từ server. |
| [ADR-010](./ADR-010-domain-exceptions.md) | Strict Domain Exceptions | `#clean-arch` `#errors` | Cấm dùng Framework Exceptions trong Domain/App layers. |
| [ADR-011](./ADR-011-registry-pattern-for-decoupling.md) | Giải quyết Circular Dependency bằng Registry Pattern | `#clean-arch` `#decoupling` | Áp dụng Registry Pattern để bẻ gãy vòng lặp phụ thuộc giữa các Tier. |
