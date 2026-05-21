---
id: dom-finote-payment
title: Thiết kế Luồng Ghi nhận Thanh toán Finote
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Đặc tả kỹ thuật cơ chế ghi nhận thanh toán Finote sử dụng Server-Driven UI, Shared Zod Contract và query invalidation."
tags: [accounting, finote, payment, sdui, zod, react-hook-form]
---

### 1. Cơ chế Điều khiển UI (Server-Driven UI)
- **Ẩn/Hiện Action:** Nút "Ghi nhận thanh toán" tại `FinotesPage` (List Dropdown) và `FinoteDetailPage` được quyết định bởi backend thông qua trường:
  `finote._actions.recordPayment?.allowed: boolean`
- **Luồng Trạng thái:** Sau khi thanh toán thành công, gọi `queryClient.invalidateQueries` để kích hoạt fetch lại dữ liệu tự động, chuyển trạng thái Finote sang `PARTIALLY_PAID` hoặc `PAID`.

### 2. Biểu mẫu & Validation (Form & Contract)
- **Shared Schema:** Sử dụng trực tiếp `RecordFinotePaymentSchema` từ backend contracts.
- **Type Safety:** Định nghĩa kiểu dữ liệu đồng bộ bằng Zod Inference:
  ```typescript
  type RecordFinotePaymentInput = z.infer<typeof RecordFinotePaymentSchema>;
  ```
- **Ràng buộc Client:** 
  - Giá trị mặc định của ô nhập tiền = `remainingAmount` (Tổng tiền - Đã thanh toán).
  - Giới hạn nhập tối đa: `max={remainingAmount}`.

### 3. API & Lưu trữ Dữ liệu
- **Endpoint:** `accountingApi.recordFinotePayment(data: RecordFinotePaymentInput)`
- **Cấu trúc dữ liệu mở rộng:**
  - `finote.payments`: Mảng lịch sử các lần thanh toán (hiển thị theo VND).
  - Tích hợp ghi nhận log giao dịch thông qua `[[hb-delta-logging]]`.