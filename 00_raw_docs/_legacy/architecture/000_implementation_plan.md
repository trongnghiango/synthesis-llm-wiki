# Báo cáo Thiết kế Kế hoạch Tích hợp Quy trình Dịch vụ Kế toán Thuế (STAX)

Dựa trên phân tích nội dung file MD và chi tiết từ 4 sơ đồ quy trình bạn cung cấp (Quy trình tổng thể, Hợp đồng, Kế toán thuế, và Billing), tôi đề xuất bản thiết kế kiến trúc và kế hoạch tích hợp toàn diện vào hệ thống STAX. 

Mục tiêu cốt lõi: Số hóa hoàn toàn các thao tác thủ công (file Excel CRM, tạo folder tay, nhắc nợ thủ công), đồng thời tuân thủ chặt chẽ kiến trúc **Clean Architecture + DDD** của STAX.

---

## 1. Phân tích Luồng nghiệp vụ (Từ Sơ đồ & Tài liệu)

Dựa vào sơ đồ, có 3 Actor chính tham gia vào quy trình:
1. **Bộ phận Dịch vụ (Service Dept):** Soạn hợp đồng, xin thông tin, làm báo cáo, tạo Feenote (Yêu cầu thanh toán).
2. **Quản lý (Manager):** Kiểm duyệt Feenote và Báo cáo trước khi gửi khách.
3. **Kế toán (Accountant):** Theo dõi thanh toán, xuất hóa đơn GTGT.
4. **Khách hàng (Client):** Cung cấp thông tin, chốt báo cáo, thanh toán.

### Các "Pain points" cần giải quyết bằng Hệ thống:
- Đang dùng Google Sheets/Excel (`FN summary`, `Client list`, `Revenue estimate`).
- Tạo folder lưu trữ (Hợp đồng, Thông tin chung, Dịch vụ) thủ công.
- Nhắc nợ (ngày 15, 20, 25, 30) đang phụ thuộc vào con người.
- Xin thông tin Token, Tài khoản thuế thiếu bảo mật.

---

## 2. Thiết kế Cấu trúc Module (STAX Architecture)

Để đảm bảo ranh giới **Tier 2 (Core)** và **Tier 3 (Process Flow)**, chúng ta sẽ thiết kế các Bounded Context sau:

### 2.1. Module CRM (Quản lý Khách hàng & Hợp đồng)
Thay thế hoàn toàn sheet "Client list" và "Revenue estimate".
- **Entities:** `Client`, `Contract`, `ServiceItem`.
- **Luồng:** Hợp đồng được soạn -> Ký kết (upload bản Scan) -> Chuyển trạng thái `ACTIVE`.
- **Event Bus:** Khi hợp đồng Active, phát ra domain event `ContractActivatedEvent`.

### 2.2. Module DMS (Document Management System - Quản lý tài liệu)
Xử lý quy trình lưu trữ tự động hóa theo chuẩn 3 folder.
- **Consumer:** Lắng nghe `ContractActivatedEvent`.
- **Action:** Giao tiếp với Port/Adapter (S3, Google Drive, hoặc Local Storage) để tự động tạo cấu trúc:
  - `/{clientId}/Contracts`
  - `/{clientId}/General_Info`
  - `/{clientId}/Services/{year}`

### 2.3. Module Accounting Process (Nghiệp vụ Kế toán Thuế)
Quản lý chu kỳ làm báo cáo và thu thập thông tin.
- **Entities:** `ClientCredential` (Lưu trữ Token, Mật khẩu thuế - Cần mã hóa hóa cấp độ cao), `TaxReportCycle` (TNDN, GTGT, TNCN).
- **Luồng:** Tạo Task định kỳ -> Dịch vụ nhập số liệu/upload file mềm -> Gửi khách phê duyệt -> Đóng kỳ.

