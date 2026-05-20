# Walkthrough: Finote Detail API Implementation

## 1. Tính năng đã thực hiện
- **Repository:** Bổ sung `findByIdWithAttachments` vào `DrizzleFinoteRepository` sử dụng SQL Query để lấy đầy đủ thông tin kèm danh sách đính kèm.
- **Service:** Triển khai `FinoteService.getById` với cơ chế **Tenancy Enforcement** (chỉ cho phép xem dữ liệu thuộc Org của mình) và tính toán danh sách hành động khả thi (`_actions`).
- **Controller:** Mở endpoint `GET /accounting/finotes/:id` chuẩn RESTful.
- **DTO:** Cập nhật `FinoteResponseDto` để trả về metadata cho UI (Labels, Colors, Reasons).

## 2. Kết quả kiểm thử
Đã chạy toàn bộ 8 bộ test suite của module Accounting, tất cả đều **PASS**.

### Unit Tests nổi bật (`finote.service.spec.ts`):
- ✅ `nên trả về Finote kèm _actions hợp lệ cho Manager`: Kiểm chứng logic phân quyền Manager.
- ✅ `nên văng EntityNotFoundException nếu truy cập trái phép (khác OrgId)`: Kiểm chứng bảo mật Tenancy.
- ✅ `chỉ nên cho Staff thấy nút View/Edit, không thấy nút Approve`: Kiểm chứng logic phân quyền Staff.

## 3. Các bản sửa lỗi & Tối ưu (Hotfixes)
- **Extending Shared DTO:** Mở rộng `ActionDetailDto` bổ sung `label` và `color` để hỗ trợ Metadata cho UI động.
- **Typing Fix:** Điều chỉnh `FinoteController` truy cập đúng `user.roles` thay vì `user.profileContext.roles` (do kiến trúc User entity lưu roles ở gốc).
- **Type Safety:** Đã verify bằng lệnh `npm run build`, hệ thống biên dịch thành công 100%.

## 4. Hướng dẫn Frontend
- Gọi `GET /api/accounting/finotes/:id`.
- Dữ liệu trả về sẽ có mảng `attachments` để hiển thị danh sách file.
- Sử dụng đối tượng `_actions` để render các nút bấm:
    - Nếu `_actions[actionName].allowed === true` -> Hiển thị nút.
    - Sử dụng `label` và `color` từ backend trả về để render đồng nhất (Server-Driven).
    - Nếu `allowed === false` -> Disable nút kèm thông tin `reason`.
