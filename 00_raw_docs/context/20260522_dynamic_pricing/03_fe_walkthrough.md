# Frontend Dynamic Pricing Integration - Walkthrough

Chúng ta đã hoàn thành việc tích hợp giao diện người dùng (Frontend) cho luồng cấu hình Biểu phí động và doanh thu bậc thang trong CRM.

## 1. Tóm tắt tính năng (Feature Summary)

- **Cấu hình Catalog Dịch vụ mẫu**:
  - Tích hợp biểu mẫu chọn mô hình tính giá (`FIXED`, `MANUAL_AGREEMENT`, `TIERED_REVENUE`) trên màn hình Catalog Dịch vụ ([services.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/services.tsx)).
  - Thiết kế bảng nhập bậc thang động (Min Revenue, Max Revenue, Fee Amount) sử dụng `useFieldArray` từ `react-hook-form`.
  - Hiển thị badge mô hình tính giá tương ứng trên DataGrid để thay thế hiển thị giá trị thô cố định.
- **Quy trình chốt hợp đồng (Won Lead)**:
  - Tích hợp biểu mẫu thiết lập biểu phí động ngay trong Dialog Chốt Hợp Đồng tại trang Kanban Leads ([leads.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/leads.tsx)) và trang Chi tiết cơ hội ([lead-detail.tsx](file:///home/ka/Repos/github.com/trongnghiango/STAX_ASP/frontend/client/src/pages/admin/crm/lead-detail.tsx)).
  - Tự động điền dữ liệu (pre-fill) từ cấu hình dịch vụ mẫu liên kết để giảm thiểu thao tác nhập liệu của nhân viên kinh doanh.
  - Tùy chỉnh thông minh nhãn tạo Phiếu thu (Finote) dựa trên mô hình giá được chọn.
  - Chuyển giao hoàn toàn logic tạo phiếu thu cọc ban đầu về Backend thông qua Event Bus để đảm bảo tính bao gói.

---

## 2. Quyết định kiến trúc UI/UX (Architecture Decisions)

- **Server-Driven UI / Conditional UI**:
  - Giao diện Dialog và Form tự động ẩn/hiện và thay đổi validator dựa trên trường `pricingModel` được chọn. Điều này giúp giao diện tinh gọn, tránh làm phiền Sales bằng những trường dữ liệu không cần thiết.
- **Nhất quán qua Shared Contracts**:
  - Toàn bộ Schema và Validation trên Form đều được ánh xạ trực tiếp từ `closeWonSchema` của `shared/contracts/crm.ts`, đảm bảo tính an toàn kiểu dữ liệu và chống sai lệch hợp đồng API (Contract drift).
- **Delegation of Finote Logic**:
  - Việc loại bỏ lệnh gọi API tạo Finote trực tiếp từ Frontend và chuyển về dạng Event-Driven trên Backend giúp giảm số lượng API request đồng thời từ client, cải thiện hiệu năng và hạn chế xung đột trạng thái dữ liệu (race conditions).

---

## 3. Khó khăn & Xử lý (Troubleshooting)

- **TypeScript Type Error**:
  - Phát hiện lỗi gán kiểu dữ liệu đối với `service.basePrice` (có thể là `null` hoặc `undefined`) tại `lead-detail.tsx` dòng 324. Đã xử lý triệt để bằng cách gán mặc định thông qua toán tử nullish coalescing: `service.basePrice ?? 0`.
- **Đồng bộ hóa Báo giá (Quotes) vs Chốt trực tiếp**:
  - Do Báo giá (Quotes) mặc định chỉ hỗ trợ biểu phí cố định (`FIXED`), chúng tôi đã thiết lập ẩn nút chọn Mô hình giá khi chốt hợp đồng từ Báo giá đã chấp nhận, đồng thời hiển thị thông tin cảnh báo rõ ràng. Mô hình giá động chỉ hiển thị khi Sales thực hiện "Chốt Trực Tiếp" (chốt tay).

---

## 4. Hướng phát triển (Next Steps)

- Hỗ trợ mô hình tính giá bậc thang trực tiếp khi lập bảng báo giá (Quotes) ở các pha nâng cấp tiếp theo nếu có yêu cầu nghiệp vụ.
