---
id: dom-company-stats-aggregation
title: Tổng hợp chỉ số doanh nghiệp
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Định nghĩa logic truy vấn và cấu trúc DTO tổng hợp chỉ số vận hành, tài chính, thuế và hiệu năng doanh nghiệp."
tags: [domain, company-stats, finance, kpi]
---

## 1. Logic Tính Toán & Nguồn Dữ Liệu

- **Thuế (`tax_declarations`)**:
  - Kiểm tra các kỳ kê khai (Tháng/Quý) đã qua.
  - Nếu tất cả các kỳ đều có `filed_at IS NOT NULL` -> `SECURE` (Nhãn: `"100% Secure"`).
  - Ngược lại -> `AT_RISK` (Nhãn: `"X kỳ quá hạn"`).
- **Doanh thu YTD (`contracts` hoặc `invoices`)**:
  - Truy vấn: `SELECT SUM(amount) FROM contracts WHERE status = 'ACTIVE' AND organization_id = :id AND created_at >= '2026-01-01'`.
  - Định dạng hiển thị phía Client: `Intl.NumberFormat('vi-VN')`.
- **Task khẩn cấp (`employee_tasks`)**:
  - Truy vấn: `SELECT COUNT(*) FROM employee_tasks WHERE priority = 'HIGH' AND status != 'DONE' AND organization_id = :id`.
- **Mối quan hệ (`client_feedback` / `clients`)**:
  - Điểm trung bình `rating` (1-5) của khách hàng liên kết.
  - Phân loại nhãn: `> 4.5` (Rất tốt) | `3.5 - 4.5` (Tốt) | `< 3.5` (Cần cải thiện).

## 2. API Contract (Backend DTO)

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