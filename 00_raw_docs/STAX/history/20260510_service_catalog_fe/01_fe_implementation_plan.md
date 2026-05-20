# Bước 2: Kế hoạch Kỹ thuật & Contract — Frontend Service Catalog

## A. API Contract & Zod Schema
Sử dụng Zod để đảm bảo tính an toàn dữ liệu từ API.

- **Schema:** `ServiceSchema`
  - `id`: number
  - `name`: string
  - `description`: string (optional)
  - `type`: 'ONE_OFF' | 'RETAINER' | 'SUBSCRIPTION'
  - `basePrice`: number
  - `status`: 'ACTIVE' | 'INACTIVE' | 'ARCHIVED'

- **Endpoints:**
  - `GET /api/crm/services` -> `fetchServices()`
  - `POST /api/crm/services` -> `createService(data)`
  - `PATCH /api/crm/services/:id` -> `updateService(id, data)`

## B. Thành phần UI (Components)

### 1. `ServicePicker` (Smart Selector)
- **Công nghệ:** Shadcn/ui (Command + Popover).
- **UX:** 
  - Ô input tìm kiếm theo tên dịch vụ.
  - Hiển thị giá và loại hình ngay trong danh sách gợi ý.
  - Phím tắt (Hotkeys) để chọn nhanh.
- **Output:** Khi chọn, component trả về trọn bộ object `Service` để Form tự động điền các trường khác.

### 2. `ServiceTable` (Quản lý)
- Hiển thị danh sách dịch vụ phía Admin.
- Cho phép sửa giá nhanh (Inline editing) hoặc chuyển trạng thái.

## C. Điểm tích hợp (Integration Points)

### 1. `QuoteForm` (Trong Lead Detail)
- Thay thế ô nhập "Description" tự do bằng `ServicePicker`.
- Khi chọn dịch vụ: Tự động điền "Unit Price" và "Description".

### 2. `FinoteForm` (Accounting)
- Thêm field `Linked Service` (Optional) để gán chi phí cho dịch vụ.

## D. Cấu trúc thư mục dự kiến
- `src/modules/crm/types/service.types.ts` (Zod & Types)
- `src/modules/crm/api/service.api.ts` (Hooks & API calls)
- `src/modules/crm/components/ServicePicker.tsx`
- `src/pages/admin/crm/services.tsx` (Trang quản lý)

---
Kế hoạch này đã đáp ứng được tiêu chí "Zero-Learning UX" chưa? Nếu OK, tôi sẽ xuất Checklist thực thi.
