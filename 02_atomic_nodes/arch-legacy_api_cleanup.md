---
id: arch-legacy_api_cleanup
title: Dọn dẹp Legacy API & Chuyển đổi sang Modular API
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on: []
summary: "Loại bỏ hoàn toàn đối tượng api dùng chung tại queryClient và chuyển đổi sang mô hình Modular API độc lập."
tags: [refactor, modular-api, query-client, tech-debt]
---

### 1. Mô Hình Chuyển Đổi (Modular API)
Thay thế đối tượng `api` tập trung (monolithic) trong `queryClient.ts` bằng các module API độc lập để giảm coupling và tối ưu khả năng mở rộng:
* **Legacy:** Khai báo chung toàn bộ API endpoints trong một đối tượng `api` duy nhất tại `queryClient.ts`.
* **Modular:** Phân rã thành các tệp API chuyên biệt theo Domain:
  - `auth.api.ts`: Xử lý các nghiệp vụ và endpoints liên quan đến xác thực.
  - `system.api.ts`: Xử lý các endpoints hệ thống và cấu hình chung.

### 2. Chi Tiết Thay Đổi Kỹ Thuật
* **Tệp chỉnh sửa chính:** `src/core/queryClient.ts` (Xóa bỏ hoàn toàn cấu trúc `api` cũ).
* **Tệp khởi tạo mới:**
  - `src/features/auth/api/auth.api.ts`
  - `src/features/system/api/system.api.ts`
* **Cập nhật Consumer:** Khắc phục và chuyển đổi import trực tiếp từ các module API mới tại 8 consumers chịu ảnh hưởng.
* **Xác thực:** Đảm bảo toàn vẹn kiểu dữ liệu (Type Safety). Kết quả `npm run check` và `npm run build` PASS.