---
title: "ADR-009: Decoupled Bootstrap Intelligence"
status: accepted
date: 2026-05-04
tags: [architecture, frontend, bootstrap]
---

# ADR-009: Decoupled Bootstrap Intelligence

## Bối cảnh
Frontend cần thông tin về quyền hạn và ngữ cảnh ngay khi khởi động app mà không nên dựa vào mock data.

## Quyết định
`BootstrapService` tính toán App Context (quyền UI, báo cáo nhanh) trực tiếp từ Permission Service và Repository.

## Lý do
Đảm bảo Frontend luôn có dữ liệu chính xác và tuân thủ nguyên tắc Server-Driven UI.
