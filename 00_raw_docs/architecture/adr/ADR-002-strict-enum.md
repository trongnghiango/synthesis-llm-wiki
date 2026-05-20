---
title: "ADR-002: Triển khai Strict Enum"
status: accepted
date: 2026-04-26
tags: [architecture, database, type-safety]
---

# ADR-002: Triển khai Strict Enum (Gia cố kiểu dữ liệu)

## Bối cảnh
Việc sử dụng kiểu `text` cho các trường trạng thái (status) hoặc loại (type) dễ dẫn đến sai lệch dữ liệu do lỗi nhập liệu (VD: " Won" vs "won").

## Quyết định
Thay thế toàn bộ trường `text` status/type bằng `pgEnum` (Drizzle) và TypeScript Enums.

## Lý do
Đảm bảo báo cáo kinh doanh và tài chính chính xác tuyệt đối. Loại bỏ hoàn toàn các giá trị không hợp lệ tại tầng Database.

## Áp dụng
- Organization
- Lead
- Contract
- Finote
