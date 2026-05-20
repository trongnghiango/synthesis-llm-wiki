## 1. Tóm tắt tính năng (Feature Summary)

- **RecordPaymentDialog**: Component Modal được tạo mới để xử lý nghiệp vụ ghi nhận thanh toán (Partial/Full Payment). Sử dụng `react-hook-form` và `zodResolver` với schema `RecordFinotePaymentSchema` trực tiếp từ backend shared contracts.
- **FinoteDetailPage**: Tích hợp gọi `RecordPaymentDialog` dựa trên phân quyền `_actions.recordPayment?.allowed`. Thêm section Lịch sử thanh toán bên cạnh phần Nhật ký (Audit Log) để hiển thị danh sách các lần thanh toán, tổng đã thanh toán, và số dư còn lại.
- **FinotesPage (List)**: Cập nhật Dropdown Action Menu ở từng dòng dữ liệu để cung cấp tùy chọn "Ghi nhận thanh toán" ngay tại bảng, tiết kiệm thao tác click cho kế toán viên.
- **accountingApi**: Cập nhật method `recordFinotePayment` để gọi endpoint Backend chuẩn xác.

## 2. Quyết định kiến trúc UI/UX (Architecture Decisions)

- **Server-Driven UI (SDUI)**: Nút "Thanh toán" ở cả trang Chi tiết và Danh sách đều bị ẩn/hiện điều khiển hoàn toàn bởi dữ liệu `finote._actions.recordPayment?.allowed` trả về từ Backend. Frontend không tự quyết định cứng logic ẩn hiện nút này, đảm bảo tính chặt chẽ của State Machine từ server.
- **Form Component (Bắt buộc)**: Sử dụng chặt chẽ pattern chuẩn với `Form`, `FormControl`, và Toast thông báo kết quả. Gọi `queryClient.invalidateQueries` để tự động fetch lại chi tiết hóa đơn (finote detail) và danh sách ngay sau khi thanh toán thành công, giúp cập nhật trạng thái UI sang `PARTIALLY_PAID` hoặc `PAID` mượt mà không cần F5.
- **UX Tính số tiền**: Tự động set giá trị mặc định của ô Số tiền thanh toán là `remainingAmount` (Tổng - Đã thanh toán) để User không phải tự trừ nhẩm. Giới hạn `max={remainingAmount}` ở Input.

## 3. Khó khăn & Xử lý (Troubleshooting)

- **Contract Type Inference**: Đảm bảo sử dụng `RecordFinotePaymentInput` được infer từ `RecordFinotePaymentSchema` (Zod) ở phía shared contracts, giúp cho FE đồng nhất 100% với BE và được TypeScript check an toàn, thoát khỏi lỗi type-checking.
- **API Response Structure**: API Response trả về `finote.payments` cần được map thành công và hiển thị thân thiện với định dạng tiền tệ Việt Nam.
- Build TypeScript Frontend `npm run check` **PASS (0 lỗi)** thành công sau khi hoàn tất tích hợp, xác nhận quá trình tuân thủ type rất an toàn.

## 4. Hướng phát triển (Next Steps)

- Triển khai chức năng "In phiếu thanh toán/biên lai" cho mỗi lần Partial Payment (hiện đang in toàn bộ Finote).
- Có thể thêm cơ chế hoàn tiền (Refund) từ UI nếu User nhập sai số tiền hoặc khách hàng yêu cầu trả lại khoản dư.
