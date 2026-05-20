---
title: "ADR-007: Rich Domain Model & Field Encapsulation"
status: accepted
date: 2026-04-30
tags: [architecture, ddd, domain-model]
---

# ADR-007: Rich Domain Model & Field Encapsulation

## Bối cảnh
Anemic Domain Model khiến logic nghiệp vụ bị rò rỉ ra tầng Service, gây khó khăn cho việc bảo trì các ràng buộc (invariants).

## Quyết định
Chuyển đổi các thực thể trọng yếu (VD: Finote) sang Rich Domain Model. Các thuộc tính trạng thái được chuyển sang `private`.

## Lý do
Đảm bảo tính toàn vẹn dữ liệu. Mọi thay đổi trạng thái phải thông qua các phương thức nghiệp vụ để kiểm tra ràng buộc.

## Áp dụng
- Finote Entity (30/04/2026)
- Các thực thể Core khác dần dần.
