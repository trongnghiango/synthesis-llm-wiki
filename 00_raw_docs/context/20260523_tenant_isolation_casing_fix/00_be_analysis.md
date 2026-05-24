# Analysis: Tenant Isolation Casing and Fallback Fixes

**Ngày phân tích:** 2026-05-23
**Handoff Plan:** `lively-crafting-trinket.md`
**Chế độ:** Handoff của Backend (`stax-backend`)

---

## 1. Phân loại Module & Tiêu chuẩn
Nhiệm vụ này ảnh hưởng trực tiếp đến 2 phân khu lớn trong hệ thống `STAX_ASP`:
1. **User/Auth Module (Tier 2 - Domain Core):** Sửa lỗi casing trong `VisibilityResolverService.ts` để khôi phục cơ chế phân giải tầm nhìn (`scope`) chính xác cho các vai trò quản trị hệ thống (`ADMIN`, `SUPER_ADMIN`, `MANAGER`).
2. **CRM Module (Tier 3 - Process Flow):** Siết chặt Tenant Isolation ở lớp Presentation/Controller và Persistence/Repository, loại bỏ hoàn toàn fallback nguy hiểm `|| 1` cho người dùng bên ngoài, đồng thời tích hợp `applyTenantIsolation` vào repository để tự động lọc dữ liệu.

---

## 2. Bounded Context & Ubiquitous Language

| Nghiệp vụ | Khái niệm kỹ thuật | Định danh & Ranh giới |
| :--- | :--- | :--- |
| Tổ chức / Khách thuê | `Organization` | `organizationId`: Multi-tenancy context boundary. Giá trị `1` đại diện cho Công ty chủ quản (Platform Owner - STAX). |
| Người dùng | `User` | `userId`: Login/Identity credentials only. |
| Người dùng bên ngoài | `External User` | Người dùng thuộc doanh nghiệp khách hàng (`organizationId > 1`). |
| Người dùng nội bộ | `Internal Staff` | Nhân sự thuộc STAX (`organizationId === 1` hoặc `isInternal === true`). |
| Phạm vi tầm nhìn | `Visibility Scope` | `ALL` (Xem toàn hệ thống), `OWN_ORG` (Xem tổ chức mình), `ASSIGNED_ONLY` (Chỉ xem bản ghi được gán). |

---

## 3. Data Flow & API Design

### A. Phân giải Quyền & Tầm nhìn (Visibility Resolution)
Khi người dùng thực hiện yêu cầu, `VisibilityResolverService` quét qua các role của người dùng để xác định `scope` của họ. Lỗi casing (so sánh chữ thường `admin`, `manager` với DB Role `ADMIN`, `MANAGER`) làm cho toàn bộ admin/manager bị rơi vào fallback `ASSIGNED_ONLY`.
- **Luồng sửa đổi:** Chuyển đổi toàn bộ roles sang UPPERCASE trước khi so sánh.

### B. CRM Controllers - Upload Attachment & Queries
Tại `ContractController`, `QuoteController`, `LeadController`, `OrganizationController`:
- **Trước đây:** `const tenantId = user?.organizationId || 1;`
  - *Rủi ro:* Nếu `user.organizationId` là `undefined` (do lỗi nạp profile hoặc token không đầy đủ), họ sẽ nhận được quyền truy cập vào tổ chức `1` (Platform Owner).
- **Thiết kế mới (An toàn hơn):**
  - Đối với các yêu cầu chỉnh sửa/truy xuất liên quan đến CRM (`ContractController`):
    - Kiểm tra xem người dùng có phải là `SUPER_ADMIN` hoặc `Platform Leader` (thuộc Org 1 và có role phù hợp) hay không.
    - Nếu đúng, `tenantId = 1`.
    - Nếu không phải và thiếu `organizationId`, ném ngay `ForbiddenException` ("Không tìm thấy thông tin tổ chức hợp lệ.").
  - Đối với các file đính kèm/upload (`Quote`, `Lead`, `Organization`):
    - Kiểm tra `user.isInternal === true`. Nếu đúng, cho phép fallback về `1` (thư mục hệ thống của STAX).
    - Nếu không phải và thiếu `organizationId`, ném ngay `ForbiddenException` ("Tài khoản không thuộc về bất kỳ doanh nghiệp nào để tải lên.").

### C. Repository Tenant Isolation (`DrizzleContractRepository`)
- **Trước đây:** Lọc thủ công `orgId` hoặc kiểm tra điều kiện `orgId > 1`.
- **Thiết kế mới:** Tích hợp `this.applyTenantIsolation(conditions, schema.contracts)` kế thừa từ `DrizzleBaseRepository` nhằm tận dụng cơ chế lọc tự động dựa trên `scope` được phân giải từ ALS/JWT.

---

## 4. Multi-tenancy & Security (The Core Guardrails)
- **Tenant Isolation:** Tuyệt đối không cho phép query dữ liệu chéo tổ chức. Đối với tài khoản Platform Owner (Org ID 1) có `scope: 'ALL'`, `applyTenantIsolation` sẽ tự động bỏ qua mệnh đề lọc `organizationId` để họ có thể quản lý, đúng như yêu cầu của người dùng.
- **Exception Safety:** Việc ném `ForbiddenException` ở lớp Controller là hoàn toàn hợp lệ theo Hiến pháp STAX (chỉ cấm ném NestJS exception ở tầng Domain/Application).

---

Vui lòng gõ 'OK' để tôi tiến hành thiết kế kiến trúc chi tiết.
