# Task Checklist: Org Structure Recursion & Aggregation

- [ ] **Backend Development**
    - [ ] Cập nhật DTO để nhận tham số `includeDescendants: boolean`.
    - [ ] Cập nhật Repository logic cho `Position` (Sử dụng LIKE path%).
    - [ ] Cập nhật Repository logic cho `Employee` (Sử dụng LIKE path%).
- [x] **Frontend Infrastructure**
    - [x] Cập nhật `hrm.api.ts` để hỗ trợ tham số mới.
- [x] **Frontend UI/UX**
    - [x] Cập nhật `OrgNode` hiển thị song song Direct/Total Headcount (Đã sẵn sàng chờ dữ liệu tổng hợp từ Tree API).
    - [x] Bổ sung bộ lọc "Tổng hợp dữ liệu" trong Side Panel của Đơn vị.
    - [ ] Tối ưu hóa hiệu năng bằng cách cache kết quả truy vấn đệ quy.
- [ ] **Verification**
    - [ ] Kiểm tra tính chính xác của số liệu tổng hợp tại nút Gốc (Công ty).
    - [ ] Đảm bảo không có hiện tượng trùng lặp (Double counting).
