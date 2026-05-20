---
title: "ADR-008: Event-Driven Audit Orchestration"
status: accepted
date: 2026-05-04
tags: [architecture, event-driven, audit]
---

# ADR-008: Event-Driven Audit Orchestration

## Bối cảnh
Cần tách biệt logic nghiệp vụ khỏi logic ghi log để giữ cho Service thuần khiết.

## Quyết định
Mọi thay đổi trạng thái trọng yếu phải phát hành Domain Event (`IAuditableEvent`) và được xử lý bởi `AuditDomainEventHandler`.

## Lý do
Tuân thủ nguyên tắc Single Responsibility. Đảm bảo không bỏ sót log khi logic nghiệp vụ mở rộng.

## Áp dụng
- Lead Status/Assign
- Finote Status/Created
