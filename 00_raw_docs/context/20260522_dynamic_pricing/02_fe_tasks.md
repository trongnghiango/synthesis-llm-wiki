# 02 Frontend Tasks: Biểu phí động & Doanh thu bậc thang CRM

Danh sách các tác vụ cụ thể cần triển khai trên Frontend.

## Task List

- [ ] **Task 1: Đồng bộ Shared Contracts**
  - Cập nhật [crm.ts (shared)](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/shared/contracts/crm.ts):
    - Cập nhật `closeWonSchema` hỗ trợ `pricingModel` và `pricingConfig`.
    - Cập nhật interface `ContractItem` hỗ trợ đơn giá nullable và các thuộc tính biểu phí động.

- [ ] **Task 2: Cập nhật Service Types & API**
  - Cập nhật [service.types.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/crm/types/service.types.ts):
    - Cập nhật `ServiceSchema` và `CreateServiceSchema` để thêm `pricingModel` và `pricingConfig`, đặt `basePrice` thành nullable.
  - Cập nhật [crm.api.ts](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/modules/crm/api/crm.api.ts):
    - Đảm bảo `crmApi.closeWon` truyền đúng cấu trúc payload (bao gồm `pricingModel`, `pricingConfig`, `createFinote`, `finoteAmount`, `finoteDate`, `finoteDescription`).

- [ ] **Task 3: Phát triển UI Catalog Dịch vụ**
  - Cập nhật [services.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/services.tsx):
    - Thêm trường chọn `pricingModel` trong form Thêm/Sửa dịch vụ.
    - Xây dựng Dynamic Form Section cho cấu hình biểu phí bậc thang (`TIERED_REVENUE`) sử dụng `useFieldArray` với UI thân thiện (nút Thêm/Xóa bậc thang, nhập ngưỡng min/max và số tiền).
    - Cập nhật hiển thị đơn giá gốc trên DataGrid: nếu là giá động (`MANUAL_AGREEMENT` hoặc `TIERED_REVENUE`), hiển thị Badge tương ứng thay vì giá cố định dạng tiền mặt.

- [ ] **Task 4: Phát triển Won Lead Dialog tại trang Leads & Lead Detail**
  - Cập nhật [leads.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/leads.tsx):
    - Cập nhật Dialog chốt WON hợp đồng hỗ trợ cấu hình biểu phí linh hoạt trực tiếp.
    - Đồng bộ logic hiển thị biểu phí bậc thang/thỏa thuận tay và số tiền thu cọc ban đầu.
    - Cập nhật `closeWonMutation` để truyền đúng các tham số Finote cọc mới lên API backend.
  - Cập nhật [lead-detail.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/lead-detail.tsx):
    - Đồng bộ Dialog chốt WON tương tự tại trang danh sách.

- [ ] **Task 5: Kiểm tra & Build verification**
  - Chạy `npm run check` hoặc build frontend để xác nhận không lỗi TypeScript.

---
Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