### 2.4. Module Billing & Invoicing (Thanh toán & Hóa đơn)
Số hóa hoàn toàn sơ đồ Yêu cầu thanh toán (Hình 1).
- **Entities:** `Feenote`, `Invoice`, `PaymentReceipt`.
- **State Machine Feenote:** `DRAFT` (Dịch vụ tạo) -> `PENDING_MANAGER` (Quản lý duyệt) -> `APPROVED` -> `SENT_TO_CLIENT` (Gửi thông báo) -> `PAID` -> `INVOICED` (Kế toán xuất HĐ).

---

## 3. Tự động hóa & Tích hợp Kỹ thuật (Backend)

### 3.1. CronJobs & Workflow Automation (Fire-and-forget)
Hệ thống sẽ thay con người làm các việc nhắc nhở:
- **Nhắc nợ tự động (Billing):** Một Cronjob chạy hàng ngày, quét các `Feenote` ở trạng thái `SENT_TO_CLIENT` chưa thanh toán. Nếu rơi vào ngày 15, 20, 25, 30 -> Kích hoạt `Notification Port` gửi Email/Zalo.
- **Nhắc hạn báo cáo thuế:** Cronjob quét `TaxReportCycle` trước hạn 5 ngày -> Push notification cho Bộ phận dịch vụ.

### 3.2. Event-Driven Architecture (Cách các Module giao tiếp)
Tuyệt đối không Import Repository chéo giữa các Module.
1. Khách hàng thanh toán xong -> Cập nhật `Feenote` thành `PAID`.
2. Hệ thống phát ra `FeenotePaidEvent`.
3. Module Invoicing lắng nghe -> Tạo task `Pending Invoice` cho Kế toán.
4. Kế toán xuất hóa đơn xong -> Phát `InvoiceIssuedEvent` -> Gửi thư cảm ơn kèm Hóa đơn điện tử cho Khách.

---

## 4. Giao diện Frontend (FE Boundaries)

- **Server-Driven UI cho Feenote:** Các nút [Duyệt Feenote] (cho Quản lý), [Xuất HĐ] (cho Kế toán) sẽ được quyết định bởi trường `_actions.allowed` trả về từ Backend (dựa trên Role/Permission hệ thống Rbac của STAX), không hard-code `if (role === 'MANAGER')` trên FE.
- **State Management:** Dùng `React Query` để quản lý danh sách Khách hàng, Báo cáo thuế, Feenote (Domain Data). Tuyệt đối không lưu vào Zustand.

---

> [!WARNING]
> ## Rủi ro & Điểm cần User xác nhận (Open Questions)
> 
> Trước khi chúng ta đi vào thiết kế Schema chi tiết (Zod Contract & Drizzle), tôi cần bạn xác nhận các vấn đề (One-way doors) sau:
> 
> 1. **Client Portal (Giao diện Khách hàng):** Khách hàng sẽ đăng nhập vào hệ thống STAX để duyệt Báo cáo Thuế và Xem Feenote (Cách bảo mật tốt nhất), hay chúng ta chỉ xuất link PDF/gửi Email và Khách hàng xác nhận qua Zalo/Email (Hệ thống STAX chỉ dùng cho Nội bộ)?
> 2. **Xử lý Mật khẩu & Token:** Tài liệu có nhắc đến việc xin "Mật khẩu thuedientu, Token". STAX có cần lưu trữ tập trung các Credential này trên Database (yêu cầu mã hóa AES-256) để tự động nhắc hạn Token không?
> 3. **Tích hợp Zalo/Email:** Đối với luồng nhắc nợ tự động ngày 15, 20, 25, 30, hệ thống có được phép tự động gửi Zalo ZNS / Email trực tiếp đến Khách hàng, hay chỉ tạo ra "Nhắc nhở (Notification)" trên màn hình của nhân viên Dịch vụ để họ tự copy-paste gửi tay?

Vui lòng trả lời các câu hỏi trên, sau đó chúng ta có thể chuyển sang thiết kế Zod Contracts hoặc Implementation Code.
