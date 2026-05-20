# Logic Analysis: Tổng hợp chỉ số doanh nghiệp (Stats Aggregation)

Tài liệu này hướng dẫn cách chuyển đổi các chỉ số "cứng" (hardcoded) thành dữ liệu động (dynamic) trên trang chi tiết công ty.

## 1. Tuân thủ Thuế (Tax Compliance)
- **Nguồn**: Bảng `tax_declarations`.
- **Cách tính**:
    - Kiểm tra các kỳ kê khai (Tháng/Quý) đã qua.
    - Nếu trạng thái `filed_at` không trống cho tất cả các kỳ -> `100% Secure`.
    - Nếu có kỳ quá hạn chưa nộp -> Hiển thị số kỳ quá hạn (VD: `2 kỳ quá hạn`).

## 2. Doanh thu YTD (Revenue Year-to-Date)
- **Nguồn**: Bảng `contracts` hoặc `invoices`.
- **Cách tính**: 
    - `SELECT SUM(amount) FROM contracts WHERE status = 'ACTIVE' AND organization_id = :id AND created_at >= '2026-01-01'`.
    - Định dạng hiển thị: Sử dụng `Intl.NumberFormat('vi-VN')` để hiển thị tiền VNĐ.

## 3. Việc cần làm (Urgent Tasks)
- **Nguồn**: Bảng `employee_tasks`.
- **Cách tính**:
    - Đếm các task có `priority = 'HIGH'` và `status != 'DONE'`.
    - `SELECT COUNT(*) FROM employee_tasks WHERE priority = 'HIGH' AND status != 'DONE' AND organization_id = :id`.

## 4. Mối quan hệ (Relationship Score)
- **Nguồn**: Bảng `client_feedback` hoặc trường `rating` trong `clients`.
- **Cách tính**:
    - Điểm trung bình đánh giá (1-5).
    - Mapping nhãn:
        - `> 4.5`: Rất tốt
        - `3.5 - 4.5`: Tốt
        - `< 3.5`: Cần cải thiện

## 5. Cấu trúc DTO đề xuất (Backend)
```typescript
interface CompanyStatsResponse {
  taxCompliance: {
    status: 'SECURE' | 'AT_RISK';
    label: string;
  };
  revenueYTD: number;
  urgentTasksCount: number;
  relationshipLabel: string;
}
```
