# Walkthrough: Finote Detail Page

## 1. Kết quả đạt được
Đã triển khai thành công trang Chi tiết Phiếu Thu/Chi (`finote-detail`) với đầy đủ tính năng hiển thị và tương tác quản trị.

## 2. Các điểm nổi bật về Kỹ thuật
- **Routing**: Sử dụng TanStack Router với Type-safe params (`/admin/accounting/finotes/$id`).
- **UI Design**: 
  - **Bento Grid**: Bố trí thông tin khoa học, tách biệt giữa thông tin tài chính và đối tượng liên quan.
  - **Glassmorphism**: Áp dụng hiệu ứng backdrop-blur và gradient tinh tế, tạo cảm giác cao cấp.
  - **Framer Motion**: Thêm hiệu ứng xuất hiện mượt mà cho các card thông tin.
- **PDF Preview**: 
  - Tích hợp trình xem PDF trực tiếp qua `iframe`.
  - Hỗ trợ xem nhanh (Thumbnail) và xem chi tiết (Fullscreen Dialog).
  - Tự động nhận diện `pdfUrl` và nối chuỗi với Backend Base URL.
- **Server-Driven Logic**:
  - Hệ thống nút bấm (Duyệt/Từ chối) được điều khiển hoàn toàn bởi cờ `_actions` từ API.
  - Xử lý trạng thái loading bằng Skeleton UI đồng bộ với layout chính.

## 3. Các file đã can thiệp
- `client/src/modules/accounting/api/accounting.api.ts`: Bổ sung method `getFinoteById`.
- `client/src/app/router/routes/accounting-routes.tsx`: Đăng ký route mới.
- `client/src/app/router/index.tsx`: Cập nhật cây route hệ thống.
- `client/src/pages/admin/accounting/finotes.tsx`: Liên kết trang danh sách với trang chi tiết qua TanStack Link.
- `client/src/pages/admin/accounting/finote-detail.tsx`: **[NEW]** File component chính của trang chi tiết.

## 4. Kiểm tra (Verification)
- [x] Click "Chi tiết" từ danh sách -> Chuyển trang đúng ID.
- [x] Hiển thị đúng số tiền theo định dạng tiền tệ Việt Nam.
- [x] Nút "Phê duyệt" hoạt động và tự động cập nhật trạng thái UI sau khi thành công.
- [x] Responsive: Đã kiểm tra hiển thị tốt trên iPhone và iPad.

---
👉 **Hoàn tất nhiệm vụ.** Tính năng đã sẵn sàng để vận hành.
