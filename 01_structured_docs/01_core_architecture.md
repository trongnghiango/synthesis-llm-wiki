# 🏗️ KIẾN TRÚC CỐT LÕI STAX (STAX CORE ARCHITECTURE)

Tài liệu này hệ thống hóa toàn bộ các quyết định kiến trúc, ranh giới cấu trúc và chiến lược dữ liệu chuẩn của dự án STAX. Đây là nguồn sự thật duy nhất (Single Source of Truth) định hình thiết kế hệ thống.

---

## 1. PHÂN CẤP MODULE (TIERED SYSTEM)

Để quản lý độ phức tạp nghiệp vụ và ngăn ngừa lỗi phụ thuộc vòng (Circular Dependency), hệ thống phân cấp các module theo 3 tầng (Tiers) có tính độc lập giảm dần:

| Cấp độ | Tên Tầng | Đặc điểm & Trách nhiệm | Ví dụ Module |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Foundation** | Hạ tầng kỹ thuật lõi, hoàn toàn độc lập với nghiệp vụ doanh nghiệp. | `Rbac`, `Notification`, `AuditLog`, `Storage` |
| **Tier 2** | **Domain Core** | Dòng máu nghiệp vụ và dữ liệu xương sống của doanh nghiệp. | `User`, `OrgStructure`, `Employee` |
| **Tier 3** | **Process Flow** | Các quy trình nghiệp vụ biến động linh hoạt và dòng tiền. | `CRM`, `Accounting`, `Contracts` |

### 🚨 Nguyên tắc cô lập tầng bất di bất dịch (Tier Isolation Rules)
1. **Chiều phụ thuộc:** Tầng dưới tuyệt đối không được biết và phụ thuộc vào tầng trên (e.g., Tier 2 cấm import bất kỳ file nào từ Tier 3).
2. **Giao tiếp chéo module:** Giao tiếp giữa các module ngang hàng hoặc chéo tầng bắt buộc phải đi qua **Ports (Interfaces)** được định nghĩa sẵn, hoặc thông qua **Domain Events** được phát qua hệ thống `IEventBus`.

---

## 2. 4 LỚP BẢO VỆ CLEAN ARCHITECTURE (HEXAGONAL)

Mỗi module nghiệp vụ (Bounded Context) tuân thủ mô hình Clean Architecture nghiêm ngặt với 4 lớp bảo vệ từ trong ra ngoài:

```
┌─────────────────────────────────────────────────────────┐
│ Presentation Layer (Controllers, DTOs, Swagger, Guards)  │
│    └─► Application Layer (Use Cases, Transaction Mgmt)  │
│         └─► Domain Layer (Rich Entities, Ports, Events)  │
│              ▲                                          │
│              └─ Infrastructure Layer (Drizzle, Mappers) │
└─────────────────────────────────────────────────────────┘
```

### 1) Lớp Domain (Domain Layer - `domain/`) - *Trái tim hệ thống*
*   **Thành phần:** Rich Domain Entities, Value Objects, Domain Events (`IAuditableEvent`), Repository Interfaces (Ports).
*   **Quy tắc thuần khiết (Domain Purity):** Tuyệt đối **không** import NestJS, Drizzle-ORM, TypeORM, hay bất kỳ thư viện hạ tầng nào trong thư mục này. Chỉ sử dụng TypeScript thuần.
*   **Rich Domain Entity:** Entity phải đóng gói các quy tắc nghiệp vụ bất biến (Business Invariants). Không thiết kế Entity dạng "Anemic" (chỉ chứa getter/setter rỗng).

### 2) Lớp Ứng dụng (Application Layer - `application/`) - *Bộ điều phối*
*   **Thành phần:** Use Cases, Application Services, Transaction Management.
*   **Trách nhiệm:** Nhận yêu cầu, điều phối các Domain Entity thực hiện nghiệp vụ, kiểm soát ranh giới giao dịch (Transaction Boundary) qua `ITransactionManager` sử dụng Async Local Storage.
*   **Bảo vệ lỗi:** Cấm ném các Exception của framework (`BadRequestException`, `NotFoundException`) ở đây. Bắt buộc ném `BusinessRuleValidationException` hoặc `EntityNotFoundException`.

