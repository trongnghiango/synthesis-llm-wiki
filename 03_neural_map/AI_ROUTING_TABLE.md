# 🧠 BẢN ĐỒ PHÂN LUỒNG NƠ-RON AI (STAX AI NEURAL ROUTING MAP)

> **DÀNH CHO AI AGENTS:** Tệp tin này là cổng định tuyến ngữ cảnh siêu nhẹ. Không đọc toàn bộ Knowledge Base. Quét bảng này để tìm đúng nốt nghiệp vụ nghiệp vụ cần thiết và mở đúng đường dẫn đó.

---

## 🚦 ĐỊNH HƯỚNG TÌM KIẾM THEO NHU CẦU (USE CASE ROUTING PATHS)

Khi bạn nhận được yêu cầu từ lập trình viên, hãy ánh xạ mục tiêu công việc sang các đường dẫn dưới đây:

### 🏗️ 1. Thiết kế Module mới, Tổ chức Folder & Import
*   *Mục tiêu:* Tạo folder mới, định nghĩa boundaries, export API hoặc cấu trúc NestJS.
*   **Nốt cần đọc:**
    *   `[[arch-modular-monolith-tiers]]` — Đường dẫn: [02_atomic_nodes/arch-modular-monolith-tiers.md](../02_atomic_nodes/arch-modular-monolith-tiers.md)
    *   `[[arch-clean-boundaries]]` — Đường dẫn: [02_atomic_nodes/arch-clean-boundaries.md](../02_atomic_nodes/arch-clean-boundaries.md)
    *   `[[std-naming-rules]]` — Đường dẫn: [02_atomic_nodes/std-naming-rules.md](../02_atomic_nodes/std-naming-rules.md)
    *   `[[std-import-boundaries]]` — Đường dẫn: [02_atomic_nodes/std-import-boundaries.md](../02_atomic_nodes/std-import-boundaries.md)

### 💾 2. Làm việc với Cơ sở dữ liệu & Giao dịch (Database & Transactions)
*   *Mục tiêu:* Tạo bảng schema mới, viết Drizzle query, kiểm soát transaction chéo, hoặc filter theo Tenant.
*   **Nốt cần đọc:**
    *   `[[arch-als-tenant-isolation]]` — Đường dẫn: [02_atomic_nodes/arch-als-tenant-isolation.md](../02_atomic_nodes/arch-als-tenant-isolation.md)
    *   `[[arch-als-transactions]]` — Đường dẫn: [02_atomic_nodes/arch-als-transactions.md](../02_atomic_nodes/arch-als-transactions.md)
    *   `[[hb-drizzle-base-repo]]` — Đường dẫn: [02_atomic_nodes/hb-drizzle-base-repo.md](../02_atomic_nodes/hb-drizzle-base-repo.md)

### 🔐 3. Xác thực, Phân quyền & Request Flow
*   *Mục tiêu:* Kiểm tra quyền API, cấu hình RBAC, bẫy Exception, hoặc điều khiển Request Flow.
*   **Nốt cần đọc:**
    *   `[[arch-exception-handling]]` — Đường dẫn: [02_atomic_nodes/arch-exception-handling.md](../02_atomic_nodes/arch-exception-handling.md)
    *   `[[hb-rbac-permissions]]` — Đường dẫn: [02_atomic_nodes/hb-rbac-permissions.md](../02_atomic_nodes/hb-rbac-permissions.md)
    *   `[[hb-http-request-flow]]` — Đường dẫn: [02_atomic_nodes/hb-http-request-flow.md](../02_atomic_nodes/hb-http-request-flow.md)

### 📜 4. Logging & Kiểm toán nghiệp vụ (Audit Logging)
*   *Mục tiêu:* Ghi log thay đổi dữ liệu nghiệp vụ, tính toán Delta Diff.
*   **Nốt cần đọc:**
    *   `[[hb-delta-logging]]` — Đường dẫn: [02_atomic_nodes/hb-delta-logging.md](../02_atomic_nodes/hb-delta-logging.md)

### 📦 5. Xử lý logic Nghiệp vụ Core (HRM / CRM / Accounting)
*   *Mục tiêu:* Code logic liên quan đến nhân sự, sơ đồ tổ chức, cơ hội bán hàng Kanban, phiếu thu/chi dòng tiền, sổ quỹ.
*   **Nốt cần đọc:**
    *   `[[dom-hrm-position-model]]` — Đường dẫn: [02_atomic_nodes/dom-hrm-position-model.md](../02_atomic_nodes/dom-hrm-position-model.md)
    *   `[[dom-accounting-finote]]` — Đường dẫn: [02_atomic_nodes/dom-accounting-finote.md](../02_atomic_nodes/dom-accounting-finote.md)
    *   `[[dom-crm-pipelines]]` — Đường dẫn: [02_atomic_nodes/dom-crm-pipelines.md](../02_atomic_nodes/dom-crm-pipelines.md)

### 🤝 6. Giao tiếp Backend ↔ Frontend
*   *Mục tiêu:* Viết Zod Schema, DTO dùng chung hoặc thiết kế API contract.
*   **Nốt cần đọc:**
    *   `[[std-api-contracts]]` — Đường dẫn: [02_atomic_nodes/std-api-contracts.md](../02_atomic_nodes/std-api-contracts.md)

---

## 🕸️ CHỈ MỤC TỪ KHÓA ĐỂ GREP NHANH (SEMANTIC TAGS INDEX)

*   `#architecture` -> [[arch-modular-monolith-tiers]], [[arch-clean-boundaries]], [[arch-als-tenant-isolation]], [[arch-als-transactions]], [[arch-exception-handling]]
*   `#standards` -> [[std-naming-rules]], [[std-import-boundaries]], [[std-api-contracts]], [[std-team-workflow]]
*   `#handbooks` -> [[hb-drizzle-base-repo]], [[hb-delta-logging]], [[hb-rbac-permissions]], [[hb-http-request-flow]]
*   `#domain` -> [[dom-hrm-position-model]], [[dom-accounting-finote]], [[dom-crm-pipelines]]

---
*Cổng định tuyến tối ưu được thiết kế bởi Antigravity AI.*
