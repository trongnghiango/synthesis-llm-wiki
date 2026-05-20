# Programming Tasks: Finote Detail API

- [x] **Phase 1: Infrastructure & Repository**
    - [x] Cập nhật `IFinoteRepository` bổ sung phương thức `findByIdWithAttachments(id, orgId)`
    - [x] Triển khai phương thức trong `DrizzleFinoteRepository` sử dụng SQL Left Join
- [x] **Phase 2: Application Logic**
    - [x] Cập nhật `FinoteService.getById` thực hiện Tenancy Check và Action Logic
    - [x] Viết Unit Test cho `FinoteService.getById` (`finote.service.spec.ts`)
- [x] **Phase 3: API & DTO**
    - [x] Cập nhật `FinoteResponseDto` để hỗ trợ mảng `attachments`
    - [x] Thêm endpoint `GET /accounting/finotes/:id` vào `FinoteController`
- [x] **Phase 4: Verification**
    - [x] Chạy toàn bộ test suite để đảm bảo không hồi quy (regression)
    - [x] Tạo `03_walkthrough.md` tổng kết
