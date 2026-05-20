# Danh sách công việc: Triển khai Employee Update API

- [x] 1. Khởi tạo DTO `UpdateEmployeeRequestDto`
    - File: `src/modules/employee/infrastructure/dtos/update-employee.request.dto.ts`
- [x] 2. Cập nhật `EmployeeService`
    - Thêm phương thức `updateEmployee`
    - Implement logic kiểm tra quyền và validate positionId
- [x] 3. Cập nhật `EmployeeController`
    - Thêm endpoint `PATCH /api/hrm/employees/:id`
- [x] 4. Viết Unit Test cho Service
    - File: `src/modules/employee/application/services/employee.service.spec.ts`
- [x] 5. Chạy test và xác minh
- [x] 6. Báo cáo hoàn thành (Walkthrough)
