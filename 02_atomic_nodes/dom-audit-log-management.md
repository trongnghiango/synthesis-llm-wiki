---
id: dom-audit-log-management
title: Hệ thống Quản trị Audit Log
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
  - "[[dom-accounting-finote]]"
summary: "Hệ thống giám sát và truy vết thay đổi dữ liệu (Audit Log) thời gian thực sử dụng Polling và Delta JSON View."
tags: [audit-log, delta-logging, real-time-polling, system-monitoring, crm-routing]
---

## 1. Thiết kế Kiến trúc & Giải pháp Kỹ thuật
- **Cơ chế Real-time:** Sử dụng TanStack Query Polling (chu kỳ 30 giây) trên nền RESTful API hiện có của STAX để liên tục cập nhật trạng thái hệ thống mà không cần WebSockets.
- **[[hb-delta-logging]]:** Lưu trữ cấu trúc JSON ghi nhận trạng thái dữ liệu trước (`before`) và sau (`after`) khi thay đổi. Client render trực quan qua Delta View Modal.
- **Smart Routing:** Tích hợp liên kết điều hướng nhanh từ log record sang các domain liên quan: Leads, Contracts, và `[[dom-accounting-finote]]`.

## 2. API Contract & Schema Yêu cầu
- **Schema Log cơ bản:** 
  ```typescript
  interface AuditLog {
    id: string; // UUID
    timestamp: string; // ISO8601
    userId: string;
    module: string; // 'SYSTEM' | 'CRM' | 'FINANCE'
    action: string; // 'CREATE' | 'UPDATE' | 'DELETE'
    severity: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
    payload: {
      before: Record<string, any> | null;
      after: Record<string, any> | null;
    };
  }
  ```
- **API Endpoint:** `GET /api/v1/audit-logs?page=1&limit=10&severity=ERROR&module=SYSTEM`

## 3. Khó khăn Kỹ thuật & Khắc phục
- **Type Mismatch:** Khắc phục lỗi mismatch kiểu dữ liệu của tham số truyền vào component `RoleDetail` trong cấu hình Router hệ thống.
- **Responsive Table:** Tối ưu hóa UI DataGrid với thuộc tính cuộn ngang (overflow-x/scroll) để tương thích tốt trên các thiết bị di động.

## 4. Kế hoạch mở rộng (Next Steps)
- Phát triển API và tích hợp Engine xuất dữ liệu báo cáo dạng Excel/CSV.
- Bổ sung Dashboard Widget trực quan hóa tần suất xuất hiện log lỗi (`ERROR`/`CRITICAL`) theo chuỗi thời gian (time-series).