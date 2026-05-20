# 🏛️ STAX Project History Index (Archive)

Tài liệu này đóng vai trò là "Sổ cái" ghi lại toàn bộ quá trình tiến hóa của dự án STAX. AI Agents nên đọc file này trước khi quyết định có cần đào sâu vào từng folder lịch sử cụ thể hay không.

---

## 📅 Danh mục Lịch sử phát triển

| Giai đoạn (YYYYMMDD) | Chủ đề / Slug | Mô tả tóm tắt |
| :--- | :--- | :--- |
| **20260320** | `early_design_docs` | Các bản thảo thiết kế ban đầu, sơ đồ DB sơ khai cho ERP/HRM. |
| **20260326** | `unit_of_work` | Thiết lập hạ tầng `Unit of Work` và `Transaction Management` đầu tiên. |
| **20260425** | `standardization_cleanup` | Dọn dẹp nợ kỹ thuật (Legacy code) và chuẩn hóa Database Schema lần 1. |
| **20260426** | `audit_log_standardization` | Triển khai hệ thống Audit Log, Activity Feed và chuẩn hóa Naming sang `camelCase`. |
| **20260426** | `legacy_migration` | Di cư thành công toàn bộ dữ liệu từ Excel (CRM/Kế toán) vào hệ thống STAX. |
| **20260428** | `professional_api_integration`| Tái cấu trúc `SystemModule`, giới thiệu `Actionable Metadata (_actions)` cho UI. |
| **20260430** | `domain_hardening` | Chuyển đổi sang Rich Domain Model, gia cố tính toàn vẹn của dữ liệu nghiệp vụ. |
| **20260501** | `delta_logging_optimization` | Tối ưu hóa dung lượng lưu trữ Log bằng cơ chế Deep Diff (Delta Logging). |
| **20260503** | `hybrid_security_crm` | Triển khai bảo mật 3 lớp (Guard + SQL Filter + DTO Actions) cho Module CRM. |
| **20260503** | `golden_flow_quote` | Hoàn thiện luồng Golden Flow với Module Báo giá (Quote) tự động hóa. |
| **20260504** | `constitution_hardening` | Chiến dịch Testing Phase 3, đảm bảo độ phủ và tính tuân thủ Hiến pháp tuyệt đối. |
| **20260505** | `integration_testing_stabilization`| Chuyển đổi môi trường Test sang PGLite (WASM) để đạt độ tương thích 100% với Drizzle. |
| **20260518** | `finote_payment` | Tích hợp Sổ Quỹ vào luồng Thanh toán Phiếu thu/chi (Finote Payment). |
| **20260518** | `cash_book` | Xây dựng trang Sổ Quỹ (Cash Book) toàn diện với Modern Bento Grid và Classic Ledger Table. |
| **20260518** | `manual_entries` | Tích hợp Lập Bút toán thủ công và Lập Phiếu Thu/Chi thủ công trên Frontend. |
| **20260520** | `crm_kanban_and_reports` | Triển khai giao diện Kanban cho Lead và Dashboard Báo cáo CRM ở Frontend + Hỗ trợ API chuyển đổi trạng thái Lead ở Backend. |
| **20260520** | `fix_lead_acquired_at_display` | Sửa lỗi hiển thị ngày của Lead trên Kanban và Response API của `acquiredAt`. |
| **20260520** | `attachment_management` | Tích hợp hệ thống Quản lý tài liệu đính kèm (Attachments) liên kết Google Drive cho Lead, Contract, Client ở cả BE và FE. |
| **20260520** | `crm_analytics_service` | Xây dựng dịch vụ phân tích dữ liệu CRM (Pipeline, Doanh thu, Cảnh báo thông minh) tối ưu bằng các truy vấn SQL CTE phức tạp. |

---

## 💡 Hướng dẫn cho AI Agents
1. **Kiểm tra Index này trước**: Để xác định xem tính năng mình đang làm có liên quan đến các quyết định cũ trong lịch sử hay không.
2. **Chỉ đọc sâu khi cần**: Nếu task hiện tại liên quan đến Audit Log, hãy đọc folder `20260426` và `20260501`.
3. **Tuyệt đối tuân thủ**: Không tạo file rời rạc ngoài các folder đã được đánh mã ngày tháng tại đây.

---
*Cập nhật lần cuối: 05/05/2026 - Theo quy trình Context Management v1.*
