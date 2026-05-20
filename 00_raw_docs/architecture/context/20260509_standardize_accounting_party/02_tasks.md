# Tasks: Accounting Party Standardization Checklist

## Infrastructure (Schema & DB)
- [x] Cập nhật `finotes.schema.ts`: Thêm `tenantId`, `organizationId`, `employeeId`, `partyName`, `partyType`.
- [x] Chạy migration hoặc cập nhật schema local.

## Domain Layer
- [x] Cập nhật thực thể `Finote`: Thêm các trường mới vào Props và Class.
- [x] Cập nhật logic khởi tạo để đảm bảo `partyName` luôn tồn tại.

## Infrastructure Layer (Persistence)
- [x] Cập nhật `FinoteMapper`: Ánh xạ các trường party mới giữa Domain và Database.
- [x] Cập nhật `DrizzleFinoteRepository`: 
    - [x] Sửa logic `findById` và `findByIdWithAttachments` để lấy thông tin đối tượng (JOIN hoặc lấy trực tiếp).
    - [x] Sửa logic `findAll` để tối ưu hóa việc lấy thông tin đối tượng.

## Application Layer
- [x] Cập nhật `FinoteService.createFinote`: 
    - [x] Nhận diện đối tượng từ đầu vào.
    - [x] Gán `partyName` và `partyType` tương ứng.
- [x] Cập nhật `FinoteResponseDto`: Định nghĩa lại cấu trúc object `party` và logic mapping `fromDomain`.

## Verification & Testing
- [x] Viết Unit Test cho `FinoteService`: Đảm bảo tạo phiếu đúng loại đối tượng.
- [x] Viết Integration Test cho `DrizzleFinoteRepository`: Kiểm tra query danh sách với đa đối tượng.
- [x] Chạy `npm run build` để kiểm tra toàn bộ hệ thống.
