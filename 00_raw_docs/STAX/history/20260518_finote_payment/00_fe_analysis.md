# Phân tích UI/UX: Finote Payment Integration

**Context Check:**
Dựa trên Base từ `stax-think` Decision Log, luồng UI sẽ có 2 điểm chạm dùng chung 1 Component.

**Mục tiêu UX:**
Kế toán có thể đối soát nhanh và trực quan. Tránh tối đa việc ghi nhận dư tiền bằng cách hiển thị số nợ còn lại (remainingAmount) ngay trên Form.

**Data Flow:**
1. Lấy dữ liệu: Dùng `useFinote` (React Query) để lấy data hiện tại.
2. Nút "Ghi nhận thanh toán" xuất hiện dựa vào `_actions.recordPayment.allowed`.
3. Submit Form -> `RecordPaymentDialog` -> React Query Mutation -> Invalidate `finotes` query.

**Server-Driven UI:**
Không hardcode `if (status === 'PAID')` trên Frontend. Luôn tuân thủ `_actions` từ API trả về.
