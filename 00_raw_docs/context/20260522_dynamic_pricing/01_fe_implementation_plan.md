# 01 Frontend Implementation Plan: Biểu phí động & Doanh thu bậc thang CRM

Kế hoạch triển khai kỹ thuật phần Frontend cho biểu phí linh hoạt trên STAX.

## A. Contract Sync (Đồng bộ Shared Contracts)
Chúng ta cần đồng bộ các schemas và interfaces từ backend sang frontend tại `frontend/shared/contracts/crm.ts`:
- **`closeWonSchema`**:
  - Thêm `pricingModel: z.enum(["FIXED", "MANUAL_AGREEMENT", "TIERED_REVENUE"]).default("FIXED")`.
  - Thêm `pricingConfig: z.any().optional().nullable()`.
  - Chuyển `feeAmount` thành optional (vì chỉ bắt buộc với FIXED).
- **`ContractItem`**:
  - Chuyển `unitPrice` và `amount` thành `number | null`.
  - Thêm `pricingModel?: 'FIXED' | 'MANUAL_AGREEMENT' | 'TIERED_REVENUE'`.
  - Thêm `pricingConfig?: any`.

## B. API Client & Types
1. **Dịch vụ Catalog**:
   - Cập nhật `frontend/client/src/modules/crm/types/service.types.ts`:
     - Thêm `pricingModel` và `pricingConfig` vào `ServiceSchema` và `CreateServiceSchema`.
     - Cho phép `basePrice` là `nullable`.
   - Các API hooks (`useServices`, `useCreateService`, `useUpdateService` tại `frontend/client/src/modules/crm/api/service.api.ts`) không cần thay đổi vì chúng đã truyền nhận payload dạng json generic.

2. **Won Lead Flow**:
   - API Client `crmApi.closeWon` tại `frontend/client/src/modules/crm/api/crm.api.ts` cần nhận thêm `pricingModel` và `pricingConfig`.
   - Cập nhật `closeWon` payload tại `crm.api.ts` để truyền đầy đủ dữ liệu mới xuống Backend:
     ```typescript
     closeWon: (id: number, data: any) => request.post(`/crm/leads/${id}/won`, data)
     ```
     (Hiện tại đã là `crmData` generic).

## C. Component Tree & UI Changes

### 1. Service Catalog Form (`services.tsx`)
- Thêm phần chọn `Mô hình tính giá` (`pricingModel`) với 3 options: `Cố định`, `Thỏa thuận tay`, `Bậc thang doanh thu`.
- Tạo một Dynamic Form Section:
  - Nếu `pricingModel === "FIXED"`: Hiển thị trường `Đơn giá gốc` (`basePrice`).
  - Nếu `pricingModel === "MANUAL_AGREEMENT"`: Ẩn trường đơn giá gốc.
  - Nếu `pricingModel === "TIERED_REVENUE"`: Hiển thị giao diện quản lý danh sách bậc thang doanh thu (bao gồm Thêm/Xóa mốc bậc thang, mỗi mốc có: `Doanh thu tối thiểu`, `Doanh thu tối đa`, `Số tiền phí`).

### 2. Dialog Chốt Hợp Đồng (`leads.tsx` & `lead-detail.tsx`)
- Khi người dùng bấm chốt WON:
  - Lấy thông tin Dịch vụ được liên kết với Lead (nếu có).
  - Tự động đặt mặc định `pricingModel` và `pricingConfig` theo cấu hình của Dịch vụ.
  - Hiển thị phần chọn Mô hình tính giá và cho phép tùy biến trực tiếp cấu hình biểu phí của hợp đồng.
  - Nếu chọn mô hình giá động (`MANUAL_AGREEMENT` hoặc `TIERED_REVENUE`):
    - Đặt `feeAmount` về 0 / ẩn trường nhập Giá trị hợp đồng.
    - Hiển thị ô `Số tiền thu cọc ban đầu` (`finoteAmount`) và tự động bật Checkbox tạo Phiếu thu.
    - Đổi nhãn nút tạo phiếu thu thành "Tạo phiếu thu cọc ban đầu".

## D. State Management
- Quản lý trạng thái Form thông qua `react-hook-form` tích hợp `zodResolver(closeWonSchema)`.
- Sử dụng `useFieldArray` của `react-hook-form` để quản lý danh sách bậc doanh thu động một cách tối ưu, tránh re-render toàn bộ Dialog.

---
Thiết kế này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
