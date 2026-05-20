---
title: "ADR-010: Architecture Purity & Strict Domain Exceptions"
status: accepted
date: 2026-05-04
tags: [architecture, clean-arch, exceptions]
---

# ADR-010: Architecture Purity & Strict Domain Exceptions

## Bối cảnh
Sử dụng Exception của Framework (NestJS) trong Domain Layer vi phạm nguyên tắc độc lập của Clean Architecture.

## Quyết định
Cấm dùng NestJS exceptions (NotFoundException, etc.) trong Application và Domain layer. Sử dụng Domain Exceptions riêng.

## Lý do
Bảo vệ Core Logic khỏi sự phụ thuộc vào Framework (Framework Agnostic) và ngăn rò rỉ khái niệm HTTP vào nghiệp vụ.
