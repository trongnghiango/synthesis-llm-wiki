# Bước 2️⃣: Kế hoạch Kiến trúc Chi tiết (fix_lead_acquired_at_display)

## A. Database Schema — Drizzle ORM
- Không thay đổi. Cột `acquired_at` đã tồn tại trong bảng `leads` của Database:
  ```typescript
  acquiredAt: timestamp('acquired_at').defaultNow().notNull()
  ```

## B. Domain Layer
- Không thay đổi. Thực thể `Lead` (`lead.entity.ts`) đã có đầy đủ thuộc tính `acquiredAt` trong `LeadProps` và getter `get acquiredAt()` tương ứng.

## C. Infrastructure Layer
- Không thay đổi. `LeadMapper` (`lead.mapper.ts`) đã thực hiện mapping hai chiều cho thuộc tính này:
  - `toDomain`: `acquiredAt: raw.acquiredAt ? new Date(raw.acquiredAt) : undefined`
  - `toPersistence`: `acquiredAt: domain.acquiredAt`

## D. Application Layer
- Không thay đổi logic nghiệp vụ của Service. Chỉ điều chỉnh mapping ở Presentation Layer.

## E. Presentation Layer & Contracts
- **Shared Contracts**:
  - Không cần sửa đổi file `shared/contracts/crm.ts` của frontend và backend vì giao ước `Lead` interface đã khai báo sẵn thuộc tính:
    ```typescript
    acquiredAt?: string;
    ```
- **Response DTO**:
  - Sửa đổi file: `backend/src/modules/crm/infrastructure/dtos/lead.response.dto.ts`
  - Thêm thuộc tính `acquiredAt` kiểu dữ liệu `Date` vào DTO:
    ```typescript
    @ApiPropertyOptional({ description: 'Ngày tiếp nhận Lead thực tế từ nghiệp vụ' })
    acquiredAt?: Date;
    ```
- **Query Service Mapping**:
  - Sửa đổi file: `backend/src/modules/crm/application/services/lead-query.service.ts`
  - Trong hàm private `mapToResponse`, bổ sung `acquiredAt` vào payload trả về:
    ```typescript
    acquiredAt: lead.acquiredAt,
    ```

## F. Module Wiring
- Không thay đổi. Hệ thống NestJS DI và Controller bindings giữ nguyên.

---
Kế hoạch này đã chuẩn chưa? Nếu OK, tôi sẽ xuất Checklist.
