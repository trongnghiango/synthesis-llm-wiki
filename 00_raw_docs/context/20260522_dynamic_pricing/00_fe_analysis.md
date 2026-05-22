# 00 Frontend UI/UX Analysis: Biểu phí động & Doanh thu bậc thang CRM

Tài liệu phân tích UI/UX Frontend phục vụ cho việc tích hợp mô hình biểu phí lai (Fixed, Manual, Tiered Revenue) vào trang quản lý Lead (Chốt hợp đồng) và trang Catalog Dịch vụ của STAX.

## 1. Mục tiêu UI/UX
- **Đơn giản hóa biểu mẫu**: Cho phép Sales dễ dàng chuyển đổi qua lại giữa các mô hình tính phí mà không cảm thấy giao diện bị quá tải.
- **Thân thiện với di động**: Hỗ trợ responsive hoàn chỉnh cho Dialog Chốt hợp đồng (WON Lead) và Form cấu hình Catalog Dịch vụ trên mọi màn hình.
- **Hạn chế nhập liệu sai**: Tự động vô hiệu hóa/ẩn các trường không liên quan khi đổi mô hình giá (ví dụ: ẩn Đơn giá cố định khi chọn biểu phí bậc thang).
- **Rõ ràng tài chính**: Khi chọn mô hình giá động, nhãn "Tự động tạo Phiếu Thu đợt 1" sẽ tự động chuyển thành "Tạo phiếu thu cọc ban đầu", làm rõ ý đồ thu cọc trước và đối soát thực tế sau.

## 2. Phân tích Flow màn hình & Linh kiện
Hệ thống sẽ thay đổi tại 2 phân khu chính:

### A. Catalog Dịch vụ (CRM -> Services)
- **Component**: `frontend/client/src/pages/admin/crm/services.tsx`
- **Mục tiêu**: Cho phép Admin cấu hình trước mô hình giá mẫu cho dịch vụ trong Catalog.
- **Data Flow**:
  1. Khi thêm/sửa dịch vụ, Admin chọn mô hình giá: `Cố định (FIXED)`, `Thỏa thuận tay (MANUAL_AGREEMENT)`, `Bậc thang doanh thu (TIERED_REVENUE)`.
  2. Nếu chọn `FIXED`, hiển thị ô nhập `Giá cơ sở (basePrice)`.
  3. Nếu chọn `TIERED_REVENUE`, hiển thị danh sách các mốc bậc thang (Array Fields: doanh thu tối thiểu, doanh thu tối đa, số tiền phí). Ô nhập `basePrice` bị ẩn.
  4. Nếu chọn `MANUAL_AGREEMENT`, ô nhập `basePrice` bị ẩn.

### B. Dialog Chốt Hợp Đồng (CRM -> Leads -> WON Dialog)
- **Component**: `frontend/client/src/pages/admin/crm/leads.tsx` (hoặc `lead-detail.tsx`)
- **Mục tiêu**: Sales chốt WON Lead, kế thừa cấu hình từ dịch vụ hoặc ghi đè linh hoạt cho hợp đồng.
- **Data Flow**:
  1. Khi chốt WON Lead, hiển thị Dialog chốt hợp đồng.
  2. Dialog tự động tải `pricingModel` và `pricingConfig` từ dịch vụ mẫu được liên kết với Lead.
  3. Cho phép Sales thay đổi trực tiếp mô hình giá và chỉnh sửa các mốc bậc thang trước khi gửi yêu cầu lên API `POST /api/crm/leads/:id/won`.
  4. Phần tạo Phiếu thu ban đầu:
     - Nếu mô hình giá là `FIXED`: Phí thu mặc định bằng Giá trị hợp đồng (`feeAmount`).
     - Nếu mô hình giá động (`MANUAL_AGREEMENT`, `TIERED_REVENUE`): Cho phép nhập số tiền cọc tùy ý vào ô `Số tiền thu cọc ban đầu` (`finoteAmount`).

---

## 3. Server-Driven UI & Quyền truy cập
- Sử dụng thuộc tính `_actions` từ API Lead: chỉ hiển thị tính năng chốt hợp đồng nếu có quyền `lead:edit` và trạng thái Lead cho phép.
- Cấu hình Catalog Dịch vụ yêu cầu quyền `service:edit` hoặc quyền Admin.

---
Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc FE.
