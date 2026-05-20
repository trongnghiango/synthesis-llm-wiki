# Walkthrough: Accounting Party Standardization

Chúng ta đã hoàn thành việc chuẩn hóa dữ liệu cho Đối tượng kế toán (Party) trong module Accounting, giải quyết triệt để vấn đề nhầm lẫn giữa Chủ thể (Tenant) và Đối tượng giao dịch (Partner).

## Các thay đổi chính

### 1. Database Schema (`finotes.schema.ts`)
- Thêm `tenantId`: Đảm bảo cách ly dữ liệu theo đơn vị sở hữu.
- Thêm bộ trường Party: `organizationId`, `employeeId`, `partyName`, `partyType`.
- Lưu trực tiếp `partyName` và `partyType` vào bảng `finotes` để tối ưu hiệu năng hiển thị (không cần JOIN).

### 2. Domain Layer (`finote.entity.ts`)
- Tích hợp interface `FinoteParty` vào thực thể `Finote`.
- Thêm Business Rule: Cấm tạo phiếu nếu không có thông tin đối tượng (`party.name`).

### 3. Application Layer (`finote.service.ts` & `finote-response.dto.ts`)
- **FinoteService**: Tự động phân giải tên và loại đối tượng từ Database khi tạo phiếu, đảm bảo tính chính xác và không phụ thuộc vào dữ liệu đầu vào từ Frontend.
- **FinoteResponseDto**: Trả về object `party` có cấu trúc: `{ id, name, type }`, giúp Frontend hiển thị Icon và Label một cách nhất quán.

## Kết quả kiểm tra

### 1. Build Verification
Hệ thống đã được build thành công với 0 lỗi TypeScript.
```bash
> npm run build
webpack 5.104.1 compiled successfully in 18173 ms
```

### 2. Unit & Integration Tests
Tất cả các bản test đã được cập nhật để tương thích với cấu trúc dữ liệu mới:
- `finote.entity.spec.ts`: Passed
- `finote.service.spec.ts`: Passed
- `drizzle-finote.repository.spec.ts`: Passed

## Hướng dẫn cho Frontend
API `GET /accounting/finotes` giờ đây trả về dữ liệu đối tượng trong field `party`:
```json
{
  "id": 123,
  "code": "INC-2026-0001",
  "party": {
    "id": 101,
    "name": "Công ty TNHH STAX",
    "type": "ORGANIZATION"
  },
  ...
}
```
Frontend có thể dựa vào `party.type` để hiển thị Icon (User cho `EMPLOYEE`, Building cho `ORGANIZATION`, v.v.) và `party.name` làm nhãn hiển thị.
