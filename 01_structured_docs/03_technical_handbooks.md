# 📚 SỔ TAY THỰC THI KỸ THUẬT (TECHNICAL HANDBOOKS)

Sổ tay hướng dẫn thực tế các giải pháp kỹ thuật, mẫu thiết kế mã nguồn chuẩn (Design Patterns) và các công nghệ sử dụng trong hệ thống STAX.

---

## 1. MẪU ÁNH XẠ DRIZZLE ORM (ORM MAPPING PATTERNS)

Duy trì tính thuần khiết của lớp Domain yêu cầu một cơ chế ánh xạ độc lập giữa Domain Entity và Database Records (Drizzle ORM).

### 1.1) Phân tách thực thể và bản ghi (Entity vs. Record)
*   **Domain Entity (`Session`):** Chứa business logic, invariants.
*   **Database Record (`SessionRecord`):** Cấu trúc bảng do Drizzle ORM định nghĩa.

### 1.2) Mẫu thiết kế Mapper (Mapper Pattern)
Sử dụng Mapper tĩnh để chuyển đổi hai chiều tại lớp Infrastructure:

```typescript
// infrastructure/persistence/mappers/session.mapper.ts
import { Session } from '../../../domain/entities/session.entity';
import { InferSelectModel } from 'drizzle-orm';
import { sessions } from '@database/schema';

type SessionRecord = InferSelectModel<typeof sessions>;

export class SessionMapper {
  public static toDomain(record: SessionRecord): Session {
    return new Session({
      id: record.id,
      userId: record.userId,
      token: record.token,
      refreshToken: record.refreshToken,
      expiresAt: record.expiresAt,
      ipAddress: record.ipAddress ?? undefined,
      userAgent: record.userAgent ?? undefined,
      createdAt: record.createdAt,
    });
  }

  public static toPersistence(domain: Session): Partial<SessionRecord> {
    return {
      id: domain.id,
      userId: domain.userId,
      token: domain.token,
      refreshToken: domain.refreshToken,
      expiresAt: domain.expiresAt,
      ipAddress: domain.ipAddress,
      userAgent: domain.userAgent,
      created_at: domain.createdAt,
    };
  }
}
```

---

## 2. CƠ CHẾ GHI NHẬT KÝ & AUDIT LOG (LOGGING ENGINE)

STAX phân biệt rõ ràng giữa hai loại nhật ký: **System Log** (Nhật ký hệ thống) và **Audit Log** (Nhật ký thay đổi nghiệp vụ).

### 2.1) Nhật ký hệ thống (System Log)
*   Sử dụng Winston Logger Adapter được bọc trong dịch vụ `LoggerService` của NestJS.
*   Ghi nhận lỗi kỹ thuật, hiệu năng và trace-id của request.

### 2.2) Nhật ký nghiệp vụ (Audit Log & Delta Logging)
*   **Đặc điểm:** Chỉ ghi nhận khi có sự thay đổi dữ liệu nghiệp vụ do người dùng kích thích (Mutations).
*   **Delta Logging Pattern:** Chỉ lưu trữ các trường thay đổi thực sự thay vì lưu toàn bộ object. Dữ liệu thay đổi được tổ chức dưới dạng JSON:
    ```json
    {
      "fieldName": {
        "old": "Draft",
        "new": "Active"
      }
    }
    ```
*   **Không chặn luồng (Non-blocking):** Ghi log nghiệp vụ được chạy Fire-and-Forget để không làm tăng thời gian phản hồi API chính:
    ```typescript
    this.auditLog.log(action, payload).catch(err => {
      this.logger.error('Ghi Audit Log thất bại', err);
    });
    ```

---

## 3. CƠ CHẾ PHÂN QUYỀN HYBRID RBAC/ABAC

Hệ thống phân quyền STAX kết hợp tính hiệu quả của Phân quyền dựa trên vai trò (RBAC) và tính linh hoạt của Phân quyền dựa trên thuộc tính (ABAC).

### 3.1) Định nghĩa Quyền (Permissions)
*   Permission tuân thủ định dạng: `[domain]:[resource]:[action]`
    *   Ví dụ: `crm:leads:create`, `hrm:employees:delete`.

### 3.2) Cấu trúc bộ phân quyền (Policy Engine)
1.  **RBAC Check (Tầng Ngoại vi):** Kiểm tra xem User có sở hữu quyền thô đó không thông qua JWT Token claims.
2.  **ABAC Check (Tầng Nghiệp vụ):** Kiểm tra tính hợp lệ sâu hơn dựa trên thuộc tính bản ghi (e.g., nhân viên thuộc phòng ban nào, ai là chủ sở hữu bản ghi - Owner):
    ```typescript
    if (lead.ownerId !== actor.employeeId && !actor.hasAdminPermission()) {
      throw new ForbiddenException('Bạn không sở hữu Lead này');
    }
    ```

---

## 4. LUỒNG CHẠY YÊU CẦU HTTP (HTTP REQUEST FLOW)

Hiểu rõ luồng đi của một request giúp lập trình viên can thiệp đúng chỗ mà không phá vỡ kiến trúc:

```
Request ──► Middleware (ALS setup & Authentication)
             └──► Guards (RBAC Permission checks)
                   └──► Interceptors (Request logging / Trace-ID)
                         └──► Pipes (DTO validation & sanitization)
                               └──► CONTROLLER
                                     └──► USE CASE (Transaction boundary)
                                           └──► Response
```

*   **Middleware:** Lập tức thiết lập session, giải mã JWT, và gắn Tenant ID vào Async Local Storage.
*   **Guards:** Chặn thô dựa trên quyền hạn tĩnh.
*   **Interceptors:** Đo lường thời gian chạy, log request/response thô để debug.
*   **Pipes:** Convert định dạng thô từ client thành DTO sạch trước khi chuyển vào Controller.

---
*Cẩm nang này là kim chỉ nam cho mọi công việc phát triển kỹ thuật.*
