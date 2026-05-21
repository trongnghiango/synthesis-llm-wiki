---
id: arch-shared_contracts_refactor
title: Tái cấu trúc Hợp đồng Dữ liệu Chung
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Phân rã shared/schema.ts thành các domain contracts riêng biệt truy cập qua alias @shared nhằm giảm coupling hệ thống."
tags: [refactor, shared-contracts, architecture, domain-driven]
---

## 1. Bối cảnh & Mục tiêu
Loại bỏ file monolith `shared/schema.ts` gây coupling toàn hệ thống. Thực hiện phân rã thành các hợp đồng dữ liệu (data contracts) độc lập, giúp Frontend và Backend (Python/Microservices) dễ dàng tham chiếu chéo mà không tải thừa dependency.

## 2. Thay đổi Kiến trúc & Cấu trúc Thư mục
- **Domain Contracts:** Tách thành 5 files domain chuyên biệt tại thư mục `shared/contracts/` (tương thích cấu trúc `[[hb-drizzle-base-repo]]`).
- **Entrypoint:** `shared/index.ts` đóng vai trò Barrel Export duy nhất.
- **TS Path Alias:** Cấu hình `@shared` trỏ trực tiếp đến `shared/index.ts`.

```typescript
// Cú pháp import mới sau refactor
import { UserContract, OrderContract } from "@shared";
```

## 3. Tác động kỹ thuật
- **Tối ưu hóa Dependency:** Cho phép các module độc lập hoặc dịch vụ Backend (Python) tiêu thụ từng phần nhỏ của schema/hợp đồng mà không cần kéo theo toàn bộ schema hệ thống.
- **Build Performance:** Giảm kích thước bundle biên dịch và tăng tốc thời gian phân tích cú pháp TypeScript của IDE/Compiler.
- **Kiểm định:** Đã xác thực hoàn tất qua lệnh `npm run check`.