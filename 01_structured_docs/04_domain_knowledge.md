# 📦 TRI THỨC NGHIỆP VỤ & HỆ THUẬT NGỮ (DOMAIN KNOWLEDGE & GLOSSARY)

Tài liệu này hệ thống hóa các tri thức nghiệp vụ cốt lõi, từ điển thuật ngữ thống nhất (Ubiquitous Language) và luồng quy trình nghiệp vụ (Business Workflows) của hệ thống STAX.

---

## 1. TỪ ĐIỂN THUẬT NGỮ THỐNG NHẤT (UBIQUITOUS LANGUAGE)

Để tránh hiểu nhầm giữa bộ phận Phân tích Nghiệp vụ (BA), Lập trình viên (Dev), và AI Agent, toàn bộ hệ thống bắt buộc phải sử dụng chung các thuật ngữ sau:

| Thuật ngữ tiếng Việt     | Định danh kỹ thuật | Mô tả & Ranh giới                                                               |
| :----------------------- | :----------------- | :------------------------------------------------------------------------------ |
| **Doanh nghiệp / Thuê**  | `Organization`     | Đơn vị thuê dịch vụ, ranh giới phân tách dữ liệu cao nhất (Multi-tenancy).      |
| **Nhân viên**            | `Employee`         | Nhân sự thuộc doanh nghiệp, quản lý trong module HRM.                           |
| **Đơn vị tổ chức**       | `OrgUnit`          | Phòng ban, chi nhánh hoặc tổ chức con cấu thành sơ đồ cây doanh nghiệp.         |
| **Phiếu thu / chi**      | `Finote`           | Chứng từ ghi nhận giao dịch dòng tiền (Financial Note) trong module Accounting. |
| **Liên hệ / Khách hàng** | `Contact`          | Người đại diện khách hàng của doanh nghiệp trong module CRM.                    |
| **Cơ hội / Đầu mối**     | `Lead`             | Cơ hội bán hàng tiềm năng trong CRM.                                            |
| **Vai trò & Phân quyền** | `Rbac`             | Vai trò và các quyền hạn tĩnh gán cho nhân viên hoặc người dùng.                |
| **Nhật ký thay đổi**     | `AuditLog`         | Nhật ký lưu vết thay đổi dữ liệu nghiệp vụ theo cơ chế Delta.                   |

---

## 2. LUỒNG NGHIỆP VỤ KẾ TOÁN THUẾ TRỌN GÓI (ACCOUNTING WORKFLOW)

Quy trình cung cấp dịch vụ kế toán thuế trọn gói cho khách hàng của STAX gồm các bước chính sau:

```
Nhận hóa đơn, chứng từ (CRM) ──► Phân tích & Phân loại
                                    └──► Lập định khoản chứng từ
                                          └──► Tạo Phiếu Thu/Chi (Finote)
                                                └──► Kết chuyển & Lập Báo cáo Thuế
```

### 2.1) Tiếp nhận dữ liệu đầu vào
*   Khách hàng gửi hóa đơn, chứng từ điện tử qua CRM hoặc Google Drive tích hợp.
*   Hệ thống tự động phát hiện, trích xuất dữ liệu thô và lưu trữ tại module CRM.

### 2.2) Xử lý nghiệp vụ Kế toán (Accounting)
*   **Chứng từ dòng tiền (`Finote`):** 
    *   Tạo chứng từ nghiệp vụ thu/chi tương ứng với mỗi giao dịch thực tế.
    *   Mỗi `Finote` bắt buộc liên kết với `organizationId` của khách hàng và định danh nhân viên thực hiện (`employeeId`).
*   **Sổ quỹ tiền mặt (Cash Book):**
    *   Ghi nhận luồng tiền mặt thực tế lưu chuyển, tự động cập nhật số dư tức thời khi `Finote` được phê duyệt.
*   **Định khoản thủ công (Manual Entries):**
    *   Hỗ trợ kế toán viên định khoản các nghiệp vụ đặc thù thông qua các tài khoản kế toán chuẩn.

---

## 3. NGHIỆP VỤ CRM & KANBAN PIPELINE

Quy trình chăm sóc và chuyển đổi khách hàng tiềm năng:

### 3.1) Đường ống quản lý cơ hội (CRM Kanban Pipeline)
*   **Trạng thái Lead:** `Acquired` (Đã tiếp cận) ──► `Contacted` (Đã liên hệ) ──► `Qualified` (Đạt điều kiện) ──► `Converted` (Chuyển đổi thành khách hàng chính thức).
*   **Tính năng Kanban:** Cho phép kéo thả trực quan để thay đổi trạng thái Lead. Khi chuyển đổi (`Converted`), hệ thống tự động sinh tài khoản `User` và hồ sơ `Organization` mới tương ứng cho khách hàng.

### 3.2) CRM Analytics
*   Hệ thống định kỳ tổng hợp và phân tích tỷ lệ chuyển đổi giữa các bước của đường ống, doanh thu dự kiến và hiệu suất làm việc của từng đại diện bán hàng (`employeeId`).

---
*Tài liệu này định hình logic nghiệp vụ mà mã nguồn phải phản ánh chính xác.*
