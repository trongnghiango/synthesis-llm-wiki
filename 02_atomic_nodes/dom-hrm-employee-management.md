---
id: dom-hrm-employee-management
title: "Quản lý Nhân sự Phân hệ HRM (Employee 360)"
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Mở rộng schema Employee, bổ sung HRMTask API, và tích hợp bộ UI Component Employee 360 sử dụng STAX DataGrid."
tags: [hrm, schema, api-contract, employee-360, datagrid]
---

### 1. Data Schema & API Contract (`shared/contracts/hrm.ts`)
*   **Mở rộng `Employee` interface**: Bổ sung các trường chuyên môn:
    *   `biography: string`, `skills: Skill[]`, `certifications: string[]` (e.g., CPA, CTA).
    *   `activeTaskCount: number`, `totalClients: number`, `phoneNumber: string` (đồng bộ backend).
*   **Interface mới `HRMTask`**: Biểu diễn các đầu việc nội bộ hoặc dự án khách hàng gán cho nhân sự.
*   **API Surface (`hrm.api.ts`)**:
    *   `getEmployeeDetail(id)`: Lấy chi tiết hồ sơ 360 độ.
    *   `getEmployeeTasks(id)`: Lấy danh sách task gán cho nhân sự.
    *   *Xử lý dữ liệu*: Bóc tách dữ liệu chuẩn hóa từ cấu trúc bọc (`result.items`).

### 2. Cấu trúc UI Components (`modules/hrm`)
*   **`EmployeeGrid`**: Sử dụng hệ thống `[[hb-stax-datagrid]]` mật độ thông tin cao.
    *   Hiển thị tiến độ phân tải (Capacity Progress Bar) dựa trên `activeTaskCount`.
    *   Badge trạng thái hoạt động (Active/Leave) và chứng chỉ chuyên môn.
*   **`EmployeeDetailPanel`**: Slide-out panel dùng `framer-motion` chia thành 4 Tab:
    *   *Overview*: Bio & Thông tin liên hệ.
    *   *Workload*: Danh sách Real-time tasks & Liên kết khách hàng.
    *   *Skills*: Ma trận kỹ năng tương tác (Đánh giá mức độ 1-5 sao).
    *   *Timeline*: Nhật ký hoạt động & Cột mốc sự nghiệp.
*   **`TaskCreateModal`**: Modal tạo và gán việc nhanh trực tiếp từ Dashboard.