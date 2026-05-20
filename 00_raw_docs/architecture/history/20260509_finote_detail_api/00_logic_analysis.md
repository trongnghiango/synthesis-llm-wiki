# Logic Analysis: Finote Detail API (GET /accounting/finotes/:id)

## 1. Mục đích
- **Vấn đề:** Hiện tại Backend thiếu API để lấy thông tin chi tiết của một phiếu Thu/Chi cụ thể, khiến Frontend không thể xây dựng trang Detail.
- **Giải quyết:** Bổ sung endpoint `GET /api/accounting/finotes/:id` trả về đầy đủ thông tin của Finote, bao gồm cả danh sách đính kèm (Attachments) và các hành động khả thi (`_actions`).
- **Tier:** Tier 2 (Core Business Feature).

## 2. Yêu cầu phi chức năng (NFR) & Bảo mật
- **Tenant Isolation (QUAN TRỌNG):** Tuân thủ Hiến pháp STAX Điều 1.2. Hệ thống BẮT BUỘC phải kiểm tra quyền sở hữu: Người dùng chỉ được xem Finote thuộc về `organizationId` của mình.
- **Server-Driven UI:** Response phải bao gồm trường `_actions` (mảng các chuỗi hành động như `['approve', 'reject', 'pay']`) dựa trên trạng thái hiện tại của Finote và quyền (Permissions) của người dùng.
- **Hiệu năng:** Query cần join với bảng `attachments` và `users` (người yêu cầu) một cách tối ưu.

## 3. Tác động (Impact Analysis)
- **Database:** Không thay đổi Schema. Chỉ thực hiện các câu query SELECT + JOIN.
- **Module:** Accounting (FinoteService, FinoteController).
- **DTO:** Cập nhật `FinoteResponseDto` để hỗ trợ hiển thị chi tiết đầy đủ hơn nếu cần.

## 4. Open Questions
> [!IMPORTANT]
> 1. Bạn muốn danh sách đính kèm (Attachments) trả về trực tiếp trong API Detail này hay gọi một API riêng? (STAX khuyến nghị trả về trực tiếp để giảm số lượng request cho trang Detail).
> 2. Các hành động trong `_actions` có cần phân quyền chi tiết đến mức: "Chỉ Manager mới thấy nút Approve, còn Staff chỉ thấy nút View" không?
