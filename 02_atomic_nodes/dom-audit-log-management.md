---
id: dom-audit-log-management
title: Hệ thống Quản trị Audit Log
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-delta-logging]]"
  - "[[dom-accounting-finote]]"
summary: "Hệ thống giám sát Audit Log thời gian thực (Polling 30s) hỗ trợ so sánh dữ liệu Delta JSON và điều hướng nhanh đến tài nguyên."
tags: [audit-log, polling, delta-view, monitoring, system-module]
---

## 1. Kiến trúc & Thiết kế Kỹ thuật
*   **Cơ chế Live Monitor:** Sử dụng TanStack Query Polling (interval 30s) trên nền tảng RESTful API để đảm bảo giám sát liên tục mà không phát sinh chi phí hạ tầng WebSocket.
*   **Cơ chế Delta Logging:** Lưu vết trạng thái dữ liệu trước (`before`) và sau (`after`) dưới dạng JSON struct. Giao diện hiển thị trực quan qua Delta View Modal.
*   **Smart Routing:** Tích hợp liên kết động (Smart Link) cho phép điều hướng trực tiếp từ dòng log đến thực thể liên quan trong CRM (Leads, Contracts) và Accounting (`[[dom-accounting-finote]]`).

## 2. API Contract & Schema Tham chiếu
```typescript
interface AuditLog {
  id: string;
  userId: string;
  action: 'CREATE' | 'UPDATE' | 'DELETE' | 'AUTH';
  module: 'CRM' | 'ACCOUNTING' | 'SYSTEM';
  severity: 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  delta: {
    before: Record<string, any> | null;
    after: Record<string, any> | null;
  };
  resourceId: string;
  createdAt: string;
}
```

## 3. Khắc phục Sự cố & Tối ưu
*   **Fix Type Mismatch:** Đồng bộ và sửa lỗi kiểu dữ liệu tham số đầu vào cho component `RoleDetail` trong cấu hình Router hệ thống.
*   **Responsive DataGrid:** Cấu hình thuộc tính cuộn ngang (horizontal scroll) và ghim cột (column pinning) trên UI Grid để hiển thị tốt trên thiết bị di động.