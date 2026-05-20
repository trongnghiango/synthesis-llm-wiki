---
id: std-import-boundaries
title: Quy tắc ranh giới Import (Import Boundaries)
layer: 3-atomic
parent: "[[02_standards_governance]]"
depends_on:
  - "[[arch-modular-monolith-tiers]]"
summary: "Quy tắc kiểm soát ranh giới import giữa các module, cấm import sâu để duy trì cấu trúc Modular Monolith lỏng lẻo."
tags: [standards, import-boundaries, dependencies, modularity]
---

# Quy tắc ranh giới Import (Import Boundaries)

Để duy trì cấu trúc Modular Monolith sạch sẽ và cho phép bóc tách thành Microservices bất cứ lúc nào, STAX thực thi ranh giới import nghiêm ngặt giữa các module nghiệp vụ:

## 1. Cấm Import Sâu (No Deep Imports)
*   Tuyệt đối **cấm** một module import trực tiếp vào các chi tiết cấu trúc nội bộ (internals) của module khác.
    *   *Sai:* `import { Employee } from '../../hrm/domain/entities/employee.entity'`
    *   *Đúng:* `import { Employee } from '@modules/hrm'`

## 2. Cổng Công khai (Public API Gateway)
*   Mỗi module bắt buộc phải có một tệp tin `index.ts` đặt tại thư mục gốc của module đó.
*   Tệp `index.ts` đóng vai trò là **Public API Gateway**. Chỉ những gì được export tại tệp này mới được phép cho các module bên ngoài import sử dụng.
*   Bảo vệ ranh giới này giúp che giấu chi tiết hạ tầng bên trong của module, tạo tính độc lập (Capsulation).

## 3. Giới hạn của thư mục `shared/`
*   Thư mục `shared/` (ví dụ `shared/contracts`) chỉ được phép chứa các kiểu dữ liệu thô, validator thô (Zod schema) và primitives dùng chung kỹ thuật.
*   Cấm tuyệt đối việc đặt các Business Logic nặng hoặc các dịch vụ nghiệp vụ vào `shared/`.
