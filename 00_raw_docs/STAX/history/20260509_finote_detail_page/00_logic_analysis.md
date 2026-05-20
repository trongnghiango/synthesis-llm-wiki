# Logic Analysis: Finote Detail Page

## 1. Quy mô (Scope)
Đây là một **Page** mới trong module `Accounting`, dùng để hiển thị chi tiết một Phiếu Thu/Chi (Finote) và thực hiện các thao tác quản trị liên quan.

## 2. Data & Contracts
### API Endpoints
- **GET** `/accounting/finotes/:id`: Lấy chi tiết phiếu (Backend đã cung cấp).
- **POST** `/accounting/finotes/:id/approve`: Phê duyệt phiếu.
- **POST** `/accounting/finotes/:id/reject`: Từ chối phiếu kèm lý do.

### Các API hiện có:
- **POST** `/accounting/finotes/:id/approve`: Phê duyệt phiếu.
- **POST** `/accounting/finotes/:id/reject`: Từ chối phiếu kèm lý do.

## 3. Server-Driven UI (Matrix Hành động)
Trang chi tiết sẽ phụ thuộc hoàn toàn vào metadata `_actions` từ API trả về:
- **Nút "Duyệt"**: Hiển thị nếu `_actions.approve.allowed === true`.
- **Nút "Từ chối"**: Hiển thị nếu `_actions.reject.allowed === true`.
- **Nút "Sửa"**: Hiển thị nếu `_actions.edit.allowed === true`.
- **Thông báo lý do**: Nếu hành động bị chặn, hiển thị tooltip hoặc alert dựa trên `_actions.[action].reason`.

## 4. Routing & Layout
- **URL**: `/admin/accounting/finotes/:id`
- **Layout**: `AdminLayout`.
- **Guard**: Cần quyền `finote:read` (đã được cấu hình ở route level).

## 5. UI/UX Highlights
- **Glassmorphism**: Sử dụng backdrop blur cho các card thông tin.
- **Bento Grid**: Bố trí thông tin chính (Số tiền, Trạng thái) theo dạng lưới hiện đại.
- **PDF Preview**: Tích hợp trình xem PDF ngay trên giao diện để người dùng kiểm tra chứng từ gốc mà không cần chuyển tab.
- **Timeline**: Hiển thị lịch sử thay đổi trạng thái (Audit Log).
- **Responsive**: Tối ưu hiển thị trên mobile.

## 6. PDF Integration Logic
- **Nguồn dữ liệu**: Trường `pdfUrl` từ `FinoteResponseDto`.
- **Cơ chế hiển thị**: 
  - Ưu tiên hiển thị một "Thumbnail" hoặc "Preview Card" ở sidebar.
  - Khi click sẽ mở một **Large Dialog** (Modal) chứa iframe hiển thị PDF.
  - Cần xử lý trường hợp `pdfUrl` bị trống (Hiển thị placeholder hoặc thông báo chưa có file).

---
👉 **Hỏi User**: "Bản phân tích logic này đã bao quát đủ yêu cầu chưa? Vui lòng báo cáo cho team Backend cung cấp endpoint `GET /accounting/finotes/:id` để tôi có thể tiếp tục."
