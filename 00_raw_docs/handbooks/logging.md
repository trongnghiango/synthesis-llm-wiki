---
title: "Kiến trúc Logging & Audit Log"
status: "actual"
level: "execution"
tags: ["logging", "audit", "observability"]
last_updated: "2026-05-11"
---

# 📝 DOCUMENTATION: ADVANCED LOGGING MODULE

## 1. Tổng quan Kiến trúc

Hệ thống Logging được thiết kế theo mô hình **Hexagonal Architecture (Ports & Adapters)**:

*   **Core Layer (Ports):** Định nghĩa *luật chơi* (`ILogger` interface). Các module nghiệp vụ chỉ giao tiếp với interface này.
*   **Infrastructure Layer (Adapters):** Thực thi luật chơi bằng thư viện **Winston**.

Mô hình này giúp tách biệt hoàn toàn code nghiệp vụ khỏi thư viện logging.

## 2. Cấu trúc File & Giải thích

```text
src/
├── core/shared/application/ports/
│   └── logger.port.ts          # [QUAN TRỌNG] Hợp đồng (Interface) và DI Token.
│
├── modules/logging/
│   ├── infrastructure/winston/
│   │   ├── winston.factory.ts  # Cấu hình Winston (màu sắc, format, rotate file).
│   │   └── winston-logger.adapter.ts # Cầu nối giữa Winston và ILogger.
│   └── logging.module.ts       # Module chính, đăng ký Provider.
│
└── api/middleware/
    └── request-logging.middleware.ts # Tự động log mọi HTTP Request/Response.
```

### Chi tiết các thành phần:

1.  **`logger.port.ts`**:
    *   Chứa Interface `ILogger` (các hàm `info`, `error`, `warn`...).
    *   Chứa Constant `LOGGER_TOKEN = 'ILogger'` dùng để Inject.
2.  **`winston.factory.ts`**:
    *   Cấu hình **Daily Rotate File**: Tự động cắt file log theo ngày (ví dụ: `application-2023-10-01.log`).
    *   Cấu hình **Console Transport**: Log màu mè đẹp mắt khi ở môi trường Dev.
3.  **`request-logging.middleware.ts`**:
    *   Tự động gán `requestId` cho mỗi request.
    *   Log thời gian xử lý (duration) và status code của API.

---

## 3. Cách sử dụng trong các Module khác

Để sử dụng Logger trong bất kỳ Service hay Controller nào (`User`, `Auth`, `Booking`...), bạn thực hiện 3 bước chuẩn chỉ sau:

### Bước 1: Import Token và Interface

```typescript
import { Inject } from '@nestjs/common';
import { ILogger, LOGGER_TOKEN } from '../../../core/shared/application/ports/logger.port';
```

### Bước 2: Inject vào Constructor

Sử dụng decorator `@Inject(LOGGER_TOKEN)` để lấy instance logger.

```typescript
@Injectable()
export class UserService {
  constructor(
    // Inject qua Token, không phụ thuộc vào Winston
    @Inject(LOGGER_TOKEN) private readonly logger: ILogger,
    
    @Inject('IUserRepository') private userRepository: IUserRepository,
  ) {}

  // ...
}
```

### Bước 3: Ghi Log

```typescript
async createUser(data: any) {
  // 1. Log Info (Thông tin chung)
  this.logger.info('Creating new user', { 
    username: data.username, 
    email: data.email 
  });

  try {
    // ... logic tạo user ...
    
    // 2. Log Debug (Chi tiết cho dev, không hiện ở production)
    this.logger.debug('User saved to database', { userId: savedUser.id });

  } catch (error) {
    // 3. Log Error (Lỗi nghiêm trọng)
    // Truyền error object vào để in ra Stack Trace
    this.logger.error('Failed to create user', error, { 
      username: data.username 
    });
    
    throw error;
  }
}
```

---

## 4. Các tính năng nâng cao

