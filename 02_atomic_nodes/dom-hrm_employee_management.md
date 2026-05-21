---
id: dom-hrm_employee_management
title: Quản lý Nhân sự Chuyên nghiệp Employee 360
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-stax-data-grid]]"
summary: "Thiết kế API contracts mở rộng và mô hình giao diện Employee 360 tối ưu hiệu suất cho STAX HRM."
tags: [hrm, employee-360, api-contract, schema-extension]
---

### 1. Data Contracts (`shared/contracts/hrm.ts`)
```typescript
export interface Employee {
  id: string;
  biography?: string;
  skills: Record<string, number>; // HSL Skill Matrix (level 1-5)
  certifications: ('CPA' | 'CTA' | string)[];
  activeTaskCount: number;
  totalClients: number;
  phoneNumber: string;
  status: 'Active' | 'Leave';
}

export interface HRMTask {
  id: string;
  title: string;
  assignedTo: string;
  status: 'Pending' | 'InProgress' | 'Completed';
  clientLink?: string;
}
```

### 2. API Surface (`hrm.api.ts`)
*   `getEmployeeDetail(id: string): Promise<Envelope<Employee>>`
*   `getEmployeeTasks(id: string): Promise<Envelope<HRMTask[]>>`
*   *Xử lý dữ liệu:* Giải nén từ envelope standard thông qua `result.items`.

### 3. UI/UX Architecture
*   **`EmployeeGrid`**: Sử dụng `[[hb-stax-data-grid]]` hiển thị Capacity Progress Bar (theo `activeTaskCount`) và Certification Badges.
*   **`EmployeeDetailPanel`**: Slide-out panel (`framer-motion`) tích hợp 4 Tab: Overview, Workload, Interactive Skill Matrix, và Timeline.
*   **`TaskCreateModal`**: Hỗ trợ chỉ định/gán task nhanh cho nhân sự từ Dashboard.