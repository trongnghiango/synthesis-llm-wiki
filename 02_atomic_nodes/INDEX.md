# 📂 DANH MỤC NỐT NGUYÊN TỬ STAX (STAX ATOMIC KNOWLEDGE INDEX)

Chào mừng bạn đến với Layer 3 - Hệ thống **Nốt nguyên tử (Atomic Notes)** của dự án STAX. Các tài liệu ở đây được thiết kế siêu gọn nhẹ (dưới 50 dòng) và độc lập nhằm phục vụ việc tìm kiếm chính xác và tiết kiệm Token tối đa cho các AI Agents.

---

## 🏗️ 1. Nhóm Kiến trúc & Hạ tầng (Architecture & Infrastructure)

| Nốt Nguyên Tử | Tóm tắt (1 dòng) | Phụ thuộc | Tags |
| :--- | :--- | :--- | :--- |
| [[arch-architecture_blueprint_v1_rollout]] | Thiết lập nền tảng Modular Monolith và thực hiện Phase 0 & Phase 1 Client Modularization cho dự án STAX. | *Tự động* | `#architecture ` #modular-monolith ` #client-refactor ` #api-modularization ` #bff` |
| [[arch-constitution-hardening]] | Chuẩn hóa kiến trúc STAX thông qua Event-Driven Auditing, dynamic Bootstrap permissions và thuần hóa Domain Exceptions. | *Tự động* | `#architecture ` #auditing ` #event-driven ` #security ` #domain-purity` |
| [[arch-architecture_v1_adoption]] | Quy hoạch RBAC sang chuẩn domain:action, cấu trúc lại API Bootstrap permissions.raw/flags và xác lập Backend làm Domain Service. | *Tự động* | `#architecture ` #rbac ` #bootstrap-service ` #migration` |
| [[arch-audit-log-decoupling]] | Kiến trúc Audit Log phi xâm lấn qua Event-Driven Architecture (EDA), tối ưu hóa ghi bất đồng bộ và lưu trữ lai. | *Tự động* | `#architecture ` #audit-log ` #eda ` #performance ` #postgres-jsonb` |
| [[arch-tanstack-router-migration]] | Chuyển đổi hệ thống routing từ wouter sang TanStack Router bảo đảm type-safe và tối ưu hóa UI/UX sơ đồ tổ chức (OrgChart). | *Tự động* | `#routing ` #tanstack-router ` #frontend ` #org-chart ` #ui-ux` |
| [[arch-system-api-integration]] | Tái cấu trúc SystemModule sử dụng Lookup/Bootstrap Service và triển khai chuẩn Backend-Driven UI thông qua ActionableDto. | *Tự động* | `#system-module ` #backend-driven-ui ` #actionable-dto ` #api-design` |
| [[arch-unit-of-work]] | Hướng dẫn áp dụng Unit of Work qua ITransactionManager đảm bảo tính ACID khi điều phối nhiều Repository/Module trong một Use Case. | *Tự động* | `#architecture ` #ddd ` #unit-of-work ` #transaction ` #nestjs` |
| [[arch-shared_contracts_refactor]] | Phân rã shared/schema.ts thành các domain contracts riêng biệt truy cập qua alias @shared nhằm giảm coupling hệ thống. | *Tự động* | `#refactor ` #shared-contracts ` #architecture ` #domain-driven` |
| [[arch-stax-implementation-roadmap]] | Lộ trình 11 Sprint kiến trúc & phát triển độc lập STAX: Core, HRM (Org Tree), CRM (Leads/Drive), Finote (Auto-Approve), Audit Log và Dynamic Payroll. | *Tự động* | `#roadmap ` #architecture ` #materialized-path ` #audit-log ` #auto-approve` |
| [[arch-legacy_api_cleanup]] | Loại bỏ hoàn toàn đối tượng api dùng chung tại queryClient và chuyển đổi sang mô hình Modular API độc lập. | *Tự động* | `#refactor ` #modular-api ` #query-client ` #tech-debt` |
| [[arch-domain-hardening]] | Đóng gói thuộc tính nhạy cảm của Finote, chuyển dịch logic nghiệp vụ vào thực thể và loại bỏ cấu hình cứng. | *Tự động* | `#clean-architecture ` #domain-driven-design ` #finote ` #encapsulation ` #refactoring` |
| [[arch-audit-log-standardization]] | Chuẩn hóa ánh xạ snake_case sang camelCase, thực thi DrizzleAuditLogService qua port, và hợp nhất dữ liệu Omnichannel Activity Feed. | *Tự động* | `#audit-log ` #naming-standardization ` #activity-feed ` #drizzle ` #onboarding` |
| [[arch-system-api-refactoring]] | Tái cấu trúc SystemModule qua Lookup/Bootstrap Service và chuẩn hóa tương tác Backend-Driven UI qua ActionableDto. | *Tự động* | `#system-module ` #backend-driven-ui ` #actionable-dto ` #refactoring ` #crm-api` |
| [[arch-modular-monolith-tiers]] | Phân loại module thành 3 Tiers tránh circular dependency. | *Không* | `#architecture` `#modular` |
| [[arch-clean-boundaries]] | Ranh giới độc lập của 4 lớp Clean Architecture. | [[arch-modular-monolith-tiers]] | `#clean-arch` `#layers` |
| [[arch-als-tenant-isolation]] | Tự động hóa cô lập tenant lọc CSDL thông qua ALS. | [[arch-clean-boundaries]] | `#multi-tenancy` `#als` |
| [[arch-als-transactions]] | Quản lý transactional boundary ngầm định qua ALS. | [[arch-als-tenant-isolation]] | `#transactions` `#als` |
| [[arch-exception-handling]] | Luật xử lý và ném exception an toàn trong Clean Arch. | [[arch-clean-boundaries]] | `#exceptions` `#error` |

