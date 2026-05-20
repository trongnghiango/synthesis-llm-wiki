# Refactor: Chuẩn hóa truy cập `organizationId` qua User Entity Getter

**Ngày:** 2026-05-08  
**Module liên quan:** `user`, `auth`, `crm`, `employee`, `org-structure`

---

## 1. Vấn đề Phát Hiện (Problem Discovery)

### Triệu chứng ban đầu
Khi review code, nhận thấy pattern lặp lại nhiều lần ở nhiều module khác nhau:

```typescript
// Pattern 1 — Chỉ lấy từ Employee context
const orgId = user.profileContext?.employee?.organizationId;

// Pattern 2 — Cố gắng lấy từ cả hai context nhưng viết thủ công
const orgId = currentUser?.profileContext?.organization?.id 
           || currentUser?.profileContext?.employee?.organizationId;

// Pattern 3 — Có fallback mặc định nguy hiểm (hardcode)
const orgId = user.profileContext?.employee?.organizationId || 1; // ⚠️ BUG TIỀM ẨN
```

### Danh sách các file bị ảnh hưởng (trước khi refactor)
| File | Pattern sử dụng |
|------|----------------|
| `hrm-master-data.controller.ts` | Pattern 1 (×2) |
| `org-structure.controller.ts` | Pattern 1 |
| `employee.controller.ts` | Pattern 3 ⚠️ (hardcode fallback `|| 1`) |
| `company-import.controller.ts` | Pattern 1 |
| `lead-query.service.ts` | Pattern 2 (×2) |

---

## 2. Phân tích Nguyên Nhân Gốc Rễ (Root Cause Analysis)

### Tại sao lại có nhiều pattern khác nhau?

Hệ thống STAX hỗ trợ **hai loại người dùng** gắn với tổ chức theo hai cách khác nhau:

```
User
├── profileContext.employee.organizationId  → Nhân viên (Employee) của một Công ty khách hàng
│                                             VD: Kế toán viên của Công ty ABC
└── profileContext.organization.id          → Chủ sở hữu/Quản trị viên của một Tổ chức
                                              VD: Giám đốc của Công ty ABC đăng ký tài khoản
```

Khi thêm tính năng Multi-tenancy, mỗi developer đã tự xử lý việc này theo cách riêng, dẫn đến:
- Code bị **phân tán** và **không nhất quán**
- Dễ sai sót khi chỉ xử lý một trong hai context
- Một nơi có bug nguy hiểm: `|| 1` (fallback về orgId=1) có thể khiến dữ liệu bị trộn lẫn giữa các công ty

---

## 3. Quyết Định Thiết Kế (Design Decision)

### Nguyên tắc áp dụng: **Single Point of Truth tại tầng Domain**

Trong **Clean Architecture**, logic nghiệp vụ của một Entity phải nằm trong chính Entity đó, không nằm rải rác ở Controller hay Service.

> **Câu hỏi cốt lõi:** "Tôi đang thuộc tổ chức nào?" là câu hỏi của **User Entity**, không phải của Controller.

### Giải pháp: Bổ sung Getter vào `User` Domain Entity

```typescript
// src/modules/user/domain/entities/user.entity.ts

/**
 * Lấy ID Tổ chức hiện tại của người dùng.
 * Tự động xử lý cả hai trường hợp:
 * - Nhân viên (Employee): lấy từ profileContext.employee.organizationId
 * - Chủ tổ chức (Owner): lấy từ profileContext.organization.id
 */
get organizationId(): number | undefined {
  return this._profileContext.employee?.organizationId 
      || this._profileContext.organization?.id;
}

/**
 * Kiểm tra xem người dùng có phải là nhân sự nội bộ (Consultant/Internal) không.
 * Internal user có thể xem dữ liệu của nhiều tổ chức khác nhau.
 */
get isInternal(): boolean {
  return !!(this._profileContext.employee?.isInternal 
         || this._profileContext.organization?.isInternal);
}
```

### Tại sao KHÔNG đặt logic này ở Service/Controller?

| Tiêu chí | Đặt ở Controller | Đặt ở Entity (✅ chọn) |
|---------|-----------------|----------------------|
| Tái sử dụng | ❌ Mỗi nơi tự viết lại | ✅ Viết 1 lần, dùng mọi nơi |
| Khả năng sai sót | ❌ Cao (quên case Organization) | ✅ Thấp (logic tập trung) |
| Khả năng mở rộng | ❌ Phải sửa nhiều file | ✅ Chỉ sửa Entity |
| Testability | ❌ Phải mock context phức tạp | ✅ Test Entity trực tiếp |
| Clean Architecture | ❌ Vi phạm (logic domain ở Infrastructure) | ✅ Tuân thủ |

---

## 4. Các Thay Đổi Thực Hiện

### 4.1 Tầng Domain — `User` Entity
- Thêm getter `organizationId`: Tự động ưu tiên Employee context, fallback về Organization context
- Thêm getter `isInternal`: Gộp logic kiểm tra hai loại internal flag

### 4.2 Tầng Infrastructure — JWT Payload
- Cập nhật `JwtPayload` type: Thêm `orgId?: number`
- Cập nhật `AuthenticationService.login()`: Đính kèm `orgId: user.organizationId` vào Token
- Cập nhật `AuthenticationService.register()`: Tương tự
- Cập nhật `AuthenticationService.refreshToken()`: Tương tự
- Cập nhật `DrizzleUserRepository.findByUsername()`: Load đầy đủ `employeeProfile` và `organizationProfile` để Mapper có đủ dữ liệu

### 4.3 Tầng Infrastructure — Controllers (Refactor)
Thay toàn bộ các pattern thủ công thành `user.organizationId`:

```typescript
// TRƯỚC:
const orgId = user.profileContext?.employee?.organizationId;

// SAU:
const orgId = user.organizationId;
```

Files được refactor:
- `hrm-master-data.controller.ts`
- `org-structure.controller.ts`
- `employee.controller.ts` (đồng thời xóa fallback nguy hiểm `|| 1`)
- `company-import.controller.ts`

### 4.4 Tầng Application — Services (Refactor)
- `lead-query.service.ts`: Đổi kiểu tham số từ `any` → `User`, sử dụng `user.organizationId` và `user.isInternal`

### 4.5 Unit Tests
- `lead-query.service.spec.ts`: Cập nhật để tạo `User` instance thật thay vì dùng object literal giả

---

## 5. Kết Quả và Lợi Ích

### Khả năng mở rộng trong tương lai
Nếu sau này cần hỗ trợ thêm loại user thứ ba (VD: Học viên thuộc một Tổ chức đào tạo), chỉ cần cập nhật **duy nhất** getter `organizationId` trong `User` entity. Toàn bộ hệ thống sẽ tự động hoạt động đúng mà không cần sửa từng Controller/Service.

### Bảo mật được tăng cường
- Xóa bỏ hardcode fallback `|| 1` nguy hiểm trong `employee.controller.ts`
- Logic Multi-tenancy isolation giờ nhất quán và đáng tin cậy hơn

---

## 6. Commits Liên Quan
- `a35c72e2` — `feat: include organization context in JWT payload and user entity profiles`
- (Staged, chưa commit) — Refactor controllers và services

## 7. Tham Khảo
- [Clean Architecture - Robert C. Martin] — Domain Entity chứa logic nghiệp vụ
- [Tell, Don't Ask Principle] — Entity tự biết "mình thuộc tổ chức nào" thay vì để code bên ngoài tự đi lấy
