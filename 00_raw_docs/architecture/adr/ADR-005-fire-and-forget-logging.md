---
title: "ADR-005: Fire-and-forget Logging Pattern"
status: accepted
date: 2026-04-26
tags: [architecture, logging, performance]
---

# ADR-005: Fire-and-forget Logging Pattern

## Bối cảnh
Việc ghi log không nên làm gián đoạn hoặc làm chậm các giao dịch nghiệp vụ chính.

## Quyết định
Sử dụng mô hình try-catch bao bọc lệnh ghi log. Nếu DB ghi log gặp lỗi, hệ thống vẫn phải cho phép hoàn tất giao dịch chính.

## Lý do
Audit Log là hệ thống hỗ trợ, không phải là ràng buộc cứng (Hard Constraint) đối với nghiệp vụ.
