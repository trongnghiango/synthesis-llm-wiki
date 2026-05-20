---
title: "ADR-003: Hybrid Storage Pattern"
status: accepted
date: 2026-04-26
tags: [architecture, database, legacy, jsonb]
---

# ADR-003: Hybrid Storage Pattern (JSONB cho dữ liệu legacy)

## Bối cảnh
Dữ liệu legacy từ CSV/Excel chứa nhiều trường thông tin không chuẩn hóa nhưng cần được lưu giữ để tham khảo.

## Quyết định
Thêm cột `metadata JSONB` vào các bảng `organizations`, `contacts`, `leads`, `contracts`.

## Lý do
Tránh làm phình schema quan hệ với các trường không quan trọng. JSONB cho phép lưu trữ 100% dữ liệu lịch sử mà không vi phạm Single Responsibility của các cột chính.

## Áp dụng
- Organizations
- Contacts
- Leads
- Contracts
