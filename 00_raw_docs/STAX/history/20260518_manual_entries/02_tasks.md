# Kế hoạch Triển khai Chi tiết (Task List)

## 📋 Danh sách công việc thực hiện

- [x] **Bước 1: Phân tích & Tái cấu trúc ý tưởng**
    - [x] Khảo sát các API endpoint `POST /accounting/finotes` và `POST /accounting/journal-entries` ở Backend.
    - [x] Khảo sát các Zod contract trong shared folder để đảm bảo type-safe tuyệt đối.

- [x] **Bước 2: Xây dựng Component & Tích hợp Finotes**
    - [x] Viết component `CreateFinoteDialog.tsx` hỗ trợ tạo mới phiếu thu/chi thủ công.
    - [x] Thay thế các nút tĩnh "Lập phiếu thu", "Lập phiếu chi" bằng `CreateFinoteDialog` trong `finotes.tsx`.
    - [x] Cấu hình mutation, toast thông báo và làm mới query cache khi thêm thành công.

- [x] **Bước 3: Tích hợp Lập Bút toán Nhật ký chung**
    - [x] Bọc nút "Thêm Bút toán mới" trong Dialog trên trang `journal-entries.tsx`.
    - [x] Gọi `JournalEntryForm` làm form chính để Kế toán tự chọn tài khoản định khoản.
    - [x] Tích hợp mutation gọi tới `accountingApi.createJournalEntry`.
    - [x] Đảm bảo làm mới cache `journalEntries` sau khi tạo thành công.

- [x] **Bước 4: Kiểm thử & Đóng gói Tài liệu**
    - [x] Viết cẩm nang kiểm thử thủ công trực quan.
    - [x] Thiết lập hệ thống tài liệu hồi tố lưu trữ đúng thư mục lịch sử theo chuẩn STAX.
