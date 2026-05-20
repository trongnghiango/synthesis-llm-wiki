# 🏗️ KIẾN TRÚC TỔNG THỂ (STAX ARCHITECTURE)

Hệ thống STAX được thiết kế theo mô hình **Modular Monolith** chuẩn mực, sẵn sàng bóc tách thành Microservices khi cần. Kiến trúc cốt lõi dựa trên 3 trụ cột: **Clean Architecture**, **Domain-Driven Design (DDD)**, và **Multi-tenant Data Isolation**.

## 1. PHÂN TẦNG MODULE (TIERED SYSTEM)

Để quản lý độ phức tạp và ngăn chặn phụ thuộc vòng (Circular Dependency), STAX phân cấp các module theo "độ sâu" nghiệp vụ:

| Cấp độ | Tên | Đặc điểm | Ví dụ |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Foundation** | Hạ tầng dùng chung, không chứa logic nghiệp vụ. | `Rbac`, `Notification`, `AuditLog`, `Storage` |
| **Tier 2** | **Domain Core** | Nguồn sự thật (DNA) và vận hành xương sống. | `User`, `OrgStructure`, `Employee` |
| **Tier 3** | **Process Flow** | Dòng chảy nghiệp vụ và tiền bạc (Flow). Phụ thuộc Tier 2. | `CRM`, `Accounting`, `Contracts` |

> [!IMPORTANT]
> **Nguyên tắc Cô lập:** Tier 2 KHÔNG được phụ thuộc vào Tier 3. Giao tiếp chéo module (Cross-module) phải thông qua **Ports (Interfaces)** hoặc **Domain Events (EventBus)**.

---

## 2. CLEAN ARCHITECTURE (HEXAGONAL)

Mỗi module nghiệp vụ (Bounded Context) được chia thành 4 lớp bảo vệ:

1.  **Domain Layer (Inner Circle):**
    *   Chứa **Rich Domain Models** (Entities) với các quy tắc nghiệp vụ bất biến (Invariants).
    *   Chứa **Domain Events** (Sự kiện nghiệp vụ).
    *   Chứa **Repository Interfaces** (Ports).
    *   *Ràng buộc:* Tuyệt đối không import thư viện bên ngoài (NestJS, Drizzle).

2.  **Application Layer (Use Cases):**
    *   Điều phối luồng công việc (Orchestration).
    *   Sử dụng **Transaction Manager** (ALS) để đảm bảo tính nguyên tử.
    *   Sử dụng **Domain Exceptions** để báo lỗi (không dùng HTTP Errors).

3.  **Infrastructure Layer (Adapters):**
    *   Thực thi việc lưu trữ dữ liệu (Drizzle Repositories).
    *   Giao tiếp với các bên thứ 3 (Email, PDF Generator).
    *   Chuyển đổi dữ liệu (Mappers) giữa DB Record và Domain Entity.

4.  **Presentation Layer:**
    *   Controllers, DTOs, và Swagger Documentation.
    *   Thực thi bảo mật bằng Guards và Decorators.

---

## 3. CHIẾN LƯỢC ĐA DOANH NGHIỆP (MULTI-TENANCY)

STAX sử dụng mô hình **Shared Database, Isolated Schema** (Logic-based isolation).

*   **Organization-Centric:** Bảng `organizations` là gốc của mọi dữ liệu. Cờ `is_internal` phân biệt giữa STAX (Admin) và Khách hàng (Tenants).
*   **Automatic Scoping:** 
    *   Mọi query tại tầng Repository BẮT BUỘC phải lọc theo `organization_id`.
    *   Sử dụng **Async Local Storage (ALS)** để tự động nhận diện `organization_id` của User đang đăng nhập, giảm thiểu việc truyền tham số thủ công.
*   **Uniqueness Scoped:** Các mã định danh (Code, TaxCode) được đánh Unique Index phức hợp: `uniqueIndex(['organization_id', 'code'])`.

---

## 4. BẢO MẬT LAI 3 LỚP (HYBRID SECURITY)

1.  **Lớp 1 (Guard):** Chặn thô tại Controller bằng RBAC Permissions (Ví dụ: `crm:leads:read`).
2.  **Lớp 2 (Data Filter):** Repository tự động lọc dữ liệu theo `organization_id` (Tenant Isolation) và `owner_id` (nếu cần).
3.  **Lớp 3 (DTO Actions):** Backend tính toán trạng thái và trả về mảng `_actions` cho Frontend. Giao diện sẽ tự động ẩn/hiện nút dựa trên mảng này.

---
*Cập nhật ngày 08/05/2026 bởi Antigravity AI.*
