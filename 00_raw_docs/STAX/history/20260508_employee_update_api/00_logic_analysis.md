# Phân tích Logic: Cập nhật thông tin Nhân sự (Employee Update)

## 1. Mục tiêu
Giải quyết lỗi `404 Cannot PATCH /api/hrm/employees/:id` bằng cách cung cấp một API cập nhật linh hoạt, cho phép Frontend thay đổi các thông tin như Vị trí (Position), Địa điểm (Location), và các thông tin cá nhân khác.

## 2. Các ràng buộc nghiệp vụ (Business Constraints)
- **Multi-tenancy**: Chỉ người có quyền và thuộc cùng một `organizationId` mới có thể cập nhật thông tin nhân viên.
- **Tính hợp lệ của Vị trí (Position Validation)**:
    - Nếu cập nhật `positionId`, hệ thống phải kiểm tra xem vị trí đó có tồn tại trong Database không.
    - Vị trí mới phải thuộc cùng một `organizationId` với nhân viên.
    - (Optional) Kiểm tra trạng thái hoạt động của vị trí.
- **Tính nhất quán của Dữ liệu**: `updatedAt` phải được cập nhật mỗi khi có thay đổi.

## 3. Cấu trúc dữ liệu (DTO)
`UpdateEmployeeRequestDto` sẽ bao gồm các trường tùy chọn:
- `fullName`: string
- `phoneNumber`: string
- `locationId`: number
- `positionId`: number
- `managerId`: number
- `dateOfBirth`: Date
- `avatarUrl`: string
- `joinDate`: Date

## 4. Luồng xử lý (Flow)
1. Controller nhận `id` và `dto`, lấy `currentUser.organizationId`.
2. Service tìm kiếm Employee theo `id`.
3. Kiểm tra nếu `employee.organizationId !== currentUser.organizationId` -> Ném lỗi Unauthorized/Forbidden.
4. Nếu có `positionId` trong DTO:
    - Tìm kiếm Position.
    - Kiểm tra Position có thuộc Org không.
5. Cập nhật các trường từ DTO vào Entity Employee.
6. Lưu Entity qua Repository.
