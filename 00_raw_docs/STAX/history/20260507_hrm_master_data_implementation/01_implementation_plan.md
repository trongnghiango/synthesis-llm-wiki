# Implementation Plan: Danh mục HRM (Master Data)

## 1. Tổ chức Module (Folder Structure)
Để tuân thủ Clean Architecture, chúng ta sẽ tổ chức như sau:
```
client/src/
  ├── modules/hrm/
  │     ├── api/hrm.api.ts (Infrastructure)
  │     ├── components/ (Presentation - Reusable)
  │     │     ├── JobTitleTable.tsx
  │     │     └── SalaryGradeTable.tsx
  ├── pages/admin/hrm/
  │     └── master-data.tsx (Application/Presentation - Page)
```

## 2. API Design (Infrastructure Layer)
Bổ sung vào `hrm.api.ts`:
- `GET /hrm/job-titles`: Lấy danh sách chức danh.
- `POST /hrm/job-titles`: Tạo mới.
- `PATCH /hrm/job-titles/:id`: Cập nhật.
- `DELETE /hrm/job-titles/:id`: Xóa.
- Tương tự cho `salary-grades`.

## 3. State Management (Application Layer)
Sử dụng `useQuery` với `queryKey: ['hrm', 'job-titles']` để đảm bảo dữ liệu được cache và đồng bộ trên toàn ứng dụng.

## 4. UI/UX (Presentation Layer)
- Trang `master-data.tsx` sẽ đóng vai trò là "Container".
- Sử dụng `shadcn/ui` (Tabs, Table, Dialog, Form) để đảm bảo giao diện premium và đồng nhất với các module khác.
