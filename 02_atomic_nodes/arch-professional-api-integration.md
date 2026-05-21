---
id: arch-professional-api-integration
title: Tái cấu trúc System Module & Chuẩn hóa API
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on:
  - "[[arch-clean-architecture]]"
summary: "Tái cấu trúc System Module với Service Layer, chuẩn Backend-Driven UI (_actions) và bổ sung API điều phối/báo cáo."
tags: [system-module, backend-driven-ui, action-dto, api-contract]
---

## 1. Tái cấu trúc System Module (SRP)
Tách biệt logic khỏi `SystemController` chuyển vào các service chuyên biệt:
- **`LookupService`**: Xử lý logic tra cứu và truy vấn hệ thống.
- **`BootstrapService`**: Xử lý logic khởi tạo và cấu hình ứng dụng.
- **`SystemController`**: Chỉ giữ vai trò routing và phân phối requests.

## 2. Tiêu chuẩn Backend-Driven UI (`_actions`)
Áp dụng mẫu `ActionableDto` để chuyển giao quyền kiểm soát UI từ FE về BE qua đối tượng `_actions`:
```json
{
  "data": { "id": "lead_123", "status": "processing" },
  "_actions": {
    "assign": { "enabled": true },
    "delete": { "enabled": false, "reason": "Không đủ quyền hạn" }
  }
}
```

## 3. Thiết kế API Hệ thống Mới
### 3.1. Điều phối Lead (`PATCH /crm/leads/:id/assign`)
- **Body**: `{ "assigneeId": "string" }`
- **Response**: Trả về `ActionableDto` tương ứng của Lead sau cập nhật.

### 3.2. Báo cáo nhanh hiệu suất (`GET /system/my-team/summary`)
- **Response**:
```json
{
  "summaryDate": "2026-04-28",
  "metrics": { "totalLeads": 150, "conversionRate": 0.24, "activeMembers": 8 }