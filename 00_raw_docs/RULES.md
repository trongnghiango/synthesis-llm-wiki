# 🏰 HIẾN PHÁP DỰ ÁN (RULES INDEX)

Chào mừng bạn (AI Agent hoặc Developer) đến với dự án **STAX**. Đây là tệp tin gốc chứa các nguyên tắc tối cao và chỉ dẫn điều hướng cho toàn bộ hệ thống quy định của dự án.

---

## 1. Tuyên ngôn cốt lõi (Core Principles)

1. **Module First**: Mọi tính năng phải được tổ chức theo module. Không tạo code rác rải rác.
2. **Contract-Driven**: Mọi giao tiếp FE-BE phải thông qua `shared/contracts`.
3. **Strict Boundaries**: Tuân thủ nghiêm ngặt ranh giới giữa các module (Tier 1-2-3). Domain layer tuyệt đối cô lập.
4. **Context Management**: Mọi thay đổi phải có tài liệu bối cảnh (context folder) và được lưu trữ (history folder) đúng quy trình.

---

## 2. Mục lục Quy định (Rules Index)

Nếu bạn định thực hiện bất kỳ hành động nào dưới đây, hãy đọc kỹ tài liệu tương ứng trước:

### A. Phát triển Tính năng & Sửa lỗi
- **Quy trình làm việc**: [standards/team_workflow.md](./standards/team_workflow.md)
  *Cách tạo context, task list và walkthrough để bàn giao.*

### B. Cấu trúc mã nguồn & Import
- **Kiến trúc hệ thống**: [standards/architecture_rules.md](./standards/architecture_rules.md)
  *Vị trí đặt file, cấu trúc folder modules.*
- **Ranh giới Import**: [standards/import_boundaries.md](./standards/import_boundaries.md)
  *Cấm deep import, quy tắc public API của module.*

### C. Tiêu chuẩn Mã nguồn & Tích hợp
- **Quy tắc đặt tên**: [standards/naming_conventions.md](./standards/naming_conventions.md)
  *Cách đặt tên file, biến, class, interface và DB schema.*
- **Hợp đồng API (BE-FE)**: [standards/api_contracts.md](./standards/api_contracts.md)
  *Quy chuẩn thiết kế Zod contracts dùng chung giữa Backend và Frontend.*
- **Thiết kế UI/UX**: [standards/ui_components.md](./standards/ui_components.md)
  *Quy chuẩn components, quản lý state và responsiveness frontend.*

---

## 3. Chỉ dẫn cho AI Agent

Trước khi bạn viết dòng code đầu tiên, hãy:
1. Đảm bảo đã hiểu **Kiến trúc** và **Ranh giới Import**.
2. Kiểm tra xem đã có thư mục **Context** cho công việc hiện tại chưa.
3. Sử dụng đường dẫn tương đối (Relative Path) khi dẫn chiếu giữa các tài liệu trong `docs/`.

---
*Tài liệu này được định nghĩa là Nguồn Sự thật Duy nhất (Single Source of Truth) về quy tắc dự án STAX.*
