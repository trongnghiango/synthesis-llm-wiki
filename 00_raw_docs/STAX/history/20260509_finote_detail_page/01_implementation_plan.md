# Implementation Plan: Finote Detail Page

## A. Shared Contracts Layer
- **Type**: `FinoteDetail` kế thừa từ `FinoteResponseDto`.
- **Location**: Cập nhật types trong `@/modules/accounting/api/accounting.api.ts` (Do dự án đang dùng cấu trúc inline types cho đơn giản, hoặc check `@shared/contracts` nếu có).

## B. Infrastructure Layer (API & Router)
### 1. API Client
- **File**: `client/src/modules/accounting/api/accounting.api.ts`
- **Method**: `getFinoteById(id: number)`
- **Endpoint**: `GET /accounting/finotes/${id}`

### 2. Router Setup (TanStack Router)
- **File**: `client/src/routes/admin/accounting/finotes.$id.tsx` (Tạo mới).
- **Page Component**: `FinoteDetailPage`.

## C. Application Layer (State & Hooks)
- **React Query**: 
  - `queryKey`: `['accounting', 'finotes', id]`
  - `useQuery`: Để fetch dữ liệu chi tiết.
  - `useMutation`: Cho các action `approve`, `reject`.

## D. Presentation Layer (UI)
### Components
1. **FinoteDetailHeader**: Hiển thị Mã phiếu, Trạng thái (Badge), và các nút Action (Approve/Reject/Print).
2. **FinoteMainInfo**: Bento-style card chứa Số tiền (Money), Loại phiếu, Đối tượng, Ngày hạn.
3. **FinoteDescriptionCard**: Hiển thị nội dung diễn giải chi tiết.
4. **FinotePDFCard**: Card ở sidebar hiển thị xem trước PDF và nút "Xem toàn màn hình".
5. **PDFViewerModal**: Modal phóng to sử dụng `iframe` hoặc thư viện `react-pdf-viewer` (Nếu cần nâng cao).
6. **FinoteAuditLog**: (Optional) Hiển thị dòng thời gian phê duyệt.

### Layout & Style
- Sử dụng **Glassmorphism** (backdrop-blur, white/60) cho các container.
- **PageHeader**: Tái sử dụng để hiển thị breadcrumbs và tiêu đề lớn.
- **Skeleton**: Hiển thị trạng thái đang tải chuyên nghiệp.

---
👉 **Hỏi User**: "Bản kế hoạch triển khai này đã đúng ý bạn chưa? Nếu rồi, tôi sẽ chuyển sang lập danh sách Task chi tiết."
