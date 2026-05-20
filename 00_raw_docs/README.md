# 📚 STAX — Knowledge Base

> **Dự án:** ERP/HRM/CRM Enterprise cho doanh nghiệp dịch vụ
> **Stack:** NestJS + Drizzle ORM + PostgreSQL + Clean Architecture + DDD
> **Cập nhật:** 2026-05-21

---

## 🗺️ Điều hướng nhanh (Quick Navigation)

| Tôi muốn biết về... | Đọc ở đây |
| :--- | :--- |
| **Hiến pháp (Quy tắc bất di bất dịch)** | [governance/constitution.md (Hiến pháp)](./standards/architecture_rules.md) |
| **Kiến trúc tổng thể (Modular Monolith, Clean Arch)** | [architecture/01_ARCHITECTURE.md](./architecture/01_ARCHITECTURE.md) |
| **Quy tắc code bắt buộc (Transaction, Exceptions, ALS)** | [architecture/02_CODE_GOVERNANCE.md](./architecture/02_CODE_GOVERNANCE.md) |
| **Chiến lược Cơ sở Dữ liệu & Isolation** | [architecture/03_DATA_STRATEGY.md](./architecture/03_DATA_STRATEGY.md) |
| **Thiết kế Domain (HRM & CRM)** | [architecture/04_DOMAIN_DESIGN.md](./architecture/04_DOMAIN_DESIGN.md) |
| **Quy chuẩn đặt tên và API contracts** | [standards/INDEX.md](./standards/INDEX.md) |
| **Hướng dẫn kỹ thuật chuyên sâu (Logging, ORM)** | [handbooks/INDEX.md](./handbooks/INDEX.md) |
| **Lịch sử các phiên làm việc (History)** | [STAX/history/README.md](./STAX/history/README.md) |

---

## 🌳 Cây Tài liệu (Knowledge Tree)

📁 **architecture/** — Kiến trúc tổng thể hệ thống
├── 📄 [01_ARCHITECTURE.md](./architecture/01_ARCHITECTURE.md) — Tier System và Clean Architecture 4 lớp.
├── 📄 [02_CODE_GOVERNANCE.md](./architecture/02_CODE_GOVERNANCE.md) — Exception patterns, Transaction rules.
├── 📄 [03_DATA_STRATEGY.md](./architecture/03_DATA_STRATEGY.md) — Drizzle ORM, Tenant Isolation, ALS.
├── 📄 [04_DOMAIN_DESIGN.md](./architecture/04_DOMAIN_DESIGN.md) — Rich Domain Model, Position-based HRM.
├── 📄 [05_DEVELOPER_GUIDE.md](./architecture/05_DEVELOPER_GUIDE.md) — Setup môi trường, lệnh dev.
└── 📁 [adr/](./architecture/adr/INDEX.md) — Chỉ mục và danh sách quyết định kiến trúc (ADR-001 đến ADR-011).

📁 **standards/** — Quy chuẩn & Quy tắc phát triển
├── 📄 [api_contracts.md](./standards/api_contracts.md) — Cấu trúc API contracts dùng Zod.
├── 📄 [architecture_rules.md](./standards/architecture_rules.md) — Ranh giới các lớp trong Clean Arch.
├── 📄 [import_boundaries.md](./standards/import_boundaries.md) — Quy tắc module boundary.
├── 📄 [naming_conventions.md](./standards/naming_conventions.md) — Quy định đặt tên files, db schema.
├── 📄 [team_workflow.md](./standards/team_workflow.md) — Quy trình quản lý context và history.
└── 📄 [ui_components.md](./standards/ui_components.md) — Quy chuẩn components & UI state FE.

📁 **handbooks/** — Sổ tay thực thi kỹ thuật
├── 📄 [clean-architecture-handbook-v2.md](./handbooks/clean-architecture-handbook-v2.md) — Hướng dẫn Clean Arch chi tiết.
├── 📄 [orm-mapping.md](./handbooks/orm-mapping.md) — Kỹ thuật Drizzle ORM Mapping FlatleftrightarrowNested.
├── 📄 [logging.md](./handbooks/logging.md) — Winston Logger Adapter & Audit Logging.
├── 📄 [permissions.md](./handbooks/permissions.md) — Phân quyền RBAC & Import/Export CSV.
├── 📄 [request-flow.md](./handbooks/request-flow.md) — Luồng đi của 1 HTTP Request qua Guards/Pipes.
├── 📄 [api-documentation.md](./handbooks/api-documentation.md) — Tài liệu tích hợp API.
└── 📄 [cac-buoc-refactoring.md](./handbooks/cac-buoc-refactoring.md) — Sổ tay tái cấu trúc code vi phạm.

📁 **domain/** — Tài liệu quy trình nghiệp vụ & Domain Knowledge
├── 📄 [Quy trình cung cấp dịch vụ kế toán thuế trọn gói.docx.md](./domain/Quy%20trình%20cung%20cấp%20dịch%20vụ%20kế%20toán%20thuế%20trọn%20gói.docx.md) — Nghiệp vụ Kế toán thuế.
└── 📄 [crm_accounting_status_report.md](./domain/crm_accounting_status_report.md) — Báo cáo tích hợp luồng CRM & Kế toán.

📁 **_legacy/** — Tài liệu lưu trữ lịch sử
└── Hướng dẫn và các bản thảo thiết kế HRM/ERP cũ không còn canonical.

---

## 🚀 Lộ trình Onboarding (Cho Thành viên mới)

1. [architecture/01_ARCHITECTURE.md](./architecture/01_ARCHITECTURE.md) — Hiểu tổng quan cấu trúc hệ thống (15 phút).
2. [standards/architecture_rules.md](./standards/architecture_rules.md) — Các quy tắc cốt lõi không được vi phạm (10 phút).
3. [architecture/02_CODE_GOVERNANCE.md](./architecture/02_CODE_GOVERNANCE.md) — Tiêu chuẩn viết code nghiệp vụ (20 phút).
4. [architecture/05_DEVELOPER_GUIDE.md](./architecture/05_DEVELOPER_GUIDE.md) — Cách thiết lập môi trường và chạy thử nghiệm.
