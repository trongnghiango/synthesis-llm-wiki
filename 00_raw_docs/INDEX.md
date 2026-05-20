---
title: "STAX Knowledge Tree"
summary: "Trạm điều hướng trung tâm cho toàn bộ tri thức dự án STAX"
description: |
  Đây là điểm bắt đầu duy nhất để tìm kiếm mọi thông tin về Tầm nhìn,
  Kiến trúc, Quy chuẩn và Nghiệp vụ của dự án STAX.
  Được thiết kế tối ưu cho AI Agent và Developer.
last_updated: "2026-05-21"
---

# 🌳 STAX Knowledge Tree — Bản đồ Tri thức

Chào mừng bạn đến với nguồn sự thật duy nhất của STAX. Tài liệu này được tổ chức theo cấu trúc cây phân tầng để giúp bạn tìm thấy thông tin cần thiết trong tối đa 2 bước.

---

## 🗺️ Điều hướng nhanh (Quick Links)

| Tôi muốn tìm... | Đọc ở đây |
| :--- | :--- |
| **Quy tắc bất di bất dịch** | [🏰 Constitution / Architecture Rules](./standards/architecture_rules.md) |
| **Cách tổ chức code** | [🧠 Architecture Overview](./architecture/01_ARCHITECTURE.md) |
| **Quy tắc coding & standards** | [📝 Governance & Code Standards](./architecture/02_CODE_GOVERNANCE.md) |
| **Hướng dẫn Coding / ORM / Logging** | [📚 Developer Handbooks](./handbooks/INDEX.md) |
| **Chi tiết nghiệp vụ (HRM/CRM/Accounting)** | [📦 Domain Knowledge](./domain/INDEX.md) |
| **Lịch sử phát triển** | [🕰️ Lịch sử các phiên làm việc (History)](./STAX/history/README.md) |

---

## 🌳 Cây Tài liệu (Knowledge Tree)

### 1. 🏗️ [Architecture & Infrastructure](./architecture/INDEX.md)
*Hệ thống phân tầng (Tier 1-2-3), Clean Architecture, và chiến lược Multi-tenancy.*
- [01_ARCHITECTURE.md](./architecture/01_ARCHITECTURE.md): Tổng quan kiến trúc Modular Monolith & Clean Arch 4 lớp. `#architecture` `#tier-system`
- [02_CODE_GOVERNANCE.md](./architecture/02_CODE_GOVERNANCE.md): Quy tắc quản lý giao dịch (ALS), exception và error handling. `#transaction` `#error-handling`
- [03_DATA_STRATEGY.md](./architecture/03_DATA_STRATEGY.md): Chiến lược CSDL: Drizzle ORM, tenant isolation, và delta logging. `#database` `#tenant-isolation`
- [04_DOMAIN_DESIGN.md](./architecture/04_DOMAIN_DESIGN.md): Triết lý thiết kế nghiệp vụ (Rich Domain Model, Position-based HRM). `#ddd` `#domain`
- [05_DEVELOPER_GUIDE.md](./architecture/05_DEVELOPER_GUIDE.md): Setup môi trường, lệnh CLI dev, và quy trình debug. `#onboarding` `#setup`
- [adr/INDEX.md](./architecture/adr/INDEX.md): Index ghi chép các quyết định kiến trúc lớn (ADR). `#adr` `#decisions`

### 2. 🏰 [Governance & Standards](./standards/INDEX.md)
*Các tiêu chuẩn lập trình bắt buộc để đảm bảo tính nhất quán của mã nguồn.*
- [api_contracts.md](./standards/api_contracts.md): Định nghĩa Zod schema làm contract dùng chung giữa BE và FE. `#api` `#contract`
- [architecture_rules.md](./standards/architecture_rules.md): Quy tắc phân lớp nghiêm ngặt trong Clean Architecture. `#rules` `#constitution`
- [import_boundaries.md](./standards/import_boundaries.md): Ranh giới import giữa các module nhằm tránh dependency vòng. `#dependency` `#boundary`
- [naming_conventions.md](./standards/naming_conventions.md): Quy định đặt tên tệp tin, lớp, trường CSDL đồng bộ. `#naming`
- [team_workflow.md](./standards/team_workflow.md): Quản lý vòng đời context công việc và quy trình lưu trữ (history). `#workflow` `#context`
- [ui_components.md](./standards/ui_components.md): Hướng dẫn viết components & quản lý state frontend. `#frontend` `#ui`

### 3. 📚 [Developer Handbooks](./handbooks/INDEX.md)
*Sổ tay thực thi kỹ thuật chuyên sâu.*
- [clean-architecture-handbook-v2.md](./handbooks/clean-architecture-handbook-v2.md): Hướng dẫn thực hành Clean Arch qua ví dụ cụ thể. `#clean-arch`
- [orm-mapping.md](./handbooks/orm-mapping.md): FlatleftrightarrowNested mapping với Drizzle và Base Repository. `#drizzle` `#orm`
- [logging.md](./handbooks/logging.md): Winston Logger Adapter, Audit Logging và hiển thị Activity Feed. `#logging` `#audit-log`
- [permissions.md](./handbooks/permissions.md): Đặc tả phân quyền RBAC & luồng import/export CSV. `#rbac` `#permissions`
- [request-flow.md](./handbooks/request-flow.md): Luồng đi chi tiết của HTTP Request qua Guards, Interceptors, Pipes. `#request-flow`
- [api-documentation.md](./handbooks/api-documentation.md): Tài liệu hướng dẫn sử dụng API Swagger. `#swagger`
- [cac-buoc-refactoring.md](./handbooks/cac-buoc-refactoring.md): Sách tái cấu trúc mã nguồn vi phạm quy chuẩn. `#refactor`

### 4. 📦 [Domain Knowledge](./domain/INDEX.md)
*Tri thức nghiệp vụ chuyên sâu.*
- [Quy trình...docx.md](./domain/Quy%20trình%20cung%20cấp%20dịch%20vụ%20kế%20toán%20thuế%20trọn%20gói.docx.md): Quy trình nghiệp vụ kế toán thuế chi tiết. `#accounting` `#business`
- [crm_accounting_status_report.md](./domain/crm_accounting_status_report.md): Báo cáo tích hợp luồng nghiệp vụ CRM và Kế toán. `#crm` `#accounting`

---

## 🚦 Trạng thái Dự án (Project Health)
- **Kiến trúc:** ✅ Đạt chuẩn Clean Architecture & DDD.
- **Tenancy Isolation:** ✅ Đã thực thi hoàn hảo qua ALS.
- **Tài liệu:** ✅ Đã được hệ thống hóa đồng bộ (Phase 2 hoàn tất).
