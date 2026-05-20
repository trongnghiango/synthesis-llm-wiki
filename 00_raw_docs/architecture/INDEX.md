---
folder: architecture
description: "Kiến trúc hệ thống STAX — Từ mô hình Tier đến Clean Architecture"
tags: [architecture, clean-architecture, multi-tenancy, patterns]
last_updated: "2026-05-21"
---

# 📂 Architecture — Kiến trúc Hệ thống

> Thư mục này chứa các tài liệu mô tả cách hệ thống STAX được xây dựng, các quyết định thiết kế quan trọng và lộ trình phát triển kỹ thuật.

---

## 🧭 Danh sách Tài liệu Kiến trúc

### 1. Tài liệu kiến trúc chuẩn (V2 Canonical Docs)

| File | Tóm tắt 1 dòng | Tags | Đọc khi... |
| :--- | :--- | :--- | :--- |
| **[01_ARCHITECTURE.md](./01_ARCHITECTURE.md)** | Phân cấp module (Tiered System), Clean Architecture 4 lớp. | `#architecture` `#tier` | Bắt đầu tìm hiểu về STAX. |
| **[02_CODE_GOVERNANCE.md](./02_CODE_GOVERNANCE.md)** | Quy tắc quản lý giao dịch (ALS), exception và error handling. | `#governance` `#transaction` | Bắt đầu viết code nghiệp vụ. |
| **[03_DATA_STRATEGY.md](./03_DATA_STRATEGY.md)** | Chiến lược CSDL: Drizzle ORM, tenant isolation. | `#database` `#drizzle` | Thiết kế database hoặc tối ưu query. |
| **[04_DOMAIN_DESIGN.md](./04_DOMAIN_DESIGN.md)** | Triết lý thiết kế nghiệp vụ (Rich Domain Model, Position-based HRM). | `#ddd` `#domain` | Muốn hiểu sâu về logic thực thể. |
| **[05_DEVELOPER_GUIDE.md](./05_DEVELOPER_GUIDE.md)** | Setup môi trường, lệnh CLI dev, và quy trình debug. | `#onboarding` `#setup` | Thiết lập môi trường lần đầu. |

### 2. Tài liệu thiết kế bổ trợ (Supplementary Guides)

| File | Tóm tắt 1 dòng | Tags | Đọc khi... |
| :--- | :--- | :--- | :--- |
| **[02_DYNAMICS_REGISTRATION_REGISTRY_PATTERN.md](./02_DYNAMICS_REGISTRATION_REGISTRY_PATTERN.md)** | Đặc tả Registry Pattern giải quyết phụ thuộc vòng (Decoupling). | `#decoupling` `#registry` | Muốn giao tiếp chéo module. |
| **[03_TECHNICAL_DEBT_DB_MISMATCH.md](./03_TECHNICAL_DEBT_DB_MISMATCH.md)** | Báo cáo nợ kỹ thuật và khác biệt cấu trúc DB thực tế. | `#tech-debt` `#database` | Gặp lỗi mapping DB schema. |
| **[adr/INDEX.md](./adr/INDEX.md)** | Nhật ký ghi chép các quyết định kiến trúc lớn (ADR-001 đến ADR-011). | `#adr` `#decisions` | Muốn biết tại sao chúng ta chọn X thay vì Y. |

---
*Cập nhật gần nhất: 2026-05-21*
