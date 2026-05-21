---
id: dom-finote-payment
title: Tích hợp nghiệp vụ Ghi nhận thanh toán Finote
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Thiết kế component và API tích hợp ghi nhận thanh toán Finote (Partial/Full) sử dụng Server-Driven UI và Shared Contract Zod."
tags: [accounting, finote, payment, react-hook-form, server-driven-ui, zod]
---

## 1. Cơ chế Server-Driven UI (SDUI) & Phân quyền
- Hiển thị nút "Ghi nhận thanh toán" tại `FinoteDetailPage` và Action Menu của `FinotesPage` dựa hoàn toàn vào flag `finote._actions.recordPayment?.allowed` từ Backend.
- Đảm bảo tính nhất quán cho State Machine từ Server, Frontend không tự quyết định logic ẩn/hiện nút.

## 2. API Contract & Type Safety
- **Shared Schema**: Sử dụng trực tiếp `RecordFinotePaymentSchema` từ backend shared contracts.
- **Type Inference**: Infer kiểu dữ liệu `RecordFinotePaymentInput` từ Zod Schema trên FE để đảm bảo an toàn kiểu dữ liệu (TypeScript compile pass 100%).
- **API Endpoint**: Tích hợp thông qua `accountingApi.recordFinotePayment(data)`.

## 3. UI/UX & Quản lý State
- **Component**: Thiết lập `RecordPaymentDialog` (Modal) bằng `react-hook-form` + `zodResolver`.
- **Ràng buộc dữ liệu**:
  - Giá trị mặc định cho ô số tiền: `remainingAmount` (Tổng tiền - Đã thanh toán).
  - Giới hạn Input: `max={remainingAmount}` để ngăn ngừa nhập quá số tiền cần thanh toán.
- **Đồng bộ hóa dữ liệu**: Gọi `queryClient.invalidateQueries` ngay sau khi thanh toán thành công để cập nhật tức thì trạng thái UI sang `PARTIALLY_PAID` hoặc `PAID`.
- **Hiển thị**: Lịch sử thanh toán (`finote.payments`) hiển thị song song với Audit Log, định dạng tiền tệ VND.