### 4.1. Request Context (Tự động theo dõi Request)
Nếu bạn gọi logger trong Controller hoặc Service được gọi từ API, logger đã tự động biết context hiện tại:
*   `requestId`: Mã định danh request (dùng để trace lỗi).
*   `ip`: IP người gọi.
*   `userId`: ID người dùng (nếu đã login).

Bạn không cần truyền thủ công các thông tin này, Middleware và Adapter đã tự xử lý.

### 4.2. Tạo Child Logger (Dành cho Cronjob hoặc Module lớn)
Nếu bạn muốn log có gắn tag riêng (ví dụ: `[PaymentService]`), hãy dùng `createChildLogger`:

```typescript
// Trong PaymentService
this.paymentLogger = this.logger.createChildLogger('PaymentService');

// Output: [2023...] [INFO] [PaymentService] Processing payment...
this.paymentLogger.info('Processing payment...');
```

---

## 5. Cấu hình Môi trường (.env)

Kiểm soát hành vi logging qua file `.env`:

```bash
# Mức độ log (debug, info, warn, error)
LOG_LEVEL=info

# Bật/Tắt log ra file (Nên bật ở Production)
LOG_FILE_ENABLED=true

# Đường dẫn lưu file log
LOG_FILE_PATH=./logs

# Cấu hình xoay vòng log (Giữ log trong bao nhiêu ngày)
LOG_FILE_MAX_FILES=30d
```

---

## 6. Tại sao kiến trúc này "Pro"?

1.  **Zero Coupling:** `UserService` hoàn toàn không có dòng code nào import `winston`.
2.  **Easy Testing:** Khi viết Unit Test cho `UserService`, bạn dễ dàng Mock cái `ILogger` mà không cần cài đặt Winston phức tạp.
3.  **Future Proof:** Nếu sau này sếp yêu cầu đổi sang đẩy log về **Datadog** hay **Sentry**, bạn chỉ cần viết lại file `infrastructure/datadog-logger.adapter.ts` và sửa 1 dòng trong `LoggingModule`. Toàn bộ code nghiệp vụ giữ nguyên 100%.
---

## 7. Audit Logging & Activity Feed (Ghi log nghiệp vụ)

Khác với Application Logs (Winston) dùng để debug, **Audit Logs** được lưu vào Database để phục vụ việc truy vết nghiệp vụ và hiển thị Timeline cho người dùng.

### 7.1. Cách thức hoạt động
Hệ thống sử dụng cơ chế **Event-Driven**:
1.  Module nghiệp vụ phát hành một **Domain Event** implement interface `IAuditableEvent`.
2.  `AuditDomainEventHandler` tự động bắt sự kiện và gọi `AuditLogService` để lưu vào bảng `audit_logs`.

### 7.2. Tiêu chuẩn "Clean Metadata"
Để Activity Feed hiển thị chuyên nghiệp, mọi `IAuditableEvent` cần tuân thủ:
*   **Actor Context**: Luôn truyền `actorId` và `actorName` ở cấp root của Audit Entry để định danh chính xác người thực hiện.
*   **Structured Metadata**: Không ghi log bằng text thô. Hãy đóng gói dữ liệu vào trường `metadata` (JSONB).
    *   *Ví dụ:* `metadata: { feeAmount: 5000000, contractNumber: 'HD-001' }`
*   **Professional Templates**: Khai báo mapping trong `ActivityFormatter` để chuyển đổi metadata thành câu văn xuôi tiếng Việt hoàn chỉnh.

### 7.3. Triển khai một Event mới
```typescript
export class ContractCreatedEvent implements IAuditableEvent {
    toAuditEntry(): AuditEntryPayload {
        return {
            action: 'CONTRACT.CREATED',
            resource: 'contracts',
            resourceId: this.contract.id,
            actorId: this.actorId,     // Cấp root
            actorName: this.actorName, // Cấp root
            metadata: {
                feeAmount: this.contract.value,
                description: `Đã tạo hợp đồng ${this.contract.contractNumber}`
            }
        };
    }
}
```
