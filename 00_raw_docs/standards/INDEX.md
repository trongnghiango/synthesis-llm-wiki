---
folder: standards
description: "Quy chuẩn & Quy tắc phát triển bắt buộc của dự án STAX"
tags: [standards, governance, quality, conventions]
last_updated: "2026-05-21"
---

# 📂 Standards — Quy chuẩn Phát triển

> Các tiêu chuẩn lập trình bắt buộc để đảm bảo chất lượng, tính nhất quán, và tính độc lập của các module trong codebase STAX.

---

## 🧭 Danh sách Quy chuẩn

| File | Tóm tắt 1 dòng | Tags | Đọc khi... |
| :--- | :--- | :--- | :--- |
| **[api_contracts.md](./api_contracts.md)** | Hợp đồng API (Contracts) dùng chung giữa BE và FE dựa trên Zod. | `#api` `#zod` `#contract` | Thiết kế Endpoint API mới hoặc viết DTOs. |
| **[architecture_rules.md](./architecture_rules.md)** | Hiến pháp kiến trúc: ranh giới và cách giao tiếp giữa 4 lớp. | `#constitution` `#clean-arch` | Bắt đầu viết logic nghiệp vụ cho một Module. |
| **[import_boundaries.md](./import_boundaries.md)** | Quy tắc phân cấp import giữa các Module (Tier 1-2-3). | `#boundaries` `#dependency` | Cần import chéo giữa các Module khác nhau. |
| **[naming_conventions.md](./naming_conventions.md)** | Quy định đặt tên file, class, interface, CSDL đồng bộ. | `#naming` `#conventions` | Tạo file mới hoặc thiết kế bảng CSDL mới. |
| **[team_workflow.md](./team_workflow.md)** | Quy trình làm việc nhóm, quản lý context và lưu trữ history. | `#workflow` `#git` `#context` | Kết thúc một task và chuẩn bị commit/archive. |
| **[ui_components.md](./ui_components.md)** | Quy chuẩn xây dựng components và quản trị UI state frontend. | `#frontend` `#ui` `#react` | Viết code Frontend/React. |

---
*Cập nhật gần nhất: 2026-05-21*
