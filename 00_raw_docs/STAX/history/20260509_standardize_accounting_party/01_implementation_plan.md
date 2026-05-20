# Implementation Plan: Accounting Party Standardization

## A. Database & Schema
Cập nhật bảng `finotes` trong file `src/database/schema/accounting/finotes.schema.ts`:
- **`tenantId`**: `bigint` (NotNull) - Định danh công ty chủ quản (Tenancy).
- **`organizationId`**: `bigint` (Nullable) - Tham chiếu đến `organizations`.
- **`employeeId`**: `integer` (Nullable) - Tham chiếu đến `employees`.
- **`partyName`**: `text` (NotNull) - Lưu tên đối tượng tại thời điểm lập phiếu (Cả chính quy và vãng lai).
- **`partyType`**: `pgEnum` ('ORGANIZATION', 'EMPLOYEE', 'INCIDENTAL') - Loại đối tượng để UI hiển thị Icon.

## B. Domain Layer
Refactor thực thể `Finote` tại `src/modules/accounting/domain/entities/finote.entity.ts`:
- Sử dụng mô hình **Unified Party**:
  ```typescript
  interface FinoteParty {
    name: string;
    type: 'ORGANIZATION' | 'EMPLOYEE' | 'INCIDENTAL';
    organizationId?: number;
    employeeId?: number;
  }
  ```
- **Invariants:** Mỗi phiếu bắt buộc phải có `partyName`. Nếu là đối tượng chính quy, phải có ID tương ứng.

## C. Application Layer
Cập nhật `FinoteService`:
- `createFinote`: Logic nhận diện đối tượng. Nếu tạo từ Lead -> Gán `organizationId` + `partyType='ORGANIZATION'`. Nếu chi lương -> Gán `employeeId` + `partyType='EMPLOYEE'`.
- Sử dụng `ITransactionManager` để đảm bảo tính nguyên tử khi tạo phiếu và các item đi kèm.

## D. API Contracts
Cập nhật `FinoteResponseDto`:
- Trả về object `party` thống nhất:
  ```json
  "party": {
    "name": "Công ty ABC",
    "type": "ORGANIZATION",
    "id": 123
  }
  ```

## E. Testing Strategy
- **Unit Test (Service):** Kiểm tra logic gán đúng `partyType` khi input khác nhau.
- **Integration Test (Repo):** Sử dụng PGLite để test query lấy danh sách Finote, đảm bảo JOIN đúng thông tin Organization/Employee hoặc lấy `partyName` nếu là đối tượng vãng lai.

## F. Decision Log
- **Tại sao lưu `partyName` trực tiếp?** Để đảm bảo tính Audit (Hóa đơn cũ phải giữ tên cũ) và tối ưu hiệu năng List View (Không cần JOIN lấy tên nếu không cần thông tin chi tiết).
- **Tại sao dùng 2 trường ID riêng biệt?** Thay vì dùng Polymorphic (rất khó quản lý trong SQL truyền thống), việc dùng 2 trường Nullable giúp DB quản lý Foreign Key tốt hơn và dễ truy vấn.
