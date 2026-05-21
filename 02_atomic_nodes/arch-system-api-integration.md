---
id: arch-system-api-integration
title: Tách Biệt Logic System Module & Chuẩn Hóa Backend-Driven UI
layer: 3-atomic
parent: "[[01_core_architecture]]"
depends_on: []
summary: "Tái cấu trúc SystemModule sử dụng Lookup/Bootstrap Service và triển khai chuẩn Backend-Driven UI thông qua ActionableDto."
tags: [system-module, backend-driven-ui, actionable-dto, api-design]
---

## 1. Tái Cấu Trúc System Module
Loại bỏ hoàn toàn fat-controller tại `SystemController` bằng cách phân rã trách nhiệm:
- **`BootstrapService`**: Đảm nhận toàn bộ tiến trình khởi tạo hệ thống, thiết lập môi trường và seed dữ liệu ban đầu.
- **`LookupService`**: Tập trung xử lý các truy vấn tra cứu danh mục, cấu hình hệ thống và dữ liệu tham chiếu tĩnh.
- **`SystemController`**: Giữ vai trò là Router mỏng (Thin Controller), chỉ nhận request, validate và chuyển tiếp xử lý cho Service tương ứng.

## 2. Tiêu Chuẩn Backend-Driven UI (`_actions`)
Áp dụng mẫu thiết kế `ActionableDto` cho các thực thể nghiệp vụ có trạng thái phức tạp. Logic kiểm tra quyền và điều kiện thực hiện hành động được tập trung xử lý tại Backend và trả về Frontend qua cấu trúc:

```typescript
export interface ActionableDto<T> {
  data: T;
  _actions: {
    [actionKey: string]: {
      enabled: boolean;
      reason?: string; // Trả về lý do cụ thể nếu enabled = false để hiển thị trực tiếp lên tooltip UI
    };
  };
}
```

## 3. Danh Sách API Tích Hợp Mới

### 3.1. Phân phối Lead (CRM Module)
- **Endpoint**: `PATCH /crm/leads/:id/assign`
- **Payload**:
  ```json
  {
    "assigneeId": "uuid-nhan-vien"
  }
  ```
- **Response**: Trả về `ActionableDto` của Lead sau khi được điều phối kèm trạng thái hành động kế tiếp.

### 3.2. Báo Cáo Hiệu Suất Nhóm (Management API)
- **Endpoint**: `GET /system/my-team/summary`
- **Response Schema**:
  ```json
  {
    "summary": {
      "totalLeads": 150,
      "conversionRate": 12.5,
      "activeMembers": 8
    }
  }
  ```

---
*Liên kết liên quan:* `[[01_core_architecture]]`, `[[hb-delta-logging]]`