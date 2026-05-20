---
title: "ADR-004: Kiến trúc Audit Log Tập trung"
status: accepted
date: 2026-04-26
tags: [architecture, audit-log, foundation]
---

# ADR-004: Kiến trúc Audit Log Tập trung (Tier 1 Foundation)

## Bối cảnh
Cần một cơ chế giám sát hành động người dùng nhất quán trên toàn hệ thống.

## Quyết định
Xây dựng `AUDIT_LOG_PORT` và `DrizzleAuditLogService` tại Tier 1 (Foundation).

## Lý do
Đảm bảo tính nhất quán (Consistency) và tránh việc mỗi module tự triển khai logging theo cách riêng.

## Thiết kế
Sử dụng schema tập trung `audit_logs` với JSONB `before/after` để lưu vết thay đổi dữ liệu chi tiết.