---

## 🏰 2. Nhóm Tiêu chuẩn & Quy tắc (Standards & Governance)

| Nốt Nguyên Tử | Tóm tắt (1 dòng) | Phụ thuộc | Tags |
| :--- | :--- | :--- | :--- |
| [[std-naming-rules]] | Quy ước đặt tên tệp, thư mục, hàm, biến và CSDL. | *Không* | `#standards` `#naming` |
| [[std-import-boundaries]] | Luật import chéo cấm import sâu, xuất qua index.ts. | [[arch-modular-monolith-tiers]] | `#boundaries` `#modularity` |
| [[std-api-contracts]] | Thiết kế API hướng hợp đồng dùng chung qua Zod Schema. | *Không* | `#contracts` `#zod` |
| [[std-team-workflow]] | Quy trình 4 bước lưu vết từ BA đến code và đóng băng history. | *Không* | `#workflow` `#history` |

---

## 📚 3. Nhóm Sổ tay Thực thi (Technical Handbooks)

| Nốt Nguyên Tử | Tóm tắt (1 dòng) | Phụ thuộc | Tags |
| :--- | :--- | :--- | :--- |
| [[hb-stax-safe-update-pattern]] | Giải pháp Safe-Update tự động lọc bỏ các trường bất biến (id, audit, tenant) khi cập nhật dữ liệu để tránh lỗi ràng buộc Database. | *Tự động* | `#drizzle ` #repository ` #safe-update ` #database-constraint ` #refactoring` |
| [[hb-stax-implementation-roadmap]] | Lộ trình 22 tuần chia thành 11 Sprints tối ưu hóa cho Solo-Developer triển khai hệ thống STAX (HRM, CRM, Finote, Task & Payroll) sử dụng Drizzle ORM và PostgreSQL. | *Tự động* | `#roadmap ` #project-management ` #sprint ` #solo-dev ` #tech-stack` |
| [[hb-tanstack-router-migration]] | Hướng dẫn chuyển đổi hệ thống routing sang TanStack Router, áp dụng Route Guard và tối ưu giao diện full-screen cho OrgChart. | *Tự động* | `#tanstack-router ` #routing ` #layout ` #orgchart ` #ux-optimization` |
| [[hb-integration-testing-stabilization]] | Thắt chặt Application Layer (loại bỏ Framework Leak) và chuyển đổi test database engine từ pg-mem sang PGLite để tương thích hoàn toàn với Drizzle ORM. | *Tự động* | `#testing ` #pglite ` #drizzle ` #exceptions ` #architecture` |
| [[hb-legacy_migration]] | Quy trình thiết kế di cư dữ liệu legacy CRM sang STAX sử dụng mô hình Hybrid Storage JSONB và giải quyết các xung đột Schema/ORM. | *Tự động* | `#data-migration ` #hybrid-storage ` #jsonb ` #drizzle-orm ` #crm` |
| [[hb-drizzle-base-repo]] | Triển khai Repository Adapter kế thừa từ Base Repo. | [[arch-clean-boundaries]], [[arch-als-tenant-isolation]] | `#drizzle` `#orm` |
| [[hb-delta-logging]] | Ghi nhật ký thay đổi dữ liệu nghiệp vụ dạng Delta JSON. | *Không* | `#logging` `#delta-log` |
| [[hb-rbac-permissions]] | Phân quyền vai trò tĩnh định dạng domain:resource:action. | *Không* | `#rbac` `#permissions` |
| [[hb-http-request-flow]] | Sơ đồ luồng chạy tuần tự của một HTTP Request qua NestJS. | [[arch-als-tenant-isolation]], [[hb-rbac-permissions]] | `#request-flow` `#nestjs` |

