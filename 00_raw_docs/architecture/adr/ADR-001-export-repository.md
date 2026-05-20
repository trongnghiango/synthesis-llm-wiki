---
title: "ADR-001: Export Repository trực tiếp từ CRM Module"
status: accepted
date: 2026-04-25
tags: [architecture, repository, crm]
---

# ADR-001: Export Repository trực tiếp từ CRM Module

## Bối cảnh
Bảng `Organizations` và `Contacts` là "Cột sống" dữ liệu chung, được sử dụng bởi hầu hết các module khác như Accounting, HRM, Contracts.

## Quyết định
Export `IOrganizationRepository` và `IContactRepository` trực tiếp từ CRM Module để các module khác có thể sử dụng.

## Lý do
Các module Kế toán, HRM cần truy cập trực tiếp thông tin định danh khách hàng mà không cần qua tầng Service trung gian của CRM, giúp giảm bớt boilerplate và tăng hiệu năng.
