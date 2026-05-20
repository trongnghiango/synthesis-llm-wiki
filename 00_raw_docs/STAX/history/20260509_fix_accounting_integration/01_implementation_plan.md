# Implementation Plan: Chuẩn hóa Tích hợp Kế toán (CRM-to-Accounting)

## A. Database & Schema
- Không thay đổi Schema. Giữ nguyên `requested_by_id` tham chiếu `employees.id`.
- Đảm bảo `source_org_id` không được null để record luôn hiển thị đúng Tenant.

## B. Domain Layer
- **Finote Entity:** Đảm bảo `requestedById` là ID nhân sự. Thêm validation trong constructor để đảm bảo `totalAmount` không âm.
- **FinoteMapper:** Chuyển đổi chính xác kiểu dữ liệu (Numeric -> Number, ISO String -> Date).

## C. Application Layer
- **FinoteService:** 
    - Phương thức `createFinote` sẽ nhận `creatorId` (User ID) và `orgId` (từ Session).
    - Thêm bước kiểm tra: `const employee = await employeeRepo.findByUserId(creatorId)`. Nếu không có Employee Profile, ném lỗi `BusinessRuleValidationException`.
    - Tự động gán `sourceOrgId = orgId` nếu DTO không truyền lên.

## D. API Contracts
- **CreateFinoteRequestDto:**
    - Sử dụng Class-Transformer để ánh xạ các trường cũ:
        - `@Expose({ name: 'transactionDate' })` ánh xạ vào `deadlineAt`.
        - `@Expose({ name: 'type' })` với logic xử lý `RECEIPT` -> `INCOME`.
    - Khôi phục `@IsNotEmpty()` và `@IsEnum()` để đảm bảo an toàn dữ liệu.
- **FinoteController:**
    - Loại bỏ mọi logic vá víu (debug logs, validation bypass).
    - Triển khai `GET /api/accounting/finotes` với phân trang chuẩn.

## E. Testing Strategy
- **Integration Test (Repository):** Sử dụng `pglite` để kiểm tra việc `insert` và `findAll` hoạt động đúng với các ràng buộc Database thực tế.
- **Unit Test (Service):** Mock `EmployeeRepository` để kiểm tra logic mapping ID.

## F. Decision Log
1. **Tại sao giữ requestedById là Employee ID?** Vì trong nghiệp vụ kế toán của STAX, mọi chứng từ phải được gắn với một nhân sự cụ thể (Staff) để tính lương, KPI và trách nhiệm. User ID chỉ là tài khoản đăng nhập, không đại diện cho vai trò nhân sự.
2. **Xử lý FE cũ:** Thay vì nới lỏng DTO, ta dùng Class-Transformer để "dọn dẹp" dữ liệu ngay khi nó bước vào hệ thống, giữ cho lõi (Domain) luôn sạch.
