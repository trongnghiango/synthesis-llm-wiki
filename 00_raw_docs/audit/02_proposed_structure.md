# 🗺️ STAX Docs Target Structure (Cấu trúc tài liệu đề xuất)

Dưới đây là sơ đồ cây thư mục mục tiêu giúp hợp nhất các tài liệu chồng chéo, loại bỏ liên kết hỏng, và phân loại khoa học các nhóm tài liệu của dự án STAX.

*(Lưu ý: Các thư mục `context/` và `history/` được giữ nguyên vẹn tại vị trí hiện tại theo yêu cầu).*

---

## 🌳 Sơ đồ Cây Thư mục Đề xuất

```
docs/
├── README.md                           ← Điểm bắt đầu duy nhất (Onboarding Path)
├── INDEX.md                            ← Điều hướng trung tâm toàn bộ Knowledge Base
├── AI_MAP.md                           ← Sơ đồ định hướng cho AI Agents
├── TIPS.md                             ← Hướng dẫn điều hành AI Agent
├── 06_CHANGELOG.md                     ← Lịch sử thay đổi hệ thống (hợp nhất từ STAX_V2)
├── STAX_Google_Drive_Setup_Report.docx ← Tài liệu hướng dẫn Drive (Word)
├── STAX_Google_Drive_Setup_Report.pdf  ← Tài liệu hướng dẫn Drive (PDF)
├── tasks_phase1_stax_v2 - tasks.csv    ← CSV quản lý tiến độ
│
├── architecture/                       ← 📄 Tài liệu kiến trúc canonical
│   ├── INDEX.md                        ← Chỉ mục nhóm tài liệu kiến trúc
│   ├── 01_ARCHITECTURE.md              ← Kiến trúc Modular Monolith & Clean Arch
│   ├── 02_CODE_GOVERNANCE.md           ← Quản trị code: Transaction & Exception
│   ├── 03_DATA_STRATEGY.md             ← Chiến lược DB: Drizzle, ALS, Isolation
│   ├── 04_DOMAIN_DESIGN.md             ← Thiết kế Domain: Position-based HRM & CRM
│   ├── 05_DEVELOPER_GUIDE.md           ← Hướng dẫn setup và dev workflow
│   │
│   └── adr/                            ← 📁 Hợp nhất toàn bộ ADR về đây
│       ├── INDEX.md                    ← Chỉ mục các quyết định kiến trúc
│       ├── ADR-001-export-repository.md
│       ├── ...
│       └── ADR-011-registry-pattern-for-decoupling.md
│
├── standards/                          ← 📄 Các tiêu chuẩn & quy tắc phát triển
│   ├── INDEX.md                        ← Chỉ mục nhóm standards
│   ├── api_contracts.md                ← Quy chuẩn Zod & API contract
│   ├── architecture_rules.md           ← Ranh giới 4 lớp Clean Architecture
│   ├── import_boundaries.md            ← Quy tắc module boundary (ports/events)
│   ├── naming_conventions.md           ← Quy định đặt tên tệp, class, db schema
│   ├── team_workflow.md                ← Quy trình quản lý context và history
│   └── ui_components.md                ← Quy chuẩn frontend components & state
│
├── handbooks/                          ← 📄 Sổ tay thực thi kỹ thuật (Đã làm sạch)
│   ├── INDEX.md                        ← Chỉ mục sổ tay hướng dẫn
│   ├── clean-architecture.md           ← Hợp nhất từ handbook v2
│   ├── orm-mapping.md                  ← Hợp nhất từ orm.md và orm-mapping.md
│   ├── logging.md                      ← Hợp nhất từ LOGGING.md & logging.md (xóa hoa/thường)
│   ├── permissions.md                  ← Hướng dẫn phân quyền RBAC
│   ├── request-flow.md                 ← Sơ đồ luồng chạy của HTTP Request
│   ├── api-documentation.md            ← Tài liệu tích hợp API
│   └── cac-buoc-refactoring.md         ← Sổ tay tái cấu trúc code vi phạm
│
├── domain/                             ← 📄 Tri thức nghiệp vụ (Thư mục mới)
│   ├── INDEX.md                        ← Chỉ mục nhóm nghiệp vụ
│   ├── Quy trình...docx.md             ← Luồng dịch vụ kế toán thuế trọn gói
│   └── crm_accounting_status_report.md ← Báo cáo tích hợp luồng CRM & Kế toán
│
├── _legacy/                            ← 📁 Nơi lưu trữ tài liệu cũ/nháp (Đọc tham khảo)
│   ├── README.md                       ← Giải thích lý do tồn tại thư mục
│   ├── erp-hrm/                        ← 10 file thiết kế erp-hrm cũ (2026-03/04)
│   └── handbooks/                      ← Các ghi chú nháp cũ không còn canonical
│       ├── fix_logic_mapping.md
│       ├── quy-tac-dat-ten-interface.md
│       ├── policy-engine-abac.md
│       ├── nhan-xet-va-cai-thien-du-an.md
│       ├── nang-cap-mo-hinh-ung-dung.md
│       └── smell.md
│
├── context/                            ← [GIỮ NGUYÊN] Các context đang active
└── STAX/                               ← [GIỮ NGUYÊN] Chứa lịch sử history/ cũ
    └── history/                        ← Lịch sử các session làm việc
```
