# Báo cáo Trạng thái Triển khai Module CRM & Accounting

Dựa trên quá trình quét toàn bộ cấu trúc mã nguồn (Backend và Frontend) của dự án STAX, dưới đây là báo cáo chi tiết về những phần **đã làm** và **chưa làm** đối với 2 module `crm` và `accounting`.

---

## 1. Module CRM (Quản lý Khách hàng & Hợp đồng)

### 🟢 Phần ĐÃ LÀM (Implemented)
**Backend:**
- **Domain Layer (Khá hoàn thiện):**
  - Đã định nghĩa các Entities cốt lõi: `Lead`, `Organization`, `Contact`, `Quote`, `Service`, `Contract`, `ServiceAssignment`.
  - Đã có các Domain Events phong phú: `lead-created`, `lead-status-changed`, `contract-created`, `contract-activated`, `quote-created`, `deal-won`, v.v.
  - Định nghĩa đầy đủ Interface cho Repositories.
- **Infrastructure Layer:**
  - Đã triển khai Drizzle Repositories cho toàn bộ Entities (Lead, Quote, Contact, Assignment, Organization, Contract, Service).
  - Đã có các Mappers để chuyển đổi giữa Database Model và Domain Entity.
  - Đã có Data Transfer Objects (DTOs) cơ bản cho luồng Lead & Quote (`update-lead`, `assign-lead`, `get-organizations`, v.v.).
  - Đã thiết lập `lead.controller.ts` và `quote.controller.ts`.

**Frontend:**
- Đã có các Component UI cơ sở: `LeadForm.tsx`, `OrganizationPicker.tsx`, `ServicePicker.tsx`.
- Đã khai báo các API hook cơ bản: `crm.api.ts`, `service.api.ts`.

### 🔴 Phần CHƯA LÀM (Missing / To-do)
**Backend:**
- **Application Layer (Trống hoàn toàn):** Chưa có bất kỳ Application Service (Use Case) nào được triển khai cho CRM. Thư mục `application` đang trống. Nghĩa là logic xử lý nghiệp vụ (như tạo Hợp đồng, kích hoạt Hợp đồng, phân công Dịch vụ) chưa được implement.
- **Controllers (Còn thiếu):** Chưa có Controllers cho `Contract`, `Organization`, `Contact`, `Service`. Mới chỉ có cho `Lead` và `Quote`.
- **Tự động hóa:** Chưa tích hợp hệ thống Document Management System (DMS) để tự động tạo folder khi Hợp đồng được kích hoạt (như đã phân tích ở quy trình).

**Frontend:**
- Chưa có giao diện hoàn chỉnh (Pages/Views) cho Quản lý Hợp đồng, Danh sách Khách hàng chi tiết (Client List), Bảng theo dõi Lead.

---

## 2. Module Accounting (Kế toán & Yêu cầu thanh toán - Feenote)

### 🟢 Phần ĐÃ LÀM (Implemented)
**Backend:**
- **Domain Layer:**
  - Các Entities cốt lõi: `Finote` (Yêu cầu thanh toán), `Account`, `JournalEntry` (Bút toán), `CashTransaction`.
  - Các Domain Events: `finote-created`, `finote-status-changed`, `payment-allocated`, `payment-overdue`, `bad-debt`.
- **Application Layer (Rất hoàn thiện):**
  - Có đầy đủ các Services nghiệp vụ: `finote.service.ts`, `account.service.ts`, `journal.service.ts`, `payment-reconciliation.service.ts`, `finote-document.service.ts`.
  - Các cơ chế Event Listeners đang hoạt động: `finote-created.listener`, `finote-accounting.listener`.
- **Infrastructure Layer:**
  - Triển khai PDF Generator (Puppeteer & Dummy) cho việc xuất file Finote.
  - File Storage Adapter (Lưu trữ file cục bộ).
  - Drizzle Repositories cho `Account`, `Finote`, `Journal`.
  - Controllers: `finote.controller.ts`, `general-ledger.controller.ts`.

**Frontend:**
- Đã có các Component cho sổ nhật ký chung: `JournalTable.tsx`, `JournalFilterBar.tsx`, `JournalEntryForm.tsx`, `JournalDetailView.tsx`.
- Đã có API definitions: `accounting.api.ts`.

### 🔴 Phần CHƯA LÀM (Missing / To-do)
**Backend:**
- **Phân hệ Dịch vụ Thuế trọn gói (Thu thập chứng từ, Báo cáo thuế):** Hoàn toàn chưa có. Chưa có các Entity như `TaxReportCycle` hay `ClientCredential` (Lưu token, mật khẩu thuedientu).
- **Billing Automation (Nhắc nợ):** Mặc dù đã có Finote và Event `payment-overdue`, nhưng chưa có Cronjob/Scheduler (ngày 15, 20, 25, 30) để tự động quét và kích hoạt Notification nhắc nợ khách hàng.

**Frontend:**
- Chưa có Giao diện (UI) để Quản lý Feenote / Báo phí (Workflow tạo Feenote -> Quản lý duyệt -> Gửi khách).
- Chưa có UI cho các Báo cáo thuế.

---

## 3. Tổng kết & Đề xuất Action Plan

Dựa trên file quy trình dịch vụ bạn cung cấp, hệ thống STAX hiện tại:
1. **Khá mạnh về mặt nền tảng (Foundation):** Sổ cái (Ledger), Finote (Yêu cầu thanh toán) và cấu trúc Domain của CRM đã được setup tốt.
2. **Thiếu sự liên kết nghiệp vụ (Workflow):** Cần triển khai ngay Application Services cho CRM để các đối tượng (Lead, Hợp đồng) có thể tương tác được.
3. **Thiếu phần Dịch vụ Thuế (Tax Services):** Cần tạo một Bounded Context hoặc Sub-module mới trong Accounting để quản lý riêng luồng Báo cáo Thuế và Chứng từ của khách hàng.

**Bước tiếp theo nên làm:**
- Ưu tiên 1: Viết Application Services cho CRM (đặc biệt là phần Hợp đồng và Khách hàng) để hoàn thiện luồng Onboarding.
- Ưu tiên 2: Xây dựng UI cho quy trình tạo và duyệt Feenote trên Frontend (do Backend đã có sẵn Finote Services).
- Ưu tiên 3: Bổ sung Sub-module Tax Reporting (Báo cáo thuế).