### 3) Lớp Hạ tầng (Infrastructure Layer - `infrastructure/`) - *Cánh tay thực thi*
*   **Thành phần:** Repositories triển khai (Adapters) thừa kế từ `DrizzleBaseRepository`, DB schemas (`pgTable`), Mappers (`toDomain` ↔ `toPersistence`), External API integrations.
*   **Trách nhiệm:** Hiện thực hóa các Repository Interfaces từ lớp Domain. Thực thi ánh xạ dữ liệu độc lập hoàn toàn khỏi nghiệp vụ thông qua Mapper.

### 4) Lớp Trình diễn (Presentation Layer) - *Cổng giao tiếp*
*   **Thành phần:** NestJS Controllers, Request/Response DTOs, Swagger annotations, Guards kiểm tra quyền.
*   **Trách nhiệm:** Đón nhận request, validate DTO thô qua class-validator/Zod, kiểm tra sơ bộ RBAC, định tuyến luồng chạy vào Use Cases.

---

## 3. CHIẾN LƯỢC ĐA DOANH NGHIỆP & CÔ LẬP DỮ LIỆU (MULTI-TENANCY)

STAX thực thi kiến trúc **Shared Database, Isolated Schema** (Logic-based isolation) để phục vụ hàng ngàn Tenant (Doanh nghiệp) trên cùng một tài nguyên vật lý.

### 🔑 Quản trị Context qua Async Local Storage (ALS)
*   **Cơ chế:** Khi request đi qua middleware xác thực (JWT/Session), hệ thống sẽ lưu `organizationId` của người dùng vào Async Local Storage.
*   **Tự động hóa Scoping:** Các query của Repository sẽ tự động đọc `organizationId` từ ALS và đưa vào mệnh đề `where` của SQL, giảm thiểu tối đa rủi ro quên lọc Tenant thủ công gây rò rỉ dữ liệu.
*   **Khóa duy nhất (Uniqueness):** Các trường định danh nghiệp vụ (Mã code, Mã số thuế) được thiết lập Unique Index phức hợp bắt buộc chứa `organizationId`:
    ```typescript
    uniqueIndex('idx_org_code').on(table.organizationId, table.code)
    ```

---

## 4. CHIẾN LƯỢC DỮ LIỆU & GIAO DỊCH AN TOÀN

### ⚡ Quản lý Giao dịch Tự động (ALS-driven Transactions)
*   Tầng Application điều khiển transactional boundaries một cách ngầm định qua `ITransactionManager.runInTransaction(...)`.
*   Giao dịch được propagation ngầm định giữa các Repository gọi trong cùng một luồng ALS nhờ vào Transaction Manager Adapter.

### 📜 Delta Logging & Audit Log phi tập trung
*   **Audit Logging:** Không lưu thông tin thô. Hệ thống ghi nhận biến động qua mô hình **Delta Logging** (chỉ lưu các trường có sự thay đổi kèm giá trị trước/sau).
*   **Performance:** Quá trình ghi Audit Log và gửi Notifications phải được chạy dưới dạng **Fire-and-Forget** (`catch` lỗi tại chỗ) bên ngoài luồng giao dịch cơ sở dữ liệu chính để tránh block luồng write chính.

---

## 5. BẢO MẬT LAI 3 LỚP (HYBRID SECURITY)

Hệ thống bảo vệ dữ liệu bằng cơ chế phòng thủ 3 tầng:

1.  **Tầng Kiểm soát Ngoại vi (Presentation Guard):** Dùng RBAC Guard để chặn thô dựa trên Permissions từ Token (e.g., `crm:leads:create`).
2.  **Tầng Kiểm soát Dữ liệu (Repository Isolation):** Repository tự động inject điều kiện lọc `organizationId` từ ALS.
3.  **Tầng Giao diện (DTO Action Masking):** API trả về DTO chứa mảng `_actions` (ví dụ: `['edit', 'delete']`) được tính toán dựa trên quyền hạn và trạng thái bản ghi. Frontend dựa vào mảng này để hiển thị UI tương ứng, đảm bảo an toàn tuyệt đối.

---
*Định nghĩa bởi Antigravity AI — Sẵn sàng cho việc bóc tách sang Micro-services.*