---

## 📦 4. Nhóm Nghiệp vụ & Từ điển (Domain Knowledge)

| Nốt Nguyên Tử | Tóm tắt (1 dòng) | Phụ thuộc | Tags |
| :--- | :--- | :--- | :--- |
| [[dom-accounting-cash-book]] | Đặc tả nghiệp vụ chống âm quỹ, cơ chế chuyển khoản nội bộ nguyên tử và tích hợp thanh toán hóa đơn với Sổ Quỹ. | *Tự động* | `#cash-book ` #accounting ` #transaction-propagation ` #domain-entity ` #drizzle-orm` |
| [[dom-cash-transfer-sync]] | Cơ chế đồng bộ hóa bất đồng bộ thông qua Domain Event khi chuyển tiền nội bộ, tự động sinh bút toán nháp kép. | *Tự động* | `#accounting ` #event-driven ` #money-transfer ` #journal-entry` |
| [[arch-crm-accounting-audit-20260509]] | Giải quyết trùng lặp thực thể CRM, áp dụng cô lập Tenant cho Accounting và chuẩn hóa Attachment. | *Tự động* | `#crm ` #accounting ` #tenant-isolation ` #identity ` #refactoring` |
| [[dom-accounting_party_standardization]] | Chuẩn hóa cấu trúc Đối tượng (Party) trong Finote nhằm phân định Tenant và Partner, tối ưu hóa DB Schema và API response. | *Tự động* | `#accounting ` #database-schema ` #domain-entity ` #api-contract` |
| [[dom-finote-detail-page]] | Thiết kế và triển khai trang chi tiết Phiếu Thu/Chi (finote-detail) sử dụng TanStack Router, Bento Grid, và cơ chế Server-Driven Actions. | *Tự động* | `#accounting ` #finote ` #frontend ` #tanstack-router ` #bento-grid` |
| [[dom-company-stats-aggregation]] | Định nghĩa logic truy vấn và cấu trúc DTO tổng hợp chỉ số vận hành, tài chính, thuế và hiệu năng doanh nghiệp. | *Tự động* | `#domain ` #company-stats ` #finance ` #kpi` |
| [[dom-tasks-management-implementation]] | Thiết kế kỹ thuật và lộ trình triển khai module Quản lý Công việc (Tasks) cao cấp cho HRM. | *Tự động* | `#hrm ` #tasks ` #frontend ` #premium-ui ` #kanban` |
| [[dom-crm-kanban-reports]] | Thiết kế Frontend Kanban Board kéo thả với Optimistic Updates và Dashboard báo cáo CRM tích hợp Recharts. | *Tự động* | `#frontend ` #crm ` #kanban ` #reports ` #react-query ` #recharts` |
| [[hist-20260509-fix-accounting-integration]] | Chuẩn hóa luồng tạo Finote: Đồng bộ Employee ID, tự động gán Organization ID và hỗ trợ tương thích ngược DTO. | *Tự động* | `#accounting ` #finote ` #tenant-isolation ` #resolution ` #backwards-compatibility` |
| [[dom-crm-ui-standardization]] | Chuẩn hóa UI Components (PageHeader, DataGrid) cho CRM và sửa lỗi Drizzle mapping trong Lead Repository. | *Tự động* | `#crm ` #ui-standardization ` #drizzle-orm ` #lead-repository ` #nestjs` |
| [[dom-manage-position-department-ui]] | Thiết kế Kanban Staffing Board và chuẩn hóa API nghiệp vụ quản lý chức vụ, phân bổ nhân sự. | *Tự động* | `#hrm ` #staffing-board ` #org-structure ` #api-contract` |
| [[dom-service-catalog-fe]] | Zod schema, API contract, ServicePicker và luồng tích hợp Service Catalog vào Quote và Finote. | *Tự động* | `#crm ` #service-catalog ` #frontend ` #integration` |
| [[dom-professional-activity-feed-and-structured-metadata]] | Chuẩn hóa cấu trúc AuditEntryPayload hỗ trợ actor tracking và cơ chế aggregation cho Activity Feed trong phân hệ CRM. | *Tự động* | `#crm ` #activity-feed ` #audit-log ` #event-driven ` #actor-tracking` |
| [[dom-rbac_resource_standardization]] | Chuẩn hóa tài nguyên hrm thành employee/org và cập nhật logic wildcard manage để sửa lỗi phân quyền ADMIN. | *Tự động* | `#rbac ` #permission ` #authorization ` #security` |
| [[dom-org_structure_position_api]] | Định nghĩa API endpoint và luồng dữ liệu truy vấn danh sách Vị trí (Position) theo Đơn vị tổ chức (OrgUnit) sử dụng Drizzle ORM. | *Tự động* | `#org-structure ` #position ` #drizzle ` #api` |
| [[dom-hrm_master_data_implementation]] | Triển khai module Danh mục HRM gồm Chức danh, Bậc lương và cơ chế lookup động phục vụ định biên nhân sự. | *Tự động* | `#hrm ` #master-data ` #use-lookups ` #clean-architecture` |
| [[dom-accounting-module-research]] | Đặc tả nghiệp vụ và kiến trúc kỹ thuật phân hệ Kế toán Phase 1: Hệ thống tài khoản, Nhật ký chung và tích hợp Lead-to-Contract-to-Finote. | *Tự động* | `#accounting ` #chart-of-accounts ` #general-ledger ` #finote ` #lead-to-contract` |
| [[dom-service-catalog]] | Cấu trúc schema, DDD domain model và workflow chuyển đổi Lead-to-Contract của module Service Catalog. | *Tự động* | `#service-catalog ` #domain-driven-design ` #database-schema ` #workflow-automation` |
| [[dom-crm-fix-lead-acquired-at]] | Cập nhật API GET /crm/leads trả về acquiredAt thực tế từ DB thay vì fallback sang createdAt tại Backend, đồng bộ với LeadResponseDto và UI Kanban. | *Tự động* | `#crm ` #lead ` #api-contract ` #dto ` #bug-fix` |
| [[dom-crm-client_360_view]] | Trang chi tiết khách hàng CRM 360° tích hợp theo dõi tuân thủ thuế, hợp đồng, và dòng thời gian tương tác thời gian thực. | *Tự động* | `#crm ` #client-360 ` #tax-compliance ` #react ` #ui-ux` |
| [[dom-crm-analytics-service]] | Dịch vụ read-only phân tích CRM (Pipeline, Doanh thu, Cảnh báo) dùng Drizzle CTE trực tiếp. | *Tự động* | `#crm ` #analytics ` #drizzle-orm ` #read-model ` #dashboard` |
| [[dom-manual-accounting-entries]] | Tích hợp giao diện và DTO hỗ trợ lập phiếu thu/chi thủ công và định khoản trực tiếp trong phân hệ kế toán STAX. | *Tự động* | `#accounting ` #journal-entry ` #finote ` #dto ` #backend ` #frontend` |
| [[arch-crm-normalization-migration]] | Phục hồi thiết kế chuẩn hóa CRM, tách Contact/Organization khỏi Leads và thực hiện di trú dữ liệu qua Drizzle ORM. | *Tự động* | `#crm ` #db-schema ` #drizzle ` #data-migration ` #domain-model` |
| [[dom-hrm_employee_management]] | Thiết kế API contracts mở rộng và mô hình giao diện Employee 360 tối ưu hiệu suất cho STAX HRM. | *Tự động* | `#hrm ` #employee-360 ` #api-contract ` #schema-extension` |
| [[dom-audit-log-feed]] | Chuẩn hóa hạ tầng Audit Log (Drizzle, camelCase) và triển khai Omnichannel Activity Feed hợp nhất timeline tổ chức. | *Tự động* | `#audit-log ` #activity-feed ` #drizzle ` #camelcase ` #onboarding` |
| [[dom-attachment-management]] | Tích hợp React Query Hooks và Component AttachmentBoard polymorph để quản lý tài liệu đính kèm của Client, Contract, Lead. | *Tự động* | `#frontend ` #react-query ` #attachment ` #drag-drop ` #polymorphic` |
| [[dom-org-position-crud]] | Hoàn thiện CRUD thực thể Positions với kiểm tra ràng buộc khóa ngoại và cơ chế bảo vệ ngăn xóa khi có nhân sự đang đảm nhiệm. | *Tự động* | `#domain ` #org-structure ` #position ` #crud ` #drizzle` |
| [[dom-crm-lead-acquired-at-fix]] | Đồng bộ LeadResponseDto để trả về thuộc tính acquiredAt thực tế từ Database cho các API Leads. | *Tự động* | `#crm ` #lead ` #dto ` #api-contract ` #bug-fix` |
| [[dom-crm-client-360-view]] | Triển khai màn hình chi tiết khách hàng ClientDetail 360° tích hợp Glassmorphism, chỉ số tài chính, tuân thủ thuế và dòng hoạt động. | *Tự động* | `#crm ` #client-360 ` #react ` #api-contract ` #compliance` |
| [[dom-user_entity_org_context_refactor]] | Tập trung logic xác định Tenant/Organization ID vào User Domain Entity thay vì xử lý thủ công tại Controllers/Services. | *Tự động* | `#domain-driven-design ` #multi-tenancy ` #authentication ` #user-entity ` #refactoring` |
| [[arch-crm-analytics-service]] | Kiến trúc CrmAnalyticsService tối ưu truy vấn CTE qua Drizzle ORM phục vụ dashboard pipeline, doanh thu YoY và cảnh báo. | *Tự động* | `#crm ` #analytics ` #drizzle-orm ` #pipeline ` #revenue` |
| [[dom-accounting-foundation]] | Thiết lập hệ thống kế toán kép (COA, Journal Entries, Ledger) và cơ chế tự động hóa bút toán từ Finote. | *Tự động* | `#accounting ` #double-entry ` #coa ` #ledger ` #journal-entry` |
| [[dom-finote-payment]] | Thiết kế component và API tích hợp ghi nhận thanh toán Finote (Partial/Full) sử dụng Server-Driven UI và Shared Contract Zod. | *Tự động* | `#accounting ` #finote ` #payment ` #react-hook-form ` #server-driven-ui ` #zod` |
| [[dom-accounting-manual-entries]] | Tích hợp giao diện và DTO Backend cho luồng lập phiếu thu/chi thủ công (Finote) và định khoản bút toán tay (Journal Entry). | *Tự động* | `#accounting ` #finote ` #journal-entry ` #dto ` #frontend` |
| [[dom-finote-detail-api]] | API GET /accounting/finotes/:id tích hợp Tenancy Enforcement và cơ chế Server-Driven UI Actions dựa trên vai trò người dùng. | *Tự động* | `#finote ` #security ` #tenancy ` #server-driven-ui ` #api` |
| [[dom-crm_lead_restoration]] | Chuẩn hóa thực thể Lead qua liên kết contact_id và tối ưu hóa lưu trữ thuộc tính động bằng cột metadata JSONB. | *Tự động* | `#crm ` #schema-normalization ` #drizzle ` #data-migration` |
| [[dom-employee-update-api]] | Quy trình nghiệp vụ và API contract cập nhật thông tin nhân sự bảo mật đa thuê bao (multi-tenancy) và ràng buộc vị trí. | *Tự động* | `#hrm ` #employee ` #api-patch ` #multi-tenancy ` #validation` |
| [[dom-crm-naming-migration-stage1]] | Chuẩn hóa CRM naming từ companyName sang organizationName tại DB Schema và API Layer hỗ trợ tương thích ngược. | *Tự động* | `#crm ` #migration ` #database-schema ` #backward-compatibility ` #backend` |
| [[dom-hrm-employee-management]] | Mở rộng schema Employee, bổ sung HRMTask API, và tích hợp bộ UI Component Employee 360 sử dụng STAX DataGrid. | *Tự động* | `#hrm ` #schema ` #api-contract ` #employee-360 ` #datagrid` |
| [[dom-attachment-management-fe]] | Tích hợp UI Component AttachmentBoard polymorphic vào các thực thể CRM (Lead, Client, Contract) qua React Query. | *Tự động* | `#frontend ` #attachment ` #polymorphic ` #react-query ` #crm` |
| [[dom-employee_tasks_crud]] | Thiết kế DB, API nested resource và phân quyền cho tính năng Employee Tasks. | *Tự động* | `#hrm ` #employee-task ` #crud ` #api-design ` #multi-tenancy` |
| [[dom-position-crud]] | Đặc tả nghiệp vụ và kỹ thuật triển khai CRUD thực thể Position (Vị trí) tích hợp Drizzle ORM. | *Tự động* | `#org-structure ` #position ` #crud ` #drizzle-orm ` #api-design` |
| [[dom-hrm_positions_management]] | Đặc tả kỹ thuật và cấu trúc triển khai giao diện quản lý vị trí định biên (Positions) thuộc phân hệ HRM. | *Tự động* | `#hrm ` #positions ` #route-setup ` #ui-component` |
| [[dom-org-structure-recursion-strategy]] | Cơ chế truy vấn đệ quy qua Materialized Path (LIKE path%) hỗ trợ tổng hợp dữ liệu phòng ban con. | *Tự động* | `#org-structure ` #recursion ` #drizzle-orm ` #api` |
| [[dom-org_structure]] | Thiết kế và triển khai sơ đồ tổ chức trực quan (Org Chart) tương tác cao sử dụng Framer Motion, xử lý dữ liệu đệ quy và tối ưu hiển thị. | *Tự động* | `#org-chart ` #framer-motion ` #tailwind ` #recursive-data` |
| [[dom-audit-log-management]] | Hệ thống giám sát Audit Log thời gian thực (Polling 30s) hỗ trợ so sánh dữ liệu Delta JSON và điều hướng nhanh đến tài nguyên. | *Tự động* | `#audit-log ` #polling ` #delta-view ` #monitoring ` #system-module` |
| [[dom-hybrid_security_crm]] | Thiết kế bảo mật lai 3 lớp áp dụng cho module CRM Leads: Guard (Controller), Query Isolation (Repo), và Dynamic Actions (DTO). | *Tự động* | `#security ` #crm ` #hybrid-security ` #acl ` #action-dto` |
| [[dom-hrm-position-model]] | Triết lý quản lý nhân sự dựa trên Vị trí (Position-based). | *Không* | `#domain` `#hrm` `#position` |
| [[dom-accounting-finote]] | Luồng chứng từ phiếu thu/chi và đồng bộ số dư Sổ quỹ. | *Không* | `#domain` `#accounting` `#finote` |
| [[dom-crm-pipelines]] | Quản lý cơ hội qua Kanban và tự động chuyển đổi sang Org. | *Không* | `#domain` `#crm` `#leads` |

---
*Mạng lưới liên kết chéo chằng chịt giúp AI duyệt đồ thị tri thức cực kỳ linh hoạt.*
