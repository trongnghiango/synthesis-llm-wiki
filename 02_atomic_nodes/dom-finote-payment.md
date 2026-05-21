---
id: dom-finote-payment
title: Nghiệp vụ Ghi nhận Thanh toán Finote
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Thiết kế UI/UX và API Contract cho tính năng ghi nhận thanh toán từng phần/toàn phần (Partial/Full Payment) của Finote."
tags: [finote, payment, accounting, sdui, react-hook-form]
---

### 1. Kiến trúc Server-Driven UI & Phân quyền
- **Quyết định trạng thái**: Hiển thị nút "Ghi nhận thanh toán" (ở danh sách `FinotesPage` và chi tiết `FinoteDetailPage`) được điều khiển động từ backend qua: `finote._actions.recordPayment?.allowed`.
- **Đồng bộ State**: Gọi `queryClient.invalidateQueries` sau khi thanh toán thành công để tự động cập nhật trạng thái UI sang `PARTIALLY_PAID` hoặc `PAID`.

### 2. Thiết kế Form & UX
- **Component**: `RecordPaymentDialog` tích hợp `react-hook-form` và `zodResolver`.
- **Logic tiền tệ**: Tự động điền số tiền thanh toán mặc định bằng `remainingAmount` (Tổng - Đã thanh toán). Giới hạn validation `max={remainingAmount}` trực tiếp tại Input.
- **Lịch sử thanh toán**: Hiển thị danh sách `finote.payments` (định dạng VND) song song với mục Audit Log tại chi tiết Finote.

### 3. API Contract & Type Safety
- **Shared Contract**: Sử dụng `RecordFinotePaymentInput` được infer từ `RecordFinotePaymentSchema` (Zod) từ shared contract giúp đồng bộ Type-safety 100% FE-BE.
- **API Call**: `accountingApi.recordFinotePayment` chịu trách nhiệm gửi payload lên Gateway.