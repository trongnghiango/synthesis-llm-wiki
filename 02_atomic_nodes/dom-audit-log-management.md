---
id: dom-audit-log-management
title: Hệ Thống Quản Trị Audit Log
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
summary: "Hệ thống giám sát Audit Log thời gian thực sử dụng TanStack Query Polling, hỗ trợ Delta View đối sánh dữ liệu JSON và Smart Routing."
tags: [audit-log, polling, delta-view, smart-routing, monitoring]
---

### 1. Giải Pháp Kiến Trúc & Thiết Kế
* **Cơ chế Real-time (Polling over WebSocket):** Sử dụng TanStack Query Polling với chu kỳ `30s` để tận dụng hạ tầng RESTful sẵn có, giảm tải hạ tầng và đảm bảo tính cập nhật liên tục.
* **Delta Logging & View:** Biểu diễn trực quan biến động dữ liệu bằng cách lưu trữ và so sánh trạng thái trước (`before`) và sau (`after`) dưới dạng JSON formatted trong Modal chi tiết.
* **Smart Routing:** Tích hợp liên kết điều hướng nhanh từ dòng log đến trực tiếp các tài nguyên liên quan trong CRM (`[[dom-crm-leads]]`, `[[dom-crm-contracts]]`) và Kế toán (`[[dom-accounting-finote]]`).

### 2. Thiết Kế API & Cấu Trúc Dữ Liệu
```typescript
interface AuditLog {
  id: string;
  timestamp: string; // ISO 8601
  module: 'CRM' | 'ACCOUNTING' | 'SYSTEM';
  severity: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  action: string;
  userId: string;
  resourceId: string;
  delta: {
    before: Record<string, any> | null;
    after: Record<string, any> | null;
  };
}
```

### 3. Xử Lý Điểm Nghẽn (Troubleshooting)
* **Type Mismatch:** Khắc phục triệt để lỗi ép kiểu / truyền sai tham số cho cấu hình định tuyến của component `RoleDetail`.
* **UI/UX DataGrid:** Tối ưu CSS Grid cho phép cuộn ngang (horizontal scroll) mượt mà trên Mobile view.

### 4. Roadmap Phát Triển Tiếp Theo
* Bổ sung tính năng kết xuất (Export) dữ liệu báo cáo dạng Excel/CSV.
* Tích hợp Dashboard Widget thống kê tần suất lỗi (`ERROR`/`CRITICAL`) theo chuỗi thời gian thực.