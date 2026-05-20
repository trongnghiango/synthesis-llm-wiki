# Bước 4: Báo cáo & Lưu trữ (Walkthrough) — Module Service Catalog

## ✅ Những gì đã hoàn thành
Chúng ta đã chuyên nghiệp hóa quy trình quản lý dịch vụ và hợp đồng bằng cách chuyển từ "Free-text" sang "Structured Data".

### 1. Cơ sở dữ liệu (Schema)
- Đã tạo bảng `services`: Lưu danh mục dịch vụ chính thức (Khai báo thuế, quyết toán, tư vấn...).
- Đã tạo bảng `contract_items`: Lưu chi tiết các dịch vụ trong một hợp đồng, snapshot lại giá và mô tả tại thời điểm ký.
- Cập nhật `quote_items`: Thêm cột `service_id` để liên kết báo giá với danh mục dịch vụ.
- Đồng bộ DB qua `quick-fix.ts` thành công.

### 2. Kiến trúc Clean Architecture (Domain-Driven Design)
- **Domain:** Tạo entity `Service` với các quy tắc nghiệp vụ (activate/archive/price update).
- **Application:** Triển khai `ServiceCatalogService` để điều phối các hoạt động CRUD.
- **Infrastructure:**
  - Triển khai `DrizzleServiceRepository`.
  - Cập nhật `ContractRepository` và `QuoteRepository` để hỗ trợ load/save items đi kèm.
  - Xây dựng `ServiceMapper` chuẩn hóa dữ liệu.

### 3. Quy trình nghiệp vụ (Workflow Integration)
- **Lead to Contract:** Cập nhật `LeadWorkflowService`. Khi một Lead được chốt (WON) từ một Báo giá (Quote) đã có sẵn items, hệ thống sẽ tự động sao chép toàn bộ các hạng mục dịch vụ sang Hợp đồng mới (`contract_items`). Điều này đảm bảo tính kế thừa và Single Source of Truth.

### 4. API & Documentation
- Đã expose các đầu API tại `ServiceController`:
  - `GET /crm/services`: Danh sách dịch vụ.
  - `POST /crm/services`: Tạo dịch vụ mới.
  - `PATCH /crm/services/:id`: Cập nhật dịch vụ.
- Tích hợp Swagger đầy đủ.

## 🧪 Kết quả kiểm tra
- `npm run build`: **SUCCESS** (Vượt qua kiểm tra TypeScript và Webpack).
- Database Schema: Đã verify qua `quick-fix.ts`.

## 📌 Lưu ý cho FE Team
- Khi tạo Báo giá hoặc Hợp đồng, nên fetch danh sách từ `/api/crm/services` để người dùng chọn, thay vì nhập text thủ công.
- Các API trả về Hợp đồng/Báo giá hiện đã kèm theo mảng `items`.

---
Module `Service Catalog` đã sẵn sàng để sử dụng.
