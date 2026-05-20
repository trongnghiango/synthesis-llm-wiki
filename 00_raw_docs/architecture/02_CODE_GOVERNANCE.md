# 🛑 QUY TẮC QUẢN TRỊ MÃ NGUỒN (CODE GOVERNANCE)

Để duy trì hệ thống ổn định và sạch sẽ, mọi lập trình viên tại STAX phải tuân thủ nghiêm ngặt bộ quy tắc dưới đây.

## 1. QUY TẮC TRANSACTION (ALS PATTERN)

STAX sử dụng **Async Local Storage (ALS)** để quản lý Transaction mà không làm "bẩn" signature của hàm.

*   **BẮT BUỘC:** Sử dụng `TransactionManager` để bọc các tác vụ đa thực thể.
*   **KHÔNG ĐƯỢC:** Truyền biến `tx` (transaction object) xuyên qua các tầng Service.
*   **VÍ DỤ:**
    ```typescript
    return this.txManager.runInTransaction(async () => {
        await this.leadRepo.save(lead);
        await this.contractRepo.create(contract);
    });
    ```

---

## 2. QUY TẮC XỬ LÝ LỖI (DOMAIN EXCEPTIONS)

Theo **ADR 010**, tuyệt đối không để logic nghiệp vụ phụ thuộc vào Framework (NestJS).

*   **BẮT BUỘC:** Sử dụng các Exception nằm trong `@core/shared/domain/exceptions`.
    *   `EntityNotFoundException`: Khi không tìm thấy dữ liệu.
    *   `BusinessRuleValidationException`: Khi vi phạm quy tắc nghiệp vụ.
*   **CẤM:** Ném `BadRequestException` hoặc `NotFoundException` bên trong Tầng Domain/Application.

---

## 3. QUY TẮC ĐẶT TÊN (NAMING CONVENTIONS)

### A. Database (Snake Case)
*   Table: `organizations`, `employee_tasks` (số nhiều).
*   Primary Key: `id`.
*   Foreign Key: `organization_id` (tên bảng số ít + `_id`).
*   Indexes: `idx_tên_bảng_tên_cột`.

### B. TypeScript (Camel Case)
*   Variables/Methods: `createContract`, `organizationId`.
*   Classes/Interfaces: `LeadService`, `ILeadRepository`.
*   **Port/Interface Pattern:** Token và Interface phải có cùng tên để tối ưu Dependency Injection.
    ```typescript
    export const IUserRepository = Symbol('IUserRepository');
    export interface IUserRepository { ... }
    ```

---

## 4. QUY TẮC TESTING (SQL-DRIVEN)

Chúng ta không mock các hàm SQL (fluent API) vì nó làm mất đi ý nghĩa của việc test dữ liệu.

*   **BẮT BUỘC:** Sử dụng `@electric-sql/pglite` cho Integration Test.
*   **LỢI ÍCH:** Chạy một engine Postgres thực thụ (WASM) trong memory, hỗ trợ đầy đủ các tính năng nâng cao của Drizzle (Relational Queries, Lateral Joins).
*   **LỆNH CHẠY:** `NODE_OPTIONS=--experimental-vm-modules npx jest`.

---

## 5. QUY TẮC MAPPING & ENCAPSULATION

*   **Rich Domain Model:** Các thuộc tính quan trọng của Entity (như `status`) phải là `private`. Chỉ thay đổi qua các phương thức nghiệp vụ.
*   **Mappers:** Luôn sử dụng lớp Mapper để chuyển đổi dữ liệu khi đi vào/ra khỏi hệ thống. Tuyệt đối không trả về raw database record trực tiếp lên giao diện.

---
*Cập nhật ngày 08/05/2026 bởi Antigravity AI.*